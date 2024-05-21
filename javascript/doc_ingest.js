'use strict'

require('array.prototype.flatmap').shim()
const { Client } = require('@elastic/elasticsearch')
const client = new Client({
cloud: { id: '<cloud_id>'},
auth: { apiKey: '<api_key>' }
})
const dataset = require('./source_documents.json')

// Create and load the source index
async function run () {
await client.indices.create({
    index: 'knowledge-base-src',
    operations: {
    mappings: {
        properties: {
        title: { type: 'text' },
        content: { type: 'text' },
        url: { type: 'text' },
        source: { type: 'text' },
        public_record: { type: 'boolean' },
        objectID: { type: 'text' }
        }
    }
    }
}, { ignore: [400] })

const operations = dataset.flatMap(doc => [{ index: { _index: 'knowledge-base-src' } }, doc])

const bulkResponse = await client.bulk({ refresh: true, operations })

if (bulkResponse.errors) {
    const erroredDocuments = []
    // The items array has the same order of the dataset we just indexed.
    // The presence of the `error` key indicates that the operation
    // that we did for the document has failed.
    bulkResponse.items.forEach((action, i) => {
    const operation = Object.keys(action)[0]
    if (action[operation].error) {
        erroredDocuments.push({
        // If the status is 429 it means that you can retry the document,
        // otherwise it's very likely a mapping error, and you should
        // fix the document before to try it again.
        status: action[operation].status,
        error: action[operation].error,
        operation: operations[i * 2],
        document: operations[i * 2 + 1]
        })
    }
    })
    console.log(erroredDocuments)
}

const count = await client.count({ index: 'knowledge-base-src' })
console.log(count)
}

run().catch(console.log)
