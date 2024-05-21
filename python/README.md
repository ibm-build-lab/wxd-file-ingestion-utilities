# Python helper to ingest a JSON document file

To run `elastic_ingest.py` do the following: 

## Clone repo

- Change lines 24 and 25 in `elastic_ingest.py` to add your Elastic cloud url and API key. 
- Change line 95 to location of JSON file containing documents
- On Lines 99-104 adjust fields to match the format of JSON document object

Eventually these need to be environment variables added to .env


## Set up python environment

```
python3 -m pip install elasticsearch[async]
python3 -m venv assetEnv
source assetEnv/bin/activate
```

## Run code to bulk ingest
```
python3 python3 elastic_ingest.py
```
## Create a destination index if it doesn't exist
```
Run the following in the Elastisearch `Dev Tools` console, adjust to match your JSON document format:

PUT /knowledge_base_dest
{
  "mappings": {
    "properties": {
       "text": {"type": "text"},
        "chunk_number": {"type": "integer"},
        "embedding": {"type": "sparse_vector"},
        "url": {"type": "text"},  
        "article_metadata": {"type": "text"},  
        "article_content": {"type": "text"}  
      }
  }
}
```
## Create the ingestion pipeline
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
## Re index from source to destination index running it thru the pipeline

Once the source has been ingested using the `elastic_ingest.py`. Enter the following into the Elasticsearch `Dev Tools` console and run it:
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
## Optional
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
