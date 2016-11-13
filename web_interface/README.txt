https://pouchdb.com/guides/setup-couchdb.html#installing-couchdb
sudo apt-get install couchdb

https://pouchdb.com/guides/setup-couchdb.html#verify-your–installation
curl localhost:5984
{"couchdb":"Welcome","uuid":"fce82d87d3184fa8a976b9075ced960f","version":"1.6.0","vendor":{"name":"Ubuntu","version":"15.10"}}
http://localhost:5984/_utils/fauxton/

https://pouchdb.com/guides/setup-couchdb.html#set-up-cors
sudo npm install -g add-cors-to-couchdb
/usr/local/bin/add-cors-to-couchdb -> /usr/local/lib/node_modules/add-cors-to-couchdb/bin.js
add-cors-to-couchdb@0.0.6 /usr/local/lib/node_modules/add-cors-to-couchdb
├── yargs@1.3.3
├── lie@3.1.0 (immediate@3.0.6)
└── node-fetch@1.6.3 (is-stream@1.1.0, encoding@0.1.12)


