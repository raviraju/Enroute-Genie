#https://pythonhosted.org/CouchDB/ https://pypi.python.org/pypi/CouchDB#downloads
#python loadData_CouchDb.py data/
#enroute_db database exists
#Reading data from 1 : anaheim_and_berkeley.json
#Reading data from 2 : anaheim_and_beverly hills.json

import argparse, os, json, csv
from pprint import pprint
import couchdb

dbServer = couchdb.Server('https://enroutegenie:genieenroute@enroutegenie.cloudant.com/')#Server object, representing a CouchDB server
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
            db.save(doc)
            #pprint(doc['mentions'].keys())

def main():
    parser = argparse.ArgumentParser(description="load data into couchDB")
    parser.add_argument("dataDir", help="path to directory of json files to be loaded into couchDB")
    args = parser.parse_args()
    dataDir = args.dataDir
    initDb('enroute_genie')
    loadData(dataDir)

if __name__ == "__main__" : main()

