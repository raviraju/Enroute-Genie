#python convertBlogLoctionMentionsJson_Csv.py output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/
import argparse, os, json, csv
from pprint import pprint

def rscandir(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.json'):
				yield (root, file)

def getNoOfBlogFiles(blogFileString):
	#blogFileString = "anaheim_and_fresno.json,anaheim_and_san jose.json,anaheim_and_sausalito.json,avalon_and_bakersfield.json,bakersfield_and_san bernardino.json,avalon_and_santa clarita.json,avalon_and_sausalito.json,bakersfield_and_long beach.json,bakersfield_and_monterey.json,bakersfield_and_oakland.json,bakersfield_and_riverside.json,bakersfield_and_santa clarita.json,bakersfield_and_sausalito.json,bakersfield_and_stockton.json,big bear lake_and_santa clarita.json,big bear lake_and_sausalito.json,carlsbad_and_oakland.json,carlsbad_and_sacramento.json,carlsbad_and_santa clarita.json,carlsbad_and_stockton.json,fresno_and_los angeles.json,fresno_and_san bernardino.json,huntington beach_and_sacramento.json,huntington beach_and_sausalito.json,irvine_and_sacramento.json,irvine_and_sausalito.json,long beach_and_stockton.json,los angeles_and_sausalito.json,los angeles_and_stockton.json,malibu_and_sausalito.json,mammoth lakes_and_riverside.json,monterey_and_san bernardino.json,oakland_and_santa clarita.json,pasadena_and_sausalito.json,riverside_and_sacramento.json,riverside_and_san francisco.json,riverside_and_sausalito.json,riverside_and_stockton.json,sacramento_and_santa clarita.json,san bernardino_and_san jose.json,san bernardino_and_santa clarita.json,san bernardino_and_sausalito.json,san diego_and_santa clarita.json,san francisco_and_santa clarita.json,san francisco_and_temecula.json,sacramento_and_san bernardino.json,newport beach_and_sausalito.json,san bernardino_and_stockton.json,santa clarita_and_sausalito.json,san luis obispo_and_santa clarita.json,san luis obispo_and_sausalito.json,santa monica_and_sausalito.json,stockton_and_temecula.json"
	no_of_blog_files = len(blogFileString.split(','))
	#print(no_of_blog_files)
	return no_of_blog_files

def convertToCSV(geoCodeLocations_output):
	allMentionsDict = {}
	csvFile = open('allBlogLocationMentions.csv', 'w')
	csvFile_nonCity = open('allBlogLocation_nonCity_Mentions.csv', 'w')
	csvFile_city = open('allBlogLocation_City_Mentions.csv', 'w')
	csvWriter = csv.writer(csvFile)
	csvWriter_nonCity = csv.writer(csvFile_nonCity)
	csvWriter_city = csv.writer(csvFile_city)
	csvWriter.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_longitude", "mention_latitude", "no_of_blogFiles", "mention_found_in_blogFiles"])
	csvWriter_nonCity.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_longitude", "mention_latitude","no_of_blogFiles", "mention_found_in_blogFiles"])
	csvWriter_city.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_longitude", "mention_latitude", "no_of_blogFiles", "mention_found_in_blogFiles"])
	count = 0
	for path,fileName in rscandir(geoCodeLocations_output):
		filePath = os.path.join(path, fileName)
		count+=1
		print("Reading locations from {} : {}".format(count, fileName))
		
		with open(filePath) as data_file:
			data = json.load(data_file)
			#pprint(data)
			mentions = data['mentions']
			for mention in mentions:
				if mention in allMentionsDict:
					current_blogFiles = allMentionsDict[mention]['mentioned_in_blogFiles']
					updated_blogFiles = current_blogFiles + "," + fileName
					allMentionsDict[mention]['mentioned_in_blogFiles'] = updated_blogFiles
					allMentionsDict[mention]['mentioned_in_blogURL'] |= set(mentions[mention]['blogLinks'])
				else:
					allMentionsDict[mention] = {}
					allMentionsDict[mention]['mentioned_in_blogFiles'] = fileName
					allMentionsDict[mention]['address']= mentions[mention]['address']
					allMentionsDict[mention]['locType']= mentions[mention]['locType']
					allMentionsDict[mention]['longitude']= mentions[mention]['longitude']
					allMentionsDict[mention]['latitude']= mentions[mention]['latitude']
					allMentionsDict[mention]['mentioned_in_blogURL'] = set(mentions[mention]['blogLinks'])
				#print(allMentionsDict[mention])
	for mention in allMentionsDict:
		csvWriter.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogURL']), allMentionsDict[mention]['address'], allMentionsDict[mention]['longitude'], allMentionsDict[mention]['latitude'], getNoOfBlogFiles(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['mentioned_in_blogFiles']])
		if allMentionsDict[mention]['locType'] == "city":
			csvWriter_city.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogURL']), allMentionsDict[mention]['address'], allMentionsDict[mention]['longitude'], allMentionsDict[mention]['latitude'], getNoOfBlogFiles(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['mentioned_in_blogFiles']])
		else:
			csvWriter_nonCity.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogURL']), allMentionsDict[mention]['address'], allMentionsDict[mention]['longitude'], allMentionsDict[mention]['latitude'], getNoOfBlogFiles(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['mentioned_in_blogFiles']])

def convertToCSV_BlogUrls(geoCodeLocations_output):
	csvFile = open('csvResults.csv', 'w')
	csvWriter = csv.writer(csvFile)
	csvWriter.writerow(["name","locType", "longitude", "latitude", "closest_to", "blogLinks", "src", "dest", "address", "srcLoc", "destLoc"])
	for path,fileName in rscandir(geoCodeLocations_output):
		filePath = os.path.join(path, fileName)
		print("\nReading locations from {}".format(fileName))
		cityPairCand = fileName.split('_and_')
		cityPair = (cityPairCand[0], cityPairCand[1].rstrip('json').replace('.',''))
		#dist = srcDest_distance(cityPair[0], cityPair[1])
		src = cityPair[0]
		dest = cityPair[1]
		
		with open(filePath) as data_file:
			data = json.load(data_file)
			#pprint(data)
			srcLoc = data['srcLoc']
			destLoc = data['destLoc']
			mentions = data['mentions']
			for mention in mentions:
				for blogLink in mentions[mention]['blogLinks']:
					csvWriter.writerow([mention,
					mentions[mention]['locType'],
					mentions[mention]['longitude'],
					mentions[mention]['latitude'],
					mentions[mention]['closest_to'][0],
					blogLink,
					src,dest,
					mentions[mention]['address'],
					srcLoc,destLoc
					])
def main():
	parser = argparse.ArgumentParser(description="convert geoCoded relevant location mentions of blogs from json to csv")
	parser.add_argument("geoCodeLocations_output", help="path to directory geoCodeLocations_output of json files")
	args = parser.parse_args()
	geoCodeLocations_output = args.geoCodeLocations_output

	convertToCSV(geoCodeLocations_output)

if __name__ == "__main__" : main()
