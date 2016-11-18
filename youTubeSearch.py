#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ python youT
#ubeSearch.py data_record_linkage_csv/california/tripAdvisor_attraction_in.csv 0
#Fetch Links for : top attractions in San Francisco
#Fetch Links for : top attractions in Sausalito
#Fetch Links for : top attractions in Mill Valley
#Fetch Links for : top attractions in Muir Beach

#python youTubeSearch.py data_record_linkage_csv/california/tripAdvisor_attractions.csv 0 -l data_record_linkage_csv/california/tripAdvisor_attractions_withYouTube_1.csv 

import argparse, os, csv
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time

sleepTime = 1
DEVELOPER_KEY_USC = "AIzaSyBoqWLNaeOfuchJdEHWCeK-kjalsZNHReY"
DEVELOPER_KEY = "AIzaSyC9K8dkuC8DjWvUIpazNxlSBVZRCL1iWik"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    print("Fetch Links for : {}".format(query))
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
                                            q=query,
                                            part="id,snippet",
                                            maxResults="3"
                                            ).execute()



    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    #youTube_urls = []
    #youTube_urls = ""
    youTube_ids = ""
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videoID = search_result["id"]["videoId"]
            #url = "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
            #print(url)
            #youTube_urls.append(url)
            #youTube_urls += url + "|"
            youTube_ids += videoID + ","
    #print("Sleeping for {}".format(sleepTime))
    #print("Sleeping for {}".format(sleepTime))
    time.sleep(sleepTime)
    return youTube_ids#youTube_urls

#youTube_urls = youtube_search("San Francisco")
#print(youTube_urls)

def fetchYouTubeUrls(csvFile, outFile, csvColumnNo, availLocationData):
    #search_prefix = "top attractions in "
    search_prefix = ""
    
    knownResults = 0
    resultsToBeKnown = 0
    with open(csvFile, 'r') as inFile:
        #with open(new_csvFile, 'w') as outFile:
        csvWriter = csv.writer(outFile)
        try:
            rownum = 0
            reader = csv.reader(inFile)
            for row in reader:
                if rownum == 0:
                    if not availLocationData:
                        row.append('youTubeLinkIds')
                        csvWriter.writerow(row)
                else:
                    location = row[csvColumnNo]
                    if location in availLocationData:
                        #print("Skip youtube_search for {}".format(location))
                        #print(availLocationData[location])
                        knownResults += 1
                    else:
                        #print("Youtube_search for {}".format(location))
                        resultsToBeKnown += 1
                        videoIds = youtube_search(search_prefix + location).rstrip(',')
                        row.append(videoIds)
                        ##print(row)
                        csvWriter.writerow(row)
                rownum += 1
        finally:
            inFile.close()
            outFile.close()
    print("knownResults : {}".format(knownResults))
    print("resultsToBeKnown : {}".format(resultsToBeKnown))
        
def main():
    parser = argparse.ArgumentParser(description="fetch youtube links for csv file REMEMBER to update search_prefix")
    parser.add_argument("csvFile", help="csvFile input")
    parser.add_argument("csvColumnNo", help="column no in csvFile to use as search term")
    parser.add_argument("-l", "--load",   help="csvFile which has partial results")
    args = parser.parse_args()
    csvFile = args.csvFile
    csvColumnNo = int(args.csvColumnNo)
    availLocationData = {}
    new_csvFile = csvFile.replace('.csv','_withYouTube.csv')
    header_row = ""
    if args.load:
        partialResultsFileName = args.load
        print("Loading Results from : {}".format(partialResultsFileName))
        with open(partialResultsFileName, 'r') as partialResultsFile:
            reader = csv.reader(partialResultsFile)
            rownum = 0
            for row in reader:
                if rownum != 0:
                    #print(row[csvColumnNo])
                    location = row[csvColumnNo]
                    availLocationData[location] = row
                else:
                    header_row = row
                rownum += 1
        print("Read {} results from {}".format(len(availLocationData.keys()), partialResultsFileName))
    output_csvFile = None
    with open(new_csvFile, 'w') as output_csvFile:
        if availLocationData:
            csvWriter = csv.writer(output_csvFile)
            csvWriter.writerow(header_row)
            print("Writing available Locations DataSet to : {}".format(new_csvFile))
            for location,data in availLocationData.items():
                csvWriter.writerow(data)
        fetchYouTubeUrls(csvFile, output_csvFile, csvColumnNo, availLocationData)

if __name__ == "__main__" : main()
