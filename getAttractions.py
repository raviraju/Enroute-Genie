#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ ls -ltr output_tripAdvisor_attractions_using_portia/california/
#total 164784
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 48338112 Nov  8 22:54 california_tripadvisor.csv
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 60196962 Nov  8 22:54 california_tripadvisor.json
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 60196961 Nov  8 22:54 california_tripadvisor.jl
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ python34 getAttractions.py output_tripAdvisor_attractions_using_portia/california/california_tripadvisor.jl output_tripAdvisor_attractions_using_portia/california/
#Found 5445 attractions in 682 places.
#Summary captured in : 
#tripAdvisor_attractions.csv & tripAdvisor_attraction_in.csv 
#attractionSummary.jl & attractionSummary.json 
#Attractions found in output_tripAdvisor_attractions_using_portia/california/tripAdvisor_attractions/
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ ls -ltr output_tripAdvisor_attractions_using_portia/california/total 220812
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 48338112 Nov  8 22:54 california_tripadvisor.csv
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 60196962 Nov  8 22:54 california_tripadvisor.json
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 60196961 Nov  8 22:54 california_tripadvisor.jl
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 33222757 Nov 11 21:08 attractions_Summary.jl
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 21702250 Nov 11 21:08 attractions_Summary.json
#drwxrwxrwx 1 ravirajukrishna ravirajukrishna      288 Nov 11 21:08 tripAdvisor_attractions
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna  2417754 Nov 11 21:08 tripAdvisor_attractions.csv
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna    18546 Nov 11 21:08 tripAdvisor_attraction_in.csv
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ 


#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ ls -ltr output_tripAdvisor_attractions_using_portia/karnataka/
#total 15988
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 5849879 Nov  7 10:38 karnataka_tripadvisor.jl
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 5849880 Nov  7 10:38 karnataka_tripadvisor.json
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 4661834 Nov  7 10:38 karnataka_tripadvisor.csv
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ python34 getAttractions.py output_tripAdvisor_attractions_using_portia/karnataka/karnataka_tripadvisor.jl output_tripAdvisor_attractions_using_portia/karnataka/
#Found 556 attractions in 66 places.
#Summary captured in : 
#tripAdvisor_attractions.csv & tripAdvisor_attraction_in.csv 
#attractionSummary.jl & attractionSummary.json 
#Attractions found in output_tripAdvisor_attractions_using_portia/karnataka/tripAdvisor_attractions/
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ ls -ltr output_tripAdvisor_attractions_using_portia/karnataka/total 22712
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 5849879 Nov  7 10:38 karnataka_tripadvisor.jl
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 5849880 Nov  7 10:38 karnataka_tripadvisor.json
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 4661834 Nov  7 10:38 karnataka_tripadvisor.csv
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 4024865 Nov 11 21:10 attractions_Summary.jl
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna 2612939 Nov 11 21:10 attractions_Summary.json
#drwxrwxrwx 1 ravirajukrishna ravirajukrishna     176 Nov 11 21:10 tripAdvisor_attractions
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna  239527 Nov 11 21:10 tripAdvisor_attractions.csv
#-rwxrwxrwx 1 ravirajukrishna ravirajukrishna    1728 Nov 11 21:10 tripAdvisor_attraction_in.csv
#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$ 

import json_lines, json, os, csv
import argparse 
#import pprint

attractionsDict = {}

def getAttractionFileName(attraction):
    return attraction.replace(' ','_').lower() + ".json"

