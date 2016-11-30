import argparse, json, csv, os
from pprint import pprint

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)

def mergeEnrichedMentionData(mentionData_withBlogLinks_output, geoCodeLocations_output):
    for path,fileName in rscandir(mentionData_withBlogLinks_output):
        filePath = os.path.join(path, fileName)
        print("\nReading mention data from {}".format(fileName))
        with open(filePath) as data_file:
            data = json.load(data_file)
            if "mention_name" in data:
                mention_name = data["mention_name"]
                blogFilesInfo = data["mention_found_in_blogFiles"]
                blogFiles = blogFilesInfo.split(',')
                #print(len(blogFiles))
                for blogFile in blogFiles:
                    outputFilePath = geoCodeLocations_output+blogFile.replace('\"','')
                    currentJsonData = {}
                    newJsonData = {}
                    if os.path.isfile(outputFilePath):
                        with open(outputFilePath,'r') as outFile:
                            currentJsonData = json.load(outFile).copy()
                        #print(currentJsonData)
                        if mention_name in currentJsonData["mentions"]:
                            newJsonData = currentJsonData.copy()
                            #pprint(newJsonData["mentions"][mention_name])
                            newJsonData["mentions"][mention_name]['enrich_metadata'] = data
                            #pprint(newJsonData["mentions"][mention_name])
                        with open(outputFilePath,'w') as update_outFile:
                            json.dump(newJsonData, update_outFile, indent =4)
                            print("Updated mention : {} enriched metadata in {}".format(mention_name, outputFilePath))
                    else:
                        print("{} doesnt exist".format(outputFilePath))
                        #pass

#python new_mergeAllResults.py merge_data/mentionData_withBlogLinks_output/ merge_data/geoCodeLocations_output/ merge_data/cityData_output/
def main():
    parser = argparse.ArgumentParser(description="integrate data for enroute-genie mashup")
    parser.add_argument("mentionData_withBlogLinks_output", help="path to mentionData_withBlogLinks_output") #merge_data/mentionData_withBlogLinks_output/
    parser.add_argument("geoCodeLocations_output", help="path to geoCodeLocations_output") #merge_data/geoCodeLocations_output/
    parser.add_argument("cityData_output", help="path to cityData_output") #merge_data/cityData_output/

    args = parser.parse_args()
    mentionData_withBlogLinks_output = args.mentionData_withBlogLinks_output
    geoCodeLocations_output = args.geoCodeLocations_output
    cityData_output = args.cityData_output
    
    mergeEnrichedMentionData(mentionData_withBlogLinks_output, geoCodeLocations_output)
    
    mergeEnrichedMentionData(cityData_output, geoCodeLocations_output)

if __name__ == "__main__" : main()
