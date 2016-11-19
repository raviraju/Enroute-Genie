var pouchDB = new PouchDB('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/enroute_db');
pouchDB.info().then(function (info) {
    console.log(info);
})

pouchDB.get('anaheim_and_beverly hill').then(function (doc) {
  console.log(doc);
});
