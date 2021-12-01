#python enlist_annotated_attractions_to_csv.py annotated_output_data/los\ angeles_and_san\ francisco.json 
    #No of attraction : 204
    #No of Cities : 24
    #Total No of Interesting Places : 228
    #Total No of Unique Interesting Places : 166
    #Results found in annotated_output_data/los angeles_and_san francisco.csv


import argparse, json, csv

attractionsList = []

def getFileNameCsv(jsonFileName):
    return jsonFileName.replace('.json','.csv')

def enlistAttractionsToCSV(annotated_attractions_jsonFileName):
    with open(annotated_attractions_jsonFileName, 'r') as annotated_attractions_jsonFile:
        data = json.load(annotated_attractions_jsonFile)
        print("No of attraction : {}".format(len(data['attractions'])))
        print("No of Cities : {}".format(len(data['cities'])))
        attractionsList.extend([attraction.lower() for attraction in data['attractions']])
        attractionsList.extend([attraction.lower() for attraction in data['cities']])
        print("Total No of Interesting Places : {}".format(len(attractionsList)))
        attractionsUniqueList = list(set(attractionsList))
        print("Total No of Unique Interesting Places : {}".format(len(attractionsUniqueList)))
        attractionsUniqueList.sort()
        csvFileName = getFileNameCsv(annotated_attractions_jsonFileName)
        csvFile = open(csvFileName, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["annotated_mention_name"])
        for attraction in attractionsUniqueList:
            csvWriter.writerow([attraction])
        print("Results found in {}".format(csvFileName))

def main():
    parser = argparse.ArgumentParser(description="read annotated attractions in json and enlist in sorted order to csv")
    parser.add_argument("annotated_attractions_json", help="annotated attractions json file")
    args = parser.parse_args()
    annotated_attractions_json = args.annotated_attractions_json

    enlistAttractionsToCSV(annotated_attractions_json)

if __name__ == "__main__" : main()




