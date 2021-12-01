#https://pythonhosted.org/CouchDB/ https://pypi.python.org/pypi/CouchDB#downloads
#python loadData_CouchDb.py merge_data/geoCodeLocations_output/
#enroute_db database exists
#Reading data from 1 : anaheim_and_berkeley.json
#Reading data from 2 : anaheim_and_beverly hills.json

import argparse, os, json, csv
from pprint import pprint
import couchdb

# dbServer = couchdb.Server('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/')#Server object, representing a CouchDB server
dbServer = couchdb.Server('https://apikey-v2-1w7lqsfnsd7z7kv2de3laf7226h9t5n2iqairxr04zuj:e0e4df75b8bdfc30d1c04f4cd999aa30@ee115bef-3371-43ed-90c8-93ba65d99daa-bluemix.cloudantnosqldb.appdomain.cloud/')
db = None

def initDb(dbName):
    global db
    if dbName in dbServer:
        db = dbServer[dbName]
        print('{} database exists'.format(dbName))
    else:
        db = dbServer.create(dbName)
        print('{} database created'.format(dbName))

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)

def loadData(dataDir):
    count = 0
    for path,fileName in rscandir(dataDir):
        filePath = os.path.join(path, fileName)
        count += 1
        print("Reading data from {} : {}".format(count, fileName))
        with open(filePath) as data_file:
            doc = json.load(data_file)
            doc['_id'] = fileName.replace('.json','')
            global db
            try:
                db.save(doc)
                #pprint(doc['mentions'].keys())
            except Exception as e:
                print("Cannot save : ", data_file)
                print(e)


def main():
    parser = argparse.ArgumentParser(description="load data into couchDB")
    parser.add_argument("dataDir", help="path to directory of json files to be loaded into couchDB")
    args = parser.parse_args()
    dataDir = args.dataDir
    initDb('enroute_genie')
    loadData(dataDir)

if __name__ == "__main__" : main()

