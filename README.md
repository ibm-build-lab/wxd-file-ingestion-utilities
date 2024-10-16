# watsonx Discovery Document Ingestion Utilities
This repo contains code and links to utilities to help with file ingestion into **watsonx Discovery** (Note that **watsonx Discovery** is synonymous with **Elasticsearch**)

##  RAG-LLM utility ingestDocs API
[RAG-LLM](https://github.com/annumberhocker/RAG-LLM-App) is an application that can be started locally, in Code Engine, or on an OpenShift cluster. There is [terraform automation code](https://github.com/annumberhocker/RAG-LLM-App/codeengine-terraform-setup) to help deploy this into Code Engine on IBM Cloud.  This application includes 3 different apis: 
- `ingestDocs`: ingest documents of different types from a Cloud Object Storage bucket.
- `queryLLM`: retrieve documents from an Elasticsearch index and send them into LLM for natural language response
- `queryWDLLM`: retrieve documents from a Watson Discovery Collection and send them into LLM for natural language response

## LlamaIndex document ingestion script
[watsonx Discovery setup and ingestion](https://github.com/ibm-build-lab/watsonx-wxd-setup-and-ingestion) is a python application that uses the LlamaIndex framework to ingest and chunk documents (located locally or in COS) into an Elasticsearch instance. This utility can ingest multiple documents of type `.pdf`, `.txt`, `.docx`, and `.pptx` at one time.

## Elasticsearch helper function scripts
Elasticsearch provides helper functions that use their [_bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) to ingest documents that have been saved in JSON format.

### Python
Read the [python README](./python/README.md) for details on running a [python script](./python/doc_ingest.py) to ingest a JSON file

### Javascript
Read the [javascript README](./javascript/README.md) for details on running a [javascript](./javascript/doc_ingest.js) to ingest a JSON file

## Use Elasticsearch apis
See steps here [Working with PDF and Office Documents in Elasticsearch](https://github.com/watson-developer-cloud/assistant-toolkit/blob/master/integrations/extensions/docs/elasticsearch-install-and-setup/how_to_index_pdf_and_office_documents_elasticsearch.md)

## Webcrawling

- [Using web crawler in Elasticsearch](./README_webcrawl.md)
- [Using external tools to scrape websites (turn websites into documents in JSON format, then use python or javascript above to ingest)](https://github.com/ibm-build-lab/webcrawling-scripts/blob/main/README.md)

## Additional utilities
A couple of other methods and utilities:

[Elastic documentation on how to ingest data](https://www.elastic.co/docs/current/serverless/elasticsearch/ingest-your-data)

[Set up a web crawler with Neuralseek](https://github.ibm.com/skol-assets/watsonx-RAG-w-watsonxdiscovery-method1)

[File ingestion from Cloud Object Storage, using python notebooks in watsonx.ai environment](https://github.ibm.com/skol-assets/watsonx-RAG-w-watsonxdiscovery-method2)

