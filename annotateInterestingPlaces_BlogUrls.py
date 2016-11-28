import argparse, json, os
import urllib.request
from pprint import pprint
from itertools import combinations
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from collections import deque
import time
import nltk


location_queue = deque()
all_locations = set()
all_loc_data = {}

sleepTime = 20

def readLocEmptyQueue(src):
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
    global location_queue
    #print(repr(location_queue))
    location = ""
    while(len(location_queue) != 0):
        location = location + location_queue.popleft() + " "
    location = location.strip()
    global all_locations
    all_locations.add(location)
    sources = all_loc_data.get(location, None)
    if not sources:
        all_loc_data[location] = set([src])
    else:
        all_loc_data[location].add(src)
    location_queue = deque()
    return location

def fetchBlogUrls(city_a, city_b):
    print('\n\nSleeping for {} sec...'.format(sleepTime))
    time.sleep(sleepTime)
    query = 'places to visit between '  + city_a  + ' and '  + city_b + ' blogs'
    print('fetching : ' + query + '...')
    
    config = {
        'use_own_ip': True,
        'keyword': query,
        'search_engines': ['bing'],
        'num_pages_for_keyword': 2,
        'scrape_method': 'selenium',
        'sel_browser': 'chrome',
        'do_caching': False,
        'log_level': 'CRITICAL',
        'print_results': 'summary',
        'output_format': ''
    }
    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

    urls = []
    #pprint(search)
    for serp in search.serps:
        for link in serp.links:
            print(link.getLink())
            urls.append(link.getLink())

    #pauseInterval = random.uniform(1, 20)
    #print(pauseInterval)
    #urls = search(query, stop=20, pause=pauseInterval)#last result to retrieve
    #return urls
    #sources = [
			#"http://kskrishnan.blogspot.com/2010/09/bangalore-to-mysore.html",
			#"https://www.makemytrip.com/blog/mysore-tales-1-making-way-to-mysores-hotspots",
			#"http://rajivc-food-travel-life.blogspot.com/2015/05/trip-to-gods-own-country-bangalore-to.html"
              #]
    #ca_sources = [
        #"https://www.tripline.net/trip/San_Francisco_to_San_Diego_on_the_PCH-7521703244561003A0278A25A729E901",
        #"https://www.gapyear.com/articles/216212/13-incredible-stops-on-the-pacific-coast-highway",
        #"http://moon.com/2015/08/road-trip-itinerary-san-diego-to-san-francisco-in-two-days/",
        #"http://moon.com/2016/05/take-a-two-week-california-coast-road-trip/",
        #"http://californiathroughmylens.com/pacific-coast-highway-stops",
        #"http://californiathroughmylens.com/san-francisco-mendocino-guide",
        #"http://www.heleninwonderlust.co.uk/2014/03/ultimate-california-road-trip-itinerary-las-vegas/",
        #"http://www.worldofwanderlust.com/where-to-stop-on-the-pacific-coast-highway/",
        #"http://www.visitcalifornia.com/trip/highway-one-classic",
        #"http://independenttravelcats.com/2015/11/24/planning-a-california-pacific-coast-highway-road-trip-from-san-francisco-to-los-angeles/"
        #]
    #ca_sources1 = [
        #"https://www.tripline.net/trip/San_Francisco_to_San_Diego_on_the_PCH-7521703244561003A0278A25A729E901",
        #"https://www.gapyear.com/articles/216212/13-incredible-stops-on-the-pacific-coast-highway"]
    #print(urls)
    return urls
    
def package_get_entities(text):
    #text = text[0:300]
    entity_names = []
    chunked = get_chunked_sentences(text)
    for tree in chunked:
        entity_names.extend(extract_entity_names(tree))
    entity_names = list(set(entity_names))
    return entity_names

def get_chunked_sentences(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    return chunked_sentences

def extract_entity_names(t):
    entity_names = []
    #print(t)
    if hasattr(t, 'label'):
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    return entity_names
    

def parseBlog(src):
    print("Extracting locations from : ", src)
    nltk_blogLocations = []
    blogLocations = []
    try:
        req=urllib.request.urlopen(src)
        charset=req.info().get_content_charset()
        page=req.read().decode(charset)

        soup = BeautifulSoup(page , "html.parser")
        
        #get rid of script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        
        #break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        for chunk in chunks:
            if chunk:
                sentences = nltk.sent_tokenize(chunk)
                #if len(sentences) <= 1:#skip 1-word sentences having just location....outliers
                #    continue
                for sent in sentences:
                    sent = str(sent.encode('utf-8'))
                    print(sent)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)

def comboResultsKnown(output_path, keyFileName):
    return os.path.isfile(output_path + keyFileName) 

