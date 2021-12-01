#python34 fetchImages_integrate_ReviewComments.py record_linkage_results/nonCity_result.csv record_linkage_results/tripAdvisor_attractions/

import argparse, json, csv, os
from pprint import pprint
from imageFetch import fetchImages

record_linked_city_Dict = {}

def getFileName(mention):
    mention = mention.replace('/','_or_')
    return mention.lower().replace(' ', '_')

def load_record_linked_mention_csvFile(record_linked_mention_csvFileName, attractions_in_city_path):
    keys = None
    with open(record_linked_mention_csvFileName, 'r') as record_linked_mention_csvFile:
        reader = csv.reader(record_linked_mention_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                #location = row[0]
                #record_linked_city_Dict[location] = row[12]
                #pprint(record_linked_city_Dict[location])
                mention = row[0]
                print(rownum, mention)
                fileName = getFileName(mention)
                mentionJsonFilePath = 'mentionData_output/' + fileName+ '.json'
                if os.path.isfile(mentionJsonFilePath):
                    print("Output already available. Hence Skipping...")
                    continue
                record_linked_mention_Dict = {}
                for index,info in enumerate(row):
                    key = keys[index].split('@')[0]
                    #print(index, key, info)
                    if key in ("attraction_reviewComment", "attraction_url"):#skip those as we are fetching all reviewComments for a attraction in the following segment
                        continue
                    if key == "attraction_in_file":
                        with open(attractions_in_city_path + info, 'r') as city_attractionJson:
                            attractionsData = json.load(city_attractionJson)
                            mentions = attractionsData.keys()
                            for key_mention in mentions:
                                if (key_mention.lower() == mention):
                                    record_linked_mention_Dict['attraction_reviewComments'] = attractionsData[key_mention]['reviewComments']
                                    record_linked_mention_Dict['attraction_reviewUrls'] = attractionsData[key_mention]['urls']                                
                    #if key == "mention_found_in_blogFiles":
                        #info = info.split(',')
                        #for blogPairFileName in info:
                            #print(blogPairFileName)
                            #with open("data_record_linkage_csv/california/city_match/geoCodeLocations_output/" + blogPairFileName) as blogPairFile:
                                #blogData = json.load(blogPairFile)
                                #pprint(blogData["mentions"][mention])
                    record_linked_mention_Dict[key] = info
                imageUrls = fetchImages(mention + ' California')
                record_linked_mention_Dict['imageUrls'] = imageUrls
                with open(mentionJsonFilePath, 'w') as mentionJsonFile:
                    json.dump(record_linked_mention_Dict, mentionJsonFile, indent=4)
                print("Integrated mention data dump at {}".format(mentionJsonFilePath))
            else:
                keys = row
            rownum += 1

def main():
    #imageUrls = fetchImages('Golden Gate Bridge')
    #print(imageUrls)
    parser = argparse.ArgumentParser(description="dump mention json data with relevant images and reviewComments_Urls of tripAdvisor for enroute-genie mashup")
    parser.add_argument("record_linked_mention_csvFile", help="csvFile input record linked mentions from blogs, tripAdvisor and dbPedia") #record_linkage_results/nonCity_result.csv
    parser.add_argument("path_attractions_in_city", help="path to attractions_in_city folder") #record_linkage_results/tripAdvisor_attractions/
    args = parser.parse_args()
    record_linked_mention_csvFileName = args.record_linked_mention_csvFile
    attractions_in_city_path = args.path_attractions_in_city
    load_record_linked_mention_csvFile(record_linked_mention_csvFileName, attractions_in_city_path)
    
if __name__ == "__main__" : main()
