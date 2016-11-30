#python enlist_blogNER_attractions_to_csv.py output_candidate_location_from_blogs_using_NER/california/los\ angeles_and_san\ francisco.json 
    #No of locations : 222
    #Results found in output_candidate_location_from_blogs_using_NER/california/los angeles_and_san francisco.csv


import argparse, json, csv

def getFileNameCsv(jsonFileName):
    return jsonFileName.replace('.json','.csv')

def enlistAttractionsToCSV(blogNER_attractions_jsonFileName):
    with open(blogNER_attractions_jsonFileName, 'r') as blogNER_attractions_jsonFile:
        data = json.load(blogNER_attractions_jsonFile)
        locations = [location.lower() for location in data['location_BlogUrls'].keys()]
        print("No of locations : {}".format(len(locations)))
        locations.sort()
        csvFileName = getFileNameCsv(blogNER_attractions_jsonFileName)
        csvFile = open(csvFileName, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["blogNER_mention_name"])
        for location in locations:
            csvWriter.writerow([location])
        print("Results found in {}".format(csvFileName))

def main():
    parser = argparse.ArgumentParser(description="read blog NER attractions from json and enlist in sorted order to csv")
    parser.add_argument("blogNER_attractions_json", help="blog NER attractions json file")
    args = parser.parse_args()
    blogNER_attractions_json = args.blogNER_attractions_json

    enlistAttractionsToCSV(blogNER_attractions_json)

if __name__ == "__main__" : main()




