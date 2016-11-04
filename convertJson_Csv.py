import argparse, os, json, csv
from pprint import pprint

#employee_parsed = json.loads(employee_data)

#emp_data = employee_parsed['employee_details']

## open a file for writing

#employ_data = open('/tmp/EmployData.csv', 'w')

## create the csv writer object

#csvwriter = csv.writer(employ_data)

#count = 0

#for emp in emp_data:

      #if count == 0:

             #header = emp.keys()

             #csvwriter.writerow(header)

             #count += 1

      #csvwriter.writerow(emp.values())

#employ_data.close()

def rscandir(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.json'):
				yield (root, file)

def convertToCSV(path_processedLocation):
	csvFile = open('csvResults.csv', 'w')
	csvWriter = csv.writer(csvFile)
	csvWriter.writerow(["name","locType", "longitude", "latitude", "closest_to", "blogLinks", "src", "dest", "address", "srcLoc", "destLoc"])
	for path,fileName in rscandir(path_processedLocation):
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
	parser = argparse.ArgumentParser(description="convert processed locations from json to csv")
	parser.add_argument("path_processedLocation", help="path to processed_locations Jsons directory")
	args = parser.parse_args()
	path_processedLocation = args.path_processedLocation

	convertToCSV(path_processedLocation)

if __name__ == "__main__" : main()
