import argparse, json, csv
from pprint import pprint

tripAdvisor_attractions_Dict = {}

def load_tripAdvisor_attractions_csvFile(tripAdvisor_attractions_csvFileName):
    with open(tripAdvisor_attractions_csvFileName, 'r') as tripAdvisor_attractions_csvFile:
        reader = csv.reader(tripAdvisor_attractions_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                location = row[0]
                tripAdvisor_attractions_Dict[location] = row
                pprint(tripAdvisor_attractions_Dict[location])
            else:
                header_row = row
            rownum += 1
    print("Read {} results from {}".format(len(tripAdvisor_attractions_Dict.keys()), tripAdvisor_attractions_csvFileName))

def main():
    parser = argparse.ArgumentParser(description="integrate data for enroute-genie mashup")
    parser.add_argument("tripAdvisor_attractions_csvFile", help="csvFile input tripAdvisor_attractions_with_LatLong_withYouTube")
    args = parser.parse_args()
    tripAdvisor_attractions_csvFileName = args.tripAdvisor_attractions_csvFile
    load_tripAdvisor_attractions_csvFile(tripAdvisor_attractions_csvFileName)
    
if __name__ == "__main__" : main()
