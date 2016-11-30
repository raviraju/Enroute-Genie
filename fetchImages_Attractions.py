#python fetchImages_Attractions.py fetchImages/AllAttractions.txt
    #1 Fetch images for Rock And Brews
    #2 Fetch images for Big Trees Trail
    #...
    #Results available at fetchImages/AllAttractions_withImages.json


#wc -l AllAttractions.txt 
#717 AllAttractions.txt

#>>> import json
#>>> fp = open('AllAttractions_withImages.json','r')
#>>> data = json.load(fp)
#>>> len(data.keys())
#718
#>>> 



import argparse, json, os
from imageFetch import fetchImages

def fetchImages_Attraction(fileName):
    attractionImgDict = {}
    places = []
    outputFileName = fileName.rstrip('.txt') + '_withImages.json'
    if os.path.isfile(outputFileName):
        with open(outputFileName, 'r') as tempFile:
            attractionImgDict = json.load(tempFile)
            print("Loaded existing results")
    with open(fileName, 'r') as infile:
        for line in infile:
            places.append(line.replace('\n',''))
    index = 1
    for place in places:
        print("{} Fetch images for {}".format(index, place))
        if os.path.isfile(outputFileName):
            with open(outputFileName, 'r') as tempFile:
                attractionImgDict = json.load(tempFile)
        if place not in attractionImgDict:
            imageUrls = fetchImages(place) 
            attractionImgDict[place] = imageUrls
            index += 1
            with open(outputFileName, 'w') as outfile:
                json.dump(attractionImgDict, outfile, indent=4)
    print("Results available at {}".format(outputFileName))

def main():
    parser = argparse.ArgumentParser(description="fetch images for the attractions given in a txt file")
    parser.add_argument("fileName", help="file having names of attractions")
    args = parser.parse_args()
    fileName = args.fileName

    fetchImages_Attraction(fileName)

if __name__ == "__main__" : main()
