#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ python youT
#ubeSearch.py data_record_linkage_csv/california/tripAdvisor_attraction_in.csv 0
#Fetch Links for : top attractions in San Francisco
#Fetch Links for : top attractions in Sausalito
#Fetch Links for : top attractions in Mill Valley
#Fetch Links for : top attractions in Muir Beach

import argparse, os, csv
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time

sleepTime = 1
DEVELOPER_KEY = "AIzaSyBoqWLNaeOfuchJdEHWCeK-kjalsZNHReY"
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

def fetchYouTubeUrls(csvFile, csvColumnNo):
    #search_prefix = "top attractions in "
    search_prefix = ""
    new_csvFile = csvFile.replace('.csv','_withYouTube.csv')
    with open(csvFile, 'r') as inFile:
        with open(new_csvFile, 'w') as outFile:
            csvWriter = csv.writer(outFile)
            try:
                rownum = 0
                reader = csv.reader(inFile)
                for row in reader:
                    if rownum == 0:
                        row.append('youTubeLinkIds')
                        csvWriter.writerow(row)
                        #print(row, file=outFile)
                    else:
                        videoIds = youtube_search(search_prefix + row[csvColumnNo]).rstrip(',')
                        row.append(videoIds)
                        #print(row)
                        csvWriter.writerow(row)
                    rownum += 1
            finally:
                inFile.close()
                outFile.close()
        
def main():
    parser = argparse.ArgumentParser(description="fetch youtube links for csv file REMEMBER to update search_prefix")
    parser.add_argument("csvFile", help="csvFile input")
    parser.add_argument("csvColumnNo", help="column no in csvFile to use as search term")
    args = parser.parse_args()
    csvFile = args.csvFile
    csvColumnNo = args.csvColumnNo

    fetchYouTubeUrls(csvFile, int(csvColumnNo))

if __name__ == "__main__" : main()
