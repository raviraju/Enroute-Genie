import argparse, os, json
from pprint import pprint
#https://pypi.python.org/pypi/geopy/1.11.0
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

citiesTowns = set()
ca_geolocator = Nominatim()

#from geopy.geocoders import GeocoderDotUS
#geolocator = GeocoderDotUS(format_string="%s, California, United States of America")

def get_citiesTowns(cityTown_wikiFile):
	with open(cityTown_wikiFile, 'r') as inFile:
		for line in inFile:
			factList = line.split('\t')
			#print(factList[0])
			citiesTowns.add(factList[0])
	#print(citiesTowns)

def rscandir(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.json'):
				yield (root, file)
				
def srcDest_distance(src,dest):
	srcLoc   = ca_geolocator.geocode(src,timeout=5)
	destLoc  = ca_geolocator.geocode(dest,timeout=5)
	#print(srcLoc.raw)
	#print(destLoc.raw)
	srcLatLong = (srcLoc.latitude, srcLoc.longitude)
	destLatLong = (destLoc.latitude, destLoc.longitude)
	return(vincenty(srcLatLong, destLatLong).miles)

def comboResultsKnown(keyFileName):
    return os.path.isfile('processed_output/' + keyFileName) 

def parseBlogLocations(path_blogLocation):
	for path,fileName in rscandir(path_blogLocation):
		filePath = os.path.join(path, fileName)
		print("\nReading locations from {}".format(fileName))
		cityPairCand = fileName.split('_and_')
		cityPair = (cityPairCand[0], cityPairCand[1].rstrip('json').replace('.',''))
		#dist = srcDest_distance(cityPair[0], cityPair[1])
		src = cityPair[0]
		dest = cityPair[1]
		if comboResultsKnown(fileName):
			print("Combo {},{} was already captured results in : processed_output/{}".format(src, dest, fileName))
			continue
		
		srcLoc   = ca_geolocator.geocode(src + ', California',timeout=5)
		destLoc  = ca_geolocator.geocode(dest+ ', California',timeout=5)
		print("srcLoc.address : {}".format(srcLoc.address))
		print("destLoc.address : {}".format(destLoc.address))
		srcLatLong = (srcLoc.latitude, srcLoc.longitude)
		destLatLong = (destLoc.latitude, destLoc.longitude)
		
		#ca_stateLoc = ca_geolocator.geocode("California",timeout=5)
		#ca_stateLatLong = (ca_stateLoc.latitude, ca_stateLoc.longitude)
		#print("ca_stateLoc.address : {}".format(ca_stateLoc.address))
		
		#return
		
		threshold_dist = vincenty(srcLatLong, destLatLong).miles
		print('srcDest_distance of {} is {} miles'.format(cityPair, threshold_dist))
		cityTownMentions = set()
		otherMentions = set()
		otherMentionsDict = {}
		otherMentionsDict['srcLoc'] = srcLoc.address
		otherMentionsDict['destLoc'] = destLoc.address
		otherMentionsDict['mentions'] = {}
		with open(filePath) as data_file:    
			data = json.load(data_file)
			locationsParsed = (data['location_BlogUrls'].keys())
			all_locations_count = len(locationsParsed)
			print("No of locations Parsed : {}".format(all_locations_count))
			ignored_locations_count = 0
			print("Following location mentions are too far from src and destination, hence ignoring...")
			for location in locationsParsed:
				if location in citiesTowns:
					#print("citiesTowns found : ", location)
					cityTownMentions.add(location)
					ignored_locations_count += 1
				else:
					otherMentions.add(location)
					blogLinks = data['location_BlogUrls'][location]
					location = location.lower()
					mentionLoc = ca_geolocator.geocode(location,timeout=5)
					#print(location)
					#print(mentionLoc)
					if not mentionLoc:
						#print("invalid location : ", location)
						ignored_locations_count += 1
						continue
					mentionLatLong = (mentionLoc.latitude, mentionLoc.longitude)
					src_mentionDist = vincenty(srcLatLong, mentionLatLong).miles
					dest_mentionDist = vincenty(destLatLong, mentionLatLong).miles
					closest_to = []
					srcCloser = False
					destCloser = False
					#print(closest_to)
					if (src_mentionDist <= threshold_dist):
						srcCloser = True
						closest_to.append(src)
					if (dest_mentionDist <= threshold_dist):
						destCloser = True
						closest_to.append(dest)
					#print(closest_to)
					if srcCloser or destCloser:
						otherMentionsDict['mentions'][location] = dict(cityPair = [cityPair],
						address = mentionLoc.address,
						latitude = mentionLoc.latitude,
						longitude = mentionLoc.longitude,
						closest_to = closest_to,
						locType = mentionLoc.raw['type'],
						blogLinks = blogLinks)
						#print(location)
						#pprint(otherMentionsDict['mentions'])
					else:
						#print("\t\tthreshold_dist : {}".format(threshold_dist))
						#print("\t\tsrc_mentionDist : {}".format(src_mentionDist))
						#print("\t\tdest_mentionDist : {}".format(dest_mentionDist))
						#print("{} is too far from src and destination, hence ignoring....".format(mentionLoc))
						ignored_locations_count += 1
						print(mentionLoc)
			print("No of locations Ignored : {}".format(ignored_locations_count))
			print("Valid locations extracted : {}".format(all_locations_count-ignored_locations_count))
		#print(otherMentionsDict)
		with open('processed_output/' + fileName, 'w') as outfile:
		    json.dump(otherMentionsDict, outfile, indent=4)
		    print("Valid locations dumped to processed_output/{}".format(fileName))
	#pprint(otherMentionsDict, indent=4)

def main():
	parser = argparse.ArgumentParser(description="process List_of_cities_and_towns_in_California_wiki.txt dataset to get city and town names")
	parser.add_argument("path_blogLocation", help="path to blogLocation Jsons directory")
	parser.add_argument("cityTown_wikiFile", help="path to cityTown_wikiFile data")
	args = parser.parse_args()
	cityTown_wikiFile = args.cityTown_wikiFile
	path_blogLocation = args.path_blogLocation
	
	#print(srcDest_distance('kengeri bangalore', 'm.g road bangalore'))
	#return

	get_citiesTowns(cityTown_wikiFile)
	parseBlogLocations(path_blogLocation)

if __name__ == "__main__" : main()