def main():
    
    parser = argparse.ArgumentParser(description="Cleanup Json Lines file from scrapinghub")
    parser.add_argument("input_path", help="path to tripAdvisor.jl file from portia to cleanup")
    parser.add_argument("output_path", help="path where a directory of attractions will be extracted")
    args = parser.parse_args()
    tripAdvisorfilePath = args.input_path
    
    output_path = args.output_path + "tripAdvisor_attractions/"
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    csvFile_attractions = open(args.output_path + 'tripAdvisor_attractions.csv', 'w')
    csvWriter_attractions = csv.writer(csvFile_attractions)
                                    #attraction,        processedKnownFor,          reviewComment,          ranking,            no_of_reviews,                  contact,        attraction_in,      address,            url ,           getAttractionFileName(attraction_in)
    csvWriter_attractions.writerow(["attraction_name","attraction_knownFor", "attraction_reviewComment", "attraction_ranking", "attraction_no_of_reviews", "attraction_contact","attraction_in", "attraction_address","attraction_url", "attraction_in_file"])
    
    csvFile_attraction_in = open(args.output_path + 'tripAdvisor_attraction_in.csv', 'w')
    csvWriter_attraction_in = csv.writer(csvFile_attraction_in)
                                    #attraction_in,      getAttractionFileName(attraction_in)
    csvWriter_attraction_in.writerow(["attraction_in", "attraction_in_file"])

    
    
    with open(args.output_path + 'attractions_Summary.jl', 'w') as outfile:
        with open(tripAdvisorfilePath, encoding='utf8') as infile:
            for item in json_lines.reader(infile):
                if 'attraction_in' in item.keys():
                    thing = item['attraction_in'][0]
                    if not thing:#None
                        continue
                    attraction_in = thing
                    
                    url = item.get('url',None)
                    if not url:#None
                        continue
                        
                    reviewCommentList = item.get('reviewComment',None)
                    reviewComment = ""
                    if reviewCommentList:
                        reviewComment = reviewCommentList[0]
                    
                    processedDict = {}
                    processedDict['attraction_in'] = attraction_in
                    
                    if not attraction_in in attractionsDict:
                        attractionsDict[attraction_in] = {}
                        csvWriter_attraction_in.writerow([attraction_in, getAttractionFileName(attraction_in)])
                        
                    knownForList = item.get('knownFor',None)
                    processedKnownFor = ""
                    if knownForList:
                        knownFor = knownForList[0]
                        processedKnownFor = (knownFor.split("As featured in")[0])
                        processedDict['knownFor'] = processedKnownFor

                    addressList = item.get('address',None)
                    address = ""
                    if addressList:
                        address = addressList[0]
                        processedDict['address'] = address
                    
                    rankingList = item.get('ranking',None)
                    ranking = ""
                    if rankingList:
                        ranking = rankingList[0].strip('#')
                        processedDict['rank'] = ranking

                    no_of_reviewsList = item.get('no_of_reviews',None)
                    no_of_reviews = ""
                    if no_of_reviewsList:
                        no_of_reviews = no_of_reviewsList[0]
                        processedDict['no_of_reviews'] = no_of_reviews
                        
                    contactList = item.get('contact',None)
                    contact = ""
                    if contactList:
                        contact = contactList[0]
                        #print(contact)
                        #print("\t", contact.replace('-','').replace('1-','').replace(' ','').replace('\)',''))
                        processedDict['contact'] = contact
                        
                    attractionList = item.get('attraction',None)
                    if attractionList:
                        attraction = attractionList[0]
                        processedDict['attraction'] = attraction
                        if not attraction in attractionsDict[attraction_in]:
                            attractionsDict[attraction_in][attraction] = {}
                            csvWriter_attractions.writerow([attraction,processedKnownFor, reviewComment, ranking, no_of_reviews, contact, attraction_in, address, url , getAttractionFileName(attraction_in)])
                            
                    attractionsDict[attraction_in][attraction]['knownFor'] = processedKnownFor
                    attractionsDict[attraction_in][attraction]['address'] = address
                    attractionsDict[attraction_in][attraction]['rank'] = ranking
                    attractionsDict[attraction_in][attraction]['no_of_reviews'] = no_of_reviews
                    attractionsDict[attraction_in][attraction]['contact'] = contact

                    processedDict['url'] = url
                    #attractionsDict[attraction_in][attraction]['url'] = url
                    if 'urls' in attractionsDict[attraction_in][attraction]:
                        attractionsDict[attraction_in][attraction]['urls'].append(url)
                    else:
                        attractionsDict[attraction_in][attraction]['urls'] = [url]


                    processedDict['reviewComment'] = reviewComment
                    if 'reviewComments' in attractionsDict[attraction_in][attraction]:
                        attractionsDict[attraction_in][attraction]['reviewComments'].append(reviewComment)
                    else:
                        attractionsDict[attraction_in][attraction]['reviewComments'] = [reviewComment]
                        
                    json.dump(processedDict, outfile)
                    print(file=outfile)    
    with open(args.output_path + 'attractions_Summary.json', 'w') as outfile:
        json.dump(attractionsDict, outfile, indent=4)
    total_no_of_attractions = 0
    for attraction in attractionsDict:
        fileName = getAttractionFileName(attraction) #attraction.replace(' ','_').lower() + ".json"
        total_no_of_attractions += len(attractionsDict[attraction].keys())
        with open(output_path + fileName, 'w') as outfile:
            json.dump(attractionsDict[attraction], outfile, indent=4)
    print("Found {} attractions in {} places.\nSummary captured in : \ntripAdvisor_attractions.csv & tripAdvisor_attraction_in.csv \nattractionSummary.jl & attractionSummary.json \nAttractions found in {}".format(total_no_of_attractions, len(attractionsDict.keys()), output_path))

if __name__ == "__main__" : main()
