var pouchDB = new PouchDB('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/enroute_db');
pouchDB.info().then(function (info) {
    console.log(info);
})

function myCallbackFunction(data){
    //$('body').text(data.response);
    console.log(data.response);
}
    
$.getJSON("http://localhost:8000/data/anaheim_and_berkeley.json?callback=myCallbackFunction", function(json) {
    console.log(json); // this will show the info it in firebug console
});
