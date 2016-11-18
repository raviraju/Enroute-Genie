var db = new PouchDB('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/kittens');
db.info().then(function (info) {
    console.log(info);
})
//PouchDB.debug.enable('*');//can enable debug logging, to disable : PouchDB.debug.disable();
//PouchDB.debug.disable();

//https://pouchdb.com/guides/documents.html#storing-a–document
var doc = {
  "_id": "mittens",
  "name": "Mittens",
  "occupation": "kitten",
  "age": 3,
  "hobbies": [
    "playing with balls of yarn",
    "chasing laser pointers",
    "lookin' hella cute"
  ]
};
//db.put(doc);
//Fetch doc
db.get('mittens').then(function (doc) {
  console.log(doc);
});

//https://pouchdb.com/guides/documents.html#updating-documents–correctly
// fetch mittens
db.get('mittens').then(function (doc) {
  // update their age
  doc.age = 4;
  // put them back
  return db.put(doc);
}).then(function () {
  // fetch mittens again
  return db.get('mittens');
}).then(function (doc) {
  console.log(doc);
});
/*
db.put({_id: 'charlie', age: 21}).then(function () {
  return db.get('charlie');
}).then(function (charlie) {
  // increment Charlie's age
  charlie.age++;
  return db.put(charlie);
}).then(function () {
  return db.get('charlie');
}).then(function (charlie) {
  // increment Charlie's age again
  charlie.age++;
  return db.put(charlie);
}).then(function () {
  return db.get('charlie');
}).then(function (charlie) {
  console.log(charlie);
}).catch(function (err) {
  console.log(err);
});
*/
//https://pouchdb.com/api.html#create_document
//https://pouchdb.com/api.html#delete_document
//https://pouchdb.com/api.html#fetch_document


//https://pouchdb.com/guides/bulk-operations.html
//PouchDB provides two methods for bulk operations - bulkDocs() for bulk writes, and allDocs() for bulk reads.
db.bulkDocs([
  {
    _id: 'ravi',
    occupation: 'softie',
    cuteness: 9.0
  },
  {
    _id: 'katie',
    occupation: 'kitten',
    cuteness: 7.0
  },
  {
    _id: 'felix',
    occupation: 'kitten',
    cuteness: 8.0
  }
]);
//https://pouchdb.com/api.html#batch_create
//https://pouchdb.com/api.html#batch_fetch
db.put({
    _id: new Date().toJSON(),
    name: 'Mittens',
    occupation: 'kitten',
    cuteness: 9.0
}).then(function () {
  return db.put({
    _id: new Date().toJSON(),
    name: 'Katie',
    occupation: 'kitten',
    cuteness: 7.0
  });
}).then(function () {
  return db.put({
    _id: new Date().toJSON(),
    name: 'Felix',
    occupation: 'kitten',
    cuteness: 8.0
  });
}).then(function () {
  return db.allDocs({include_docs: true});
}).then(function (response) {
  console.log(response);
}).catch(function (err) {
  console.log(err);
});


//https://pouchdb.com/2014/04/14/pagination-strategies-with-pouchdb.html
var pouch = new PouchDB('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/numbers');
var docs = [
  {_id : 'doc01', name : 'uno'},        {_id : 'doc02', name : 'dos'},
  {_id : 'doc03', name : 'tres'},       {_id : 'doc04', name : 'cuatro'},
  {_id : 'doc05', name : 'cinco'},      {_id : 'doc06', name : 'seis'},
  {_id : 'doc07', name : 'siete'},      {_id : 'doc08', name : 'ocho'}, 
  {_id : 'doc09', name : 'nueve'},      {_id : 'doc10', name : 'diez'},  
  {_id : 'doc11', name : 'once'},       {_id : 'doc12', name : 'doce'},
  {_id : 'doc13', name : 'trece'},      {_id : 'doc14', name : 'catorce'},
  {_id : 'doc15', name : 'quince'},     {_id : 'doc16', name : 'dieciseis'},
  {_id : 'doc17', name : 'diecisiete'}, {_id : 'doc18', name : 'dieciocho'},
  {_id : 'doc19', name : 'diecinueve'}, {_id : 'doc20', name : 'veinte'},
];
pouch.bulkDocs({docs : docs}, function (err, response) {
  // handle err or response
  console.log("pouch.bulkDocs response : ", response);
  console.log(err);
});
pouch.allDocs({include_docs: true}).then(function(response) {
  // handle err or response
  console.log("pouch.allDocs response : ", response);
}).catch(function (err) {
  console.log(err);
});



//Temporary queries
/*pouch.query(function (doc, emit) {
  emit(doc.name);
}, {include_docs: true, key: 'nueve'}).then(function (result) {
  // found docs with name === 'nueve'
  console.log("found docs with name nueve");
  console.log(result)
}).catch(function (err) {
  // handle any errors
});*/


// document that tells PouchDB/CouchDB
// to build up an index on doc.name
var ddoc = {
  _id: '_design/my_index',
  views: {
    by_name: {
      map: function (doc) { emit(doc.name); }.toString()
    }
  }
};
// save it
pouch.put(ddoc).then(function () {
  // success!
}).catch(function (err) {
  // some error (maybe a 409, because it already exists?)
});
