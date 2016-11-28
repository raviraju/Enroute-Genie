#python updateYouTubeLinks_TripAdvisorAttractions.py 
# /media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/data_record_linkage_csv/california/city_match/tripAdvisor_attractions_with_LatLong_withYouTube.csv 
# /media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/data_record_linkage_csv/california/city_match/tripAdvisor_attractions/


import argparse, json, csv, os
from pprint import pprint

tripAdvisor_attractions_YouTube_Dict = {}

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)
                
def load_tripAdvisor_attractions_csvFile(tripAdvisor_attractions_csvFileName):
    with open(tripAdvisor_attractions_csvFileName, 'r') as tripAdvisor_attractions_csvFile:
        reader = csv.reader(tripAdvisor_attractions_csvFile)
        rownum = 0
        for row in reader:
            if rownum != 0:
                location = row[0]
                tripAdvisor_attractions_YouTube_Dict[location] = row[12]
                #pprint(tripAdvisor_attractions_YouTube_Dict[location])
            else:
                header_row = row
            rownum += 1
    print("Read {} results from {}".format(len(tripAdvisor_attractions_YouTube_Dict.keys()), tripAdvisor_attractions_csvFileName))

def updateYouTubeLinks(tripAdvisor_attractions):
    count = 0
    for path,fileName in rscandir(tripAdvisor_attractions):
        filePath = os.path.join(path, fileName)
        count+=1
        print("Reading attractions from {} : {}".format(count, fileName))
        #updated_data = {}
        data = {}
        with open(filePath) as data_file:
            data = json.load(data_file)
            #pprint(data)
            #updated_data = data
            for attraction in data:
                youTubeIds = tripAdvisor_attractions_YouTube_Dict.get(attraction, "")
                data[attraction]["youTubeIds"] = youTubeIds
        with open(filePath,'w') as update_data_file:
            json.dump(data, update_data_file, indent=4)
        #return

def main():
    parser = argparse.ArgumentParser(description="integrate data for enroute-genie mashup")
    parser.add_argument("tripAdvisor_attractions_csvFile", help="csvFile input tripAdvisor_attractions_with_LatLong_withYouTube")
    parser.add_argument("tripAdvisor_attractions", help="path to tripAdvisor_attractions directory containing jsonFiles for each attraction_in")
    args = parser.parse_args()
    tripAdvisor_attractions_csvFileName = args.tripAdvisor_attractions_csvFile
    tripAdvisor_attractions = args.tripAdvisor_attractions
    load_tripAdvisor_attractions_csvFile(tripAdvisor_attractions_csvFileName)
    updateYouTubeLinks(tripAdvisor_attractions)
    
if __name__ == "__main__" : main()
