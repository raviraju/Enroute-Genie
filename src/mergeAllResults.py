import argparse, json, csv, os
from pprint import pprint

linkedAttractionsDict = {}
allTripAdvisorAttractionsDict = {}

def getFileName(mention):
    return mention.lower().replace(' ', '_')

def load_record_linked_mention_csvFile(record_linked_mention_csvFileName):
    with open(record_linked_mention_csvFileName, 'r') as record_linked_mention_csvFile:
        reader = csv.reader(record_linked_mention_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                #location = row[0]
                #record_linked_city_Dict[location] = row[12]
                #pprint(record_linked_city_Dict[location])
                mention = row[0]
                #print(mention)
                for index,info in enumerate(row):
                    key = keys[index].split('@')[0]
                    if key == "attraction_name":
                        fileName = getFileName(mention)
                        linkedAttractionsDict[info] = (fileName + '.json', mention)
            else:
                keys = row
            rownum += 1

def load_tripAdvisorAttractions(tripAdvisorAttractions_csvFileName):
    with open(tripAdvisorAttractions_csvFileName, 'r') as tripAdvisorAttractions_csvFile:
        reader = csv.reader(tripAdvisorAttractions_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                #location = row[0]
                #record_linked_city_Dict[location] = row[12]
                #pprint(record_linked_city_Dict[location])
                attraction_name = row[0]
                allTripAdvisorAttractionsDict[attraction_name] = {}
                #print(attraction_name)
                for index,info in enumerate(row):
                    key = keys[index]
                    allTripAdvisorAttractionsDict[attraction_name][key] = info
            else:
                keys = row
            rownum += 1
            
def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)

def enrichBlogLocations(path_blogLocation, path_tripAdvCityAttractions):
    for path,fileName in rscandir(path_blogLocation):
        filePath = os.path.join(path, fileName)
        print("\nReading locations from {}".format(fileName))
        with open(filePath) as data_file:
            data = json.load(data_file)
            new_data = {}
            new_data = data.copy()
            #pprint(new_data)
            for mention in data["mentions"]:
                if data["mentions"][mention]["locType"] == "city":
                    fileName = getFileName(mention)
                    cityJsonFilePath = 'cityData_output/' + fileName+ '.json'
                    if os.path.isfile(cityJsonFilePath):
                        print("Enriched city data exists for {}".format(mention))
                        with open(cityJsonFilePath) as cityJsonFile:
                            blogLinks = data["mentions"][mention]['blogLinks']
                            closest_to = data["mentions"][mention]['closest_to']
                            enrichCityData = json.load(cityJsonFile)
                            new_data["mentions"][mention] = enrichCityData
                            new_data["mentions"][mention]['blogLinks'] = blogLinks
                            new_data["mentions"][mention]['closest_to'] = closest_to
                            #pprint(new_data["mentions"][mention])
                            attraction_in_file = new_data["mentions"][mention]['attraction_in_file']
                            cityMentionsPath = path_tripAdvCityAttractions + attraction_in_file
                            print(cityMentionsPath)
                            with open(cityMentionsPath, 'r') as cityMentions:
                                cityMentionsData = json.load(cityMentions)
                                for cityMention in cityMentionsData:
                                    if cityMention in linkedAttractionsDict:
                                        print(linkedAttractionsDict[cityMention])
                                        mention_to_be_enriched = linkedAttractionsDict[cityMention][1]
                                        enrich_file = linkedAttractionsDict[cityMention][0]
                                        print("{} is to be enriched".format(mention_to_be_enriched))
                                        blogLinks = None
                                        closest_to = None
                                        if mention_to_be_enriched in new_data["mentions"]:#already present
                                            blogLinks = new_data["mentions"][mention_to_be_enriched]['blogLinks']
                                            closest_to = new_data["mentions"][mention_to_be_enriched]['closest_to']
                                        enrich_filePath = 'mentionData_output/' + enrich_file
                                        if os.path.isfile(enrich_filePath):
                                            with open(enrich_filePath) as enrichMentions:
                                                enrichMentionsData = json.load(enrichMentions)
                                                new_data["mentions"][mention_to_be_enriched] = enrichMentionsData
                                                print("New enriched data added")
                                                pprint(new_data["mentions"][mention_to_be_enriched])
                                    else:
                                        print("{} is not linked".format(cityMention))
                    else:
                        new_data["mentions"][mention] = data["mentions"][mention]
                        fileName = getFileName(mention)
                        unlinked_cityJsonFilePath = 'cityData_output_unlinked/' + fileName+ '.json'
                        with open(unlinked_cityJsonFilePath, 'w') as unlinked_cityJsonFile:
                            json.dump(data["mentions"][mention], unlinked_cityJsonFile, indent=4)

def main():
    parser = argparse.ArgumentParser(description="integrate data for enroute-genie mashup")
    parser.add_argument("record_linked_mention_csvFile", help="csvFile input record linked mentions from blogs, tripAdvisor and dbPedia") #record_linkage_results/nonCity_result.csv
    parser.add_argument("tripAdvisorAttractions_csvFile", help="csvFile tripAdvisorAttractions") #record_linkage_results/tripAdvisor_attractions_with_LatLong_withYouTube.csv
    parser.add_argument("path_blogLocation", help="path to blogLocation Jsons directory") #record_linkage_results/geoCodeLocations_output
    parser.add_argument("path_tripAdvCityAttractions", help="path to tripAdvisor City Attractions Jsons directory") #record_linkage_results/tripAdvisor_attractions
    args = parser.parse_args()
    record_linked_mention_csvFileName = args.record_linked_mention_csvFile
    tripAdvisorAttractions_csvFileName = args.tripAdvisorAttractions_csvFile
    path_blogLocation = args.path_blogLocation
    path_tripAdvCityAttractions = args.path_tripAdvCityAttractions
    
    load_record_linked_mention_csvFile(record_linked_mention_csvFileName)
    load_tripAdvisorAttractions(tripAdvisorAttractions_csvFileName)
    
    enrichBlogLocations(path_blogLocation, path_tripAdvCityAttractions)
    
    #pprint(linkedAttractionsDict)
    #pprint(allTripAdvisorAttractionsDict)
    
if __name__ == "__main__" : main()
