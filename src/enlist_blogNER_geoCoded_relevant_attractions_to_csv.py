#>python enlist_blogNER_geoCoded_relevant_attractions_to_csv.py output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/los\ angeles_and_san\ francisco.json 
#    No of locations : 176
#    Results found in output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/los angeles_and_san francisco.csv


import argparse, json, csv

def getFileNameCsv(jsonFileName):
    return jsonFileName.replace('.json','.csv')

def enlistAttractionsToCSV(blogNER_geoCoded_relevant_attractions_jsonFileName):
    with open(blogNER_geoCoded_relevant_attractions_jsonFileName, 'r') as blogNER_geoCoded_relevant_attractions_jsonFile:
        data = json.load(blogNER_geoCoded_relevant_attractions_jsonFile)
        locations = [mention.lower() for mention in data['mentions'].keys()]
        print("No of locations : {}".format(len(locations)))
        locations.sort()
        csvFileName = getFileNameCsv(blogNER_geoCoded_relevant_attractions_jsonFileName)
        csvFile = open(csvFileName, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["blogNER_geoCoded_relevant_mention_name"])
        for location in locations:
            csvWriter.writerow([location.lower()])
        print("Results found in {}".format(csvFileName))

def main():
    parser = argparse.ArgumentParser(description="read blog NER GeoCoded relevant attractions from json and enlist in sorted order to csv")
    parser.add_argument("blogNER_geoCoded_relevant_attractions_json", help="blog NER GeoCoded relevant attractions json file")
    args = parser.parse_args()
    blogNER_geoCoded_relevant_attractions_json = args.blogNER_geoCoded_relevant_attractions_json

    enlistAttractionsToCSV(blogNER_geoCoded_relevant_attractions_json)

if __name__ == "__main__" : main()




