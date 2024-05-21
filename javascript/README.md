# Javascript utility to bulk load data into Elasticsearch

This utility will create a source index and load data from a file containing an array of JSON objects. 

It is assumed that you have an instance of **watsonx Discovery** provisioned and set up with **Kibana** and **Enterprise** search.  
For steps to do this see https://cloud.ibm.com/docs/databases-for-elasticsearch?topic=databases-for-elasticsearch-tutorial-elasticsearch-enterprise-search-tutorial.

## Clone directory and run utility
Create an Elasticsearch API key. Within **Kibana**, go to **Management** page under **Security**.

Add API key as well as the Elasticsearch URL in the doc_ingest.js code, lines 7 and 8.

To run this script:

    npm i @elastic/elasticsearch@8
    npm i array.prototype.flatmap
    node doc_ingest.js

Once the data has been loaded, verify it either manually or programmatically. In **Kibana**, go to **Search** > **Content** > **Indeces**. Open the *knowldege-base-src* index.  Go to the **Documents** tab to see the data.

## Optional: steps to create embeddings for the ingested text

### Create a destination index

To create a destination index use the same schema as the source index but with a field to store the content embeddings.  Using the **Kibana Dev Tools Console**, enter the following and hit the **>** run icon:

    PUT /knowledge-base-dest
    {
        "mappings": {
            "properties": {
                "content_embedding": { 
                    "type": "sparse_vector" 
                },
                "title": { 
                    "type": "text" 
                },
                "content": { 
                    "type": "text" 
                },
                "url": { 
                    "type": "text" 
                }
            }
        }
    }

### Create an ingest pipeline with inference processor 
See [Ingest pipelines](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html).

Enter the following and hit the **>** run icon:

    PUT _ingest/pipeline/my-content-embedding-pipeline
    {
      "processors": [
        {
          "inference": {
            "model_id": ".elser_model_2_linux-x86_64",
            "input_output": [
              {
                "input_field": "content",
                "output_field": "content_embedding"
              }
            ]
          }
        }
      ]
    }

### Run the data thru the Inference index pipeline to create embeddings

To create the text embeddings, run the following code in the dev console. To get the name of the pipeline with the model loaded, in **Kibana**, go to **Machine Learning** > **Trained Models**.  Expand the Deployed model, go to the **Pipelines** tab, you will see *my-content-embeddings-pipeline* that was created in the previous step:

    POST _reindex?wait_for_completion=false
    {
        "source": {
            "index": "knowledge-base-src",
            "size": 50 
        },
        "dest": {
            "index": "knowledge-base-dest",
            "pipeline": "my-content-embedding-pipeline"
        }
    }

NOTE:  To confirm that this task was successful, run the following command using the task id produced in the response from previous command.

    GET _tasks/<task_id>

To verify the content embeddings are in the new destination index, in **Kibana**, go to **Search** > **Content** > **Indeces**. Open the *search-gs-docs-dest* index.  Open the **Documents** tab to see the data noting the new *content_embedding* field.

## Test the semantic search

Use the *text_expansion* query and provide the query text and the ELSER model ID. The *content_embedding* field contains the generated output:

    GET knowledge-base-dest/_search
    {
        "query":{
            "text_expansion":{
                "content_embedding":{
                    "model_id":".elser_model_2_linux-x86_64",
                    "model_text":"Put sample query here"
                }
            }
        }
    }