def process(output_path, listOfCitiesPath):
    cities = set()
    with open(listOfCitiesPath) as json_data:
        listOfCities = json.load(json_data)
        cities = set(listOfCities)
    print("No of Cities : {} \nCities : {}".format(len(cities), cities))
    #srcDestBlogUrlsDict = {}
    comboCount = 0
    for combo in (combinations(cities,2)):
        #print(combo)
        city_a = combo[0].lower()
        city_b = combo[1].lower()
        if city_a < city_b:
            key = city_a + '_and_' + city_b
        else:
            key = city_b + '_and_' + city_a
        keyFileName = key + '.json'
        if comboResultsKnown(output_path, keyFileName):
            print("Combo {} was already captured results in : {}{}".format(key, output_path,  keyFileName))
            continue
        global all_loc_data
        all_loc_data = {}
        blogUrls = fetchBlogUrls(combo[0], combo[1])
        #urlList = []
        urlDict = {}
        for blogUrl in blogUrls:
            try:
                blogLocationsSet = set(parseBlog(blogUrl))
                blogLocationsList = list(blogLocationsSet)
                if len(blogLocationsList)>0:
                    urlDict[blogUrl] = blogLocationsList
                #urlList.append(blogUrl)
            except HTTPError as e:
                print("unable to parse src : {} due to {}".format(blogUrl,e))
            except TypeError as e:
                print("unable to parse src : {} due to {}".format(blogUrl,e))
        srcDestBlogUrlsDict = {}
        #srcDestBlogUrlsDict[key] = {}
        #srcDestBlogUrlsDict[key]['blogUrl_Locations'] = urlDict
        srcDestBlogUrlsDict['blogUrl_Locations'] = urlDict
        locationsDict = {}#to convert set of urls to list
        for loc,sources in all_loc_data.items():
            locationsDict[loc] = list(sources)
        #srcDestBlogUrlsDict[key]['location_BlogUrls'] = locationsDict
        srcDestBlogUrlsDict['location_BlogUrls'] = locationsDict
        with open(output_path + keyFileName, 'w') as outfile:
            #json.dump(srcDestBlogUrlsDict[key], outfile, indent=4)
            json.dump(srcDestBlogUrlsDict, outfile, indent=4)
        comboCount += 1
        print("Combo {} : {} Captured results into : {}{}.json".format(comboCount, key, output_path, key))
            
        #pprint(srcDestBlogUrlsDict, indent=4)

    #with open('srcDestBlogUrls.json', 'w') as outfile:
    #        json.dump(srcDestBlogUrlsDict, outfile, indent=4)

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)


def annotateBlog(src):
    print("********************************************************************")
    print("Annotate interesting locations from blog : ", src)
    cityLocations = set()
    mentionLocations = set()
    try:
        req=urllib.request.urlopen(src)
        charset=req.info().get_content_charset()
        page=req.read().decode(charset)

        soup = BeautifulSoup(page , "html.parser")
        
        #get rid of script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        
        #break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        for chunk in chunks:
            if chunk:
                sentences = nltk.sent_tokenize(chunk)
                if len(sentences) <= 1:#skip 1-word sentences having just location....outliers
                    continue
                for sent in sentences:
                    #sent = str(sent.encode('utf-8'))
                    print(sent)
                    choice = input("Do u want to annotate (y/n) : ")
                    if choice == 'y':
                        #continueAdd = 'y'
                        while (input("Do u wish to add locations(y/n) : ") == 'y'):
                            location = input("Select the location u wish to annotate : \n")
                            isCity = input("Is it a city?(y/n)")
                            if isCity == 'y':
                                cityLocations.add(location)
                            else:
                                mentionLocations.add(location)
        return (cityLocations, mentionLocations)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)

def annotate(annotate_input_path, annotated_output_path):
    for path,fileName in rscandir(annotate_input_path):
        filePath = os.path.join(path, fileName)
        print("\nReading blogUrls from {}".format(fileName))
        allAnnotatedData = {}
        allAnnotatedData["cities"] = list()
        allAnnotatedData["attractions"] = list()
        allAnnotatedData["urlDetails"] = list()
        with open(filePath, 'r') as blogUrlsFile:
            data = json.load(blogUrlsFile)
            blogUrls = data["blogUrl_Locations"].keys()
            #print(blogUrls)
            for blogUrl in blogUrls:
                #print(blogUrl)
                if input("Do u wish to annotate the blog {} (y/n)\n".format(blogUrl)) == 'y':
                    cityLocationsList = []
                    mentionLocationsList = []
                    (cityLocations, mentionLocations) = annotateBlog(blogUrl)
                    if cityLocations:
                        cityLocationsList = list(cityLocations)
                        allAnnotatedData["cities"].extend(cityLocationsList)
                    if mentionLocations:
                        mentionLocationsList = list(mentionLocations)
                        allAnnotatedData["attractions"].extend(mentionLocationsList)
                    urlDict = {"url" : blogUrl, "cities" : cityLocationsList, "attractions" : mentionLocationsList}
                    allAnnotatedData["urlDetails"].append(urlDict)
                    pprint(urlDict)
                else:
                    print("Skipping...")
        #pprint(allAnnotatedData)
        with open(annotated_output_path + fileName, 'w') as annotated_outputFile:
            json.dump(allAnnotatedData, annotated_outputFile, indent = 4)
        print("Annotated data is available at {}".format(annotated_output_path + fileName))

#python3 annotateInterestingPlaces_BlogUrls.py annotate_input_data/ annotated_output_data/
def main():
    parser = argparse.ArgumentParser(description="annotate interesting locations from blogsUrls into city/attraction interest")
    parser.add_argument("annotate_input_path", help="path to set of city_pair blogLinks json file")#annotate_input_data/
    parser.add_argument("annotated_output_path", help="path of output to store annotated places")#annotated_output_data/
    args = parser.parse_args()
    annotate_input_path = args.annotate_input_path
    annotated_output_path = args.annotated_output_path
    
    if not os.path.exists(annotated_output_path):
        os.makedirs(annotated_output_path)
    annotate(annotate_input_path, annotated_output_path)
        
if __name__ == "__main__" : main()
