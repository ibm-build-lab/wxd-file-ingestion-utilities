# watsonx Discovery Document Ingestion Utilities
This repo contains code and links to utilities to help with file ingestion into **watsonx Discovery** (Note that **watsonx Discovery** is synonymous with **Elasticsearch**)

##  RAG-LLM utility ingestDocs API
[RAG-LLM](https://github.com/ibm-build-lab/RAG-LLM-Service) is an application that can be started locally, in Code Engine, or on an OpenShift cluster. There is [terraform automation code](https://github.com/ibm-build-lab/rag-codeengine-terraform-setup) to help deploy this into Code Engine on IBM Cloud.  This application produces 2 different apis: `ingestDocs` and `queryLLM`. 

## LlamaIndex document ingestion utility
[watsonx Discovery setup and ingestion](https://github.com/ibm-build-lab/watsonx-wxd-setup-and-ingestion) is a python application that uses the LlamaIndex framework to ingest and chunk documents (located locally or in COS) into an Elasticsearch instance. This utility can ingest multiple documents of type `.pdf`, `.txt`, `.docx`, and `.pptx` at one time.

## Elasticsearch helper functions
Elasticsearch provides helper functions that use their [_bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) to ingest documents that have been saved in JSON format.

### Python
Read the [python README](./python/README.md) for details on running a [python script](./python/doc_ingest.py) to ingest a JSON file

### Javascript
Read the [javascript README](./javascript/README.md) for details on running a [javascript](./javascript/doc_ingest.js) to ingest a JSON file

## Use Elasticsearch apis
See steps here [Working with PDF and Office Documents in Elasticsearch](https://github.com/watson-developer-cloud/assistant-toolkit/blob/master/integrations/extensions/docs/elasticsearch-install-and-setup/how_to_index_pdf_and_office_documents_elasticsearch.md)

## Additional utilities
A couple of other methods and utilities:

[Set up a web crawler with Neuralseek](https://github.ibm.com/skol-assets/watsonx-RAG-w-watsonxdiscovery-method1)

[File ingestion from Cloud Object Storage, using python notebooks in watsonx.ai environment](https://github.ibm.com/skol-assets/watsonx-RAG-w-watsonxdiscovery-method2)

[How to set up and use the web crawler in Elasticsearch](https://github.com/watson-developer-cloud/assistant-toolkit/blob/master/integrations/extensions/docs/elasticsearch-install-and-setup/how_to_use_web_crawler_in_elasticsearch.md)

