#python convertBlogLoctionMentionsJson_Csv.py geoCode_outputs/ca/geoCodeLocations_output/
import argparse, os, json, csv
from pprint import pprint

def rscandir(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.json'):
				yield (root, file)

def convertToCSV(geoCodeLocations_output):
	allMentionsDict = {}
	csvFile = open('allBlogLocationMentions.csv', 'w')
	csvFile_nonCity = open('allBlogLocation_nonCity_Mentions.csv', 'w')
	csvFile_city = open('allBlogLocation_City_Mentions.csv', 'w')
	csvWriter = csv.writer(csvFile)
	csvWriter_nonCity = csv.writer(csvFile_nonCity)
	csvWriter_city = csv.writer(csvFile_city)
	csvWriter.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_found_in_blogFiles"])
	csvWriter_nonCity.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_found_in_blogFiles"])
	csvWriter_city.writerow(["mention_name","mention_type", "mention_popularity", "mention_address", "mention_found_in_blogFiles"])
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
				else:
					allMentionsDict[mention] = {}
					allMentionsDict[mention]['mentioned_in_blogFiles'] = fileName
					allMentionsDict[mention]['address']= mentions[mention]['address']
					allMentionsDict[mention]['locType']= mentions[mention]['locType']
				#print(allMentionsDict[mention])
	for mention in allMentionsDict:
		csvWriter.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['address'], allMentionsDict[mention]['mentioned_in_blogFiles']])
		if allMentionsDict[mention]['locType'] == "city":
			csvWriter_city.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['address'], allMentionsDict[mention]['mentioned_in_blogFiles']])
		else:
			csvWriter_nonCity.writerow([mention,allMentionsDict[mention]['locType'], len(allMentionsDict[mention]['mentioned_in_blogFiles']), allMentionsDict[mention]['address'], allMentionsDict[mention]['mentioned_in_blogFiles']])

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
