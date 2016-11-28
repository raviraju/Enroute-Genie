import argparse, json, csv
from pprint import pprint
from imageFetch import fetchImages

record_linked_city_Dict = {}

def getFileName(city_mention):
    return city_mention.lower().replace(' ', '_')

def load_record_linked_city_csvFile(record_linked_city_csvFileName, attractions_in_city_path):
    keys = None
    with open(record_linked_city_csvFileName, 'r') as record_linked_city_csvFile:
        reader = csv.reader(record_linked_city_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                #location = row[0]
                #record_linked_city_Dict[location] = row[12]
                #pprint(record_linked_city_Dict[location])
                city_mention = row[0]
                print(rownum, city_mention)
                record_linked_city_Dict = {}
                for index,info in enumerate(row):
                    key = keys[index].split('@')[0]
                    #print(index, key, info)
                    #if key == "attraction_in_file":
                        #with open(attractions_in_city_path + info, 'r') as city_attractionJson:
                            #attractionsData = json.load(city_attractionJson)
                            #pprint(attractionsData)
                    #if key == "mention_found_in_blogFiles":
                        #info = info.split(',')
                        #for blogPairFileName in info:
                            #print(blogPairFileName)
                            #with open("data_record_linkage_csv/california/city_match/geoCodeLocations_output/" + blogPairFileName) as blogPairFile:
                                #blogData = json.load(blogPairFile)
                                #pprint(blogData["mentions"][mention])
                    record_linked_city_Dict[key] = info
                imageUrls = fetchImages(city_mention + ' California')
                record_linked_city_Dict['imageUrls'] = imageUrls
                fileName = getFileName(city_mention)
                #print(imageUrls)
                cityJsonFilePath = 'cityData_output/' + fileName + '.json'
                with open(cityJsonFilePath, 'w') as cityJsonFile:
                    json.dump(record_linked_city_Dict, cityJsonFile, indent=4)
                print("Integrated city data dump at {}".format(cityJsonFilePath))
            else:
                keys = row
            rownum += 1
        #pprint(record_linked_city_Dict)
        #for key in record_linked_city_Dict:
        #    print(key)
        #    print(record_linked_city_Dict[key]["mention_found_in_blogFiles"])
        return
    #print("Read {} results from {}".format(len(tripAdvisor_attractions_YouTube_Dict.keys()), tripAdvisor_attractions_csvFileName))

def main():
    #imageUrls = fetchImages('Golden Gate Bridge')
    #print(imageUrls)
    parser = argparse.ArgumentParser(description="integrate data for enroute-genie mashup")
    parser.add_argument("record_linked_city_csvFile", help="csvFile input record linked city mentions from blogs, tripAdvisor and dbPedia") #record_linkage_results/city_result.csv
    parser.add_argument("path_attractions_in_city", help="csvFile input record linked city mentions from blogs, tripAdvisor and dbPedia") #record_linkage_results/tripAdvisor_attractions/
    args = parser.parse_args()
    record_linked_city_csvFileName = args.record_linked_city_csvFile
    attractions_in_city_path = args.path_attractions_in_city
    load_record_linked_city_csvFile(record_linked_city_csvFileName, attractions_in_city_path)
    
if __name__ == "__main__" : main()
