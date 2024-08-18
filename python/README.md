
# Python utility to bulk load data into Elasticsearch

This utility will create a source index and load data from a file containing an array of JSON objects. 

It is assumed that you have an instance of **watsonx Discovery** provisioned and set up with **Kibana** and **Enterprise** search.  
For steps to do this see https://github.com/ibm-build-lab/terraform-elasticsearch-setup.

This utility loops thru the documents stored in JSON format, chunks them (adding metadata with each chunk), then creates a new 
dictionary containing newline JSON objects with the chunks. These are then ingested into the Elasticsearch `_bulk` API which stores them in the designated index.

**NOTE**: It does not create embeddings in the index. That can be done with the optional steps below.

## Clone directory and run utility

Create an Elasticsearch API key: within **Kibana**, go to **Management** page under **Security**.

- Change lines 24 and 25 in `doc_ingest.py` to add your Elastic cloud url and API key. 
- Change line 93 to location of JSON file containing documents
- Change line 67 to whatever chunk overlap you want (i.e. for a 512 chunk size, overlap of 128 is 25%)
- On Lines 99-104 adjust fields to match the format of JSON document object. This code expects JSON documents in the form of
  ```
  {
    {            
     "url": "",  
     "article_metadata": "",  
     "main_content": ""
    },
    {            
     "url": "",  
     "article_metadata": "",  
     "main_content": ""
    },
    ...
  }

## Set up python environment

```
python3 -m pip install elasticsearch[async]
python3 -m venv assetEnv
source assetEnv/bin/activate
```

## Run code to bulk ingest
This script chunks and ingests the documents. It adds the chunk text into the `text` field and retains the entire document content in the `main_content` field. It does not create text embeddings. That is done in the next step:
```
python3 doc_ingest.py
```

The resulting document format will be:
```
{
   "text": {"type": "text"},
   "chunk_number": {"type": "integer"},
   "url": {"type": "text"},  
   "article_metadata": {"type": "text"},  
   "main_content": {"type": "text"}  
}
```
## Optional: steps to create document embeddings for ingested data

### Create a destination index if it doesn't exist
Run the following in the Elasticsearch `Dev Tools` console, adjust to match your document format:

```
PUT /knowledge_base_dest
{
  "mappings": {
    "properties": {
       "text": {"type": "text"},
       "chunk_number": {"type": "integer"},
       "embedding": {"type": "sparse_vector"},
       "url": {"type": "text"},  
       "article_metadata": {"type": "text"},  
       "main_content": {"type": "text"}  
    }
  }
}
```
### Create the ingestion pipeline
Run the following in the Elastisearch `Dev Tools` console:
```
PUT _ingest/pipeline/elser-tokens-creation
{
 "processors": [
  {
   "inference": {
     "model_id": ".elser_model_2_linux-x86_64",
     "input_output": [
        {
          "input_field": "text",
          "output_field": "content_embedding"
        }
      ]
    }
   }
  }],
 "on_failure": [
  {
   "set": {
    "description": "Index document to 'failed-<index>'",
    "field": "_index",
    "value": "failed-{{{ _index }}}"
   }
  },
  {
   "set": {
    "description": "Set error message",
    "field": "ingest.failure",
    "value": "{{_ingest.on_failure_message}}"
   }
  }
 ]
}
```
### Re-index from source to destination index running it thru the pipeline

Once the source has been ingested into the source index, enter the following into the Elasticsearch `Dev Tools` console and reindex with embeddings:
```
POST _reindex?wait_for_completion=false
{
 "source": {
  "index": "knowledge_base_src",
  "size": 200
 },
 "dest": {
  "index": "knowledge_base_dest",
  "pipeline": "elser-tokens-creation",
  "op_type": "create"
  },
  "conflicts": "proceed"
}

```
To see the progress of the embedding
```
GET _tasks/<task_id>

```
### Optional
To delete documents from an index
```
POST /knowledge_base_dest/_delete_by_query
{
  "query": {
    "match_all": {
    }
  }
}
```
