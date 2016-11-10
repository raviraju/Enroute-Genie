import argparse, os, json
from pprint import pprint
#http://geopy.readthedocs.io/en/latest/
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.exc import GeocoderServiceError
import time
from urllib.error import HTTPError
#NOTE : create folders geoCodeLocations_output/ and geoCodeIgnoredLocations_output/, with state value updated
citiesTowns = set()
ca_geolocator = Nominatim()
no_retry_attempt = 0
max_retry_attempts = 3

output_dir = 'geoCodeLocations_output/'
outputIgnore_dir = 'geoCodeIgnoredLocations_output/'
state = 'california'
sleepTime = 1

cachedGeoDataDict = {}
no_of_saved_calls = 0

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
    return os.path.isfile(output_dir + keyFileName) 

def do_geocode(address):
	global no_retry_attempt, max_retry_attempts
	try:
		geoCodeObj = ca_geolocator.geocode(address,timeout=20)
		no_retry_attempt = 0
		return geoCodeObj
	except TimeOut:
		no_retry_attempt += 1
		if no_retry_attempt > max_retry_attempts:
			raise TimeOut
		else:
			return do_geocode(address)

def getGeoCodeDict(location):
	global no_of_saved_calls
	geoData = None
	if location in cachedGeoDataDict:
		no_of_saved_calls +=1
		print("Found {} in cache, Saved {} call".format(location, no_of_saved_calls))
		geoData = cachedGeoDataDict[location]
	else:
		time.sleep(sleepTime)
		try:
			geoDataObj = ca_geolocator.geocode(location + ', ' + state,timeout=20)
			if geoDataObj:
				cachedGeoDataDict[location] = geoDataObj.raw
				geoData = cachedGeoDataDict[location]
		except (ValueError, GeocoderServiceError):
			return None
	return geoData

def parseBlogLocations(path_blogLocation):
	for path,fileName in rscandir(path_blogLocation):
		try:
			filePath = os.path.join(path, fileName)
			print("\nReading locations from {}".format(fileName))
			cityPairCand = fileName.split('_and_')
			cityPair = (cityPairCand[0], cityPairCand[1].rstrip('json').replace('.',''))
			#dist = srcDest_distance(cityPair[0], cityPair[1])
			src = cityPair[0]
			dest = cityPair[1]
			if comboResultsKnown(fileName):
				print("Combo {},{} was already captured results in : {}{}".format(src, dest, output_dir, fileName))
				continue
			
			srcLocDict   = getGeoCodeDict(src)#ca_geolocator.geocode(src + ', California',timeout=5)
			destLocDict  = getGeoCodeDict(dest)#ca_geolocator.geocode(dest+ ', California',timeout=5)
			if not srcLocDict:
				print("Unable to locate src : {}".format(src))
				continue
			if not destLocDict:
				print("Unable to locate dest : {}".format(dest))
				continue
			print("srcLocDict['display_name'] : {}".format(srcLocDict['display_name']))
			print("destLocDict['display_name'] : {}".format(destLocDict['display_name']))
			srcLatLong = (srcLocDict['lat'], srcLocDict['lon'])
			destLatLong = (destLocDict['lat'], destLocDict['lon'])
			
			threshold_dist = vincenty(srcLatLong, destLatLong).miles
			print('srcDest_distance of {} is {} miles'.format(cityPair, threshold_dist))
			mentionsDict = {}
			mentionsDict[src] = srcLocDict
			mentionsDict[dest] = destLocDict
			mentionsDict['mentions'] = {}
			ignored_mentionsDict = {}
			ignored_mentionsDict[src] = srcLocDict
			ignored_mentionsDict[dest] = destLocDict
			ignored_mentionsDict['mentions'] = {}
			with open(filePath) as data_file:    
				data = json.load(data_file)
				locationsParsed = (data['location_BlogUrls'].keys())
				all_locations_count = len(locationsParsed)
				print("No of locations Parsed : {}".format(all_locations_count))
				ignored_locations_count = 0
				print("Following location mentions are too far from src and destination, hence ignoring...")
				for location in locationsParsed:
					blogLinks = data['location_BlogUrls'][location]
					location = location.lower()
					mentionLocDict = getGeoCodeDict(location)#ca_geolocator.geocode(location,timeout=5)
					#print(location)
					#print(mentionLoc)
					if not mentionLocDict:
						#print("invalid location : ", location)
						ignored_locations_count += 1
						continue
					mentionLatLong = (mentionLocDict['lat'], mentionLocDict['lon'])
					src_mentionDist = vincenty(srcLatLong, mentionLatLong).miles
					dest_mentionDist = vincenty(destLatLong, mentionLatLong).miles
					closest_to = ""
					srcCloser = False
					destCloser = False
					#print(closest_to)
					if (src_mentionDist <= threshold_dist):
						srcCloser = True
						closest_to = src
					if (dest_mentionDist <= threshold_dist):
						destCloser = True
						closest_to = dest
					#print(closest_to)
					locationMentionDict = dict(
											address = mentionLocDict['display_name'],
											latitude = mentionLocDict['lat'],
											longitude = mentionLocDict['lon'],
											closest_to = closest_to,
											locType = mentionLocDict['type'],
											blogLinks = blogLinks)
					if srcCloser or destCloser:
						mentionsDict['mentions'][location] = locationMentionDict
					else:
						#print("\t\tthreshold_dist : {}".format(threshold_dist))
						#print("\t\tsrc_mentionDist : {}".format(src_mentionDist))
						#print("\t\tdest_mentionDist : {}".format(dest_mentionDist))
						ignored_locations_count += 1
						ignored_mentionsDict['mentions'][location] = locationMentionDict
						print(location)
				print("No of locations Ignored : {}".format(ignored_locations_count))
				print("Valid locations extracted : {}".format(all_locations_count-ignored_locations_count))
			#print(mentionsDict)
			with open(output_dir + fileName, 'w') as outfile:
				json.dump(mentionsDict, outfile, indent=4)
				print("Valid locations dumped to {}{}".format(output_dir,fileName))
			with open(outputIgnore_dir + fileName, 'w') as outfile:
				json.dump(ignored_mentionsDict, outfile, indent=4)
				print("Ignored locations dumped to {}{}".format(outputIgnore_dir,fileName))
		except ValueError as e:
			print(e)
			print("Hence Ignoring {}".format(fileName))
			continue

def main():
	parser = argparse.ArgumentParser(description="get geoCode for location mentions extracted from blogs and filter out distant/irrelavant location_mentions")
	parser.add_argument("path_blogLocation", help="path to blogLocation Jsons directory")
	parser.add_argument("state_name", help="name of the state(ex : california, karnataka...)")
	args = parser.parse_args()
	path_blogLocation = args.path_blogLocation
	global state
	state = args.state_name
	global cachedGeoDataDict
	if os.path.isfile('cachedGeoData.json'):
		with open('cachedGeoData.json', 'r') as cache_infile:
			print("Loaded cachedGeoDataDict")
			cachedGeoDataDict = json.load(cache_infile)
	else:
		with open('cachedGeoData.json', 'w') as cache_outfile:
			cachedGeoDataDict = {}
			json.dump(cachedGeoDataDict,cache_outfile)
			print("Initialized cachedGeoDataDict")
			
	try:
		parseBlogLocations(path_blogLocation)
	except HTTPError as e:
		content = e.read()
	finally:
		with open('cachedGeoData.json', 'w') as outfile:
			json.dump(cachedGeoDataDict, outfile, indent=4)
			print("cachedGeoData dumped to cachedGeoData.json")

if __name__ == "__main__" : main()
