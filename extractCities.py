#ravirajukrishna@ubuntu:/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie$
#java -mx4g -cp "stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
#-- listing properties --
#Starting server on port 9000 with timeout of 5000 milliseconds.
#StanfordCoreNLPServer listening at /0:0:0:0:0:0:0:0:9000

#ON Installing GoogleScraper replace database.py in site-packages/GoogleScraper

import argparse, json, os
import urllib.request
from pprint import pprint
from itertools import combinations
from google import search
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from collections import deque
import nltk
import time

from GoogleScraper import scrape_with_config, GoogleSearchError

from corenlp_pywrap import pywrap
ner_annotator_list = ["pos", "ner"]
cn = pywrap.CoreNLP(url='http://localhost:9000', annotator_list=ner_annotator_list)

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
                if len(sentences) <= 1:#skip 1-word sentences having just location....outliers
                    continue
                for sent in sentences:
                    
                    #print(repr(sent))
                    
                    #nltk_blogLocations = package_get_entities(sent)                          

                    sent = str(sent.encode('utf-8'))
                    #print(sent)
                    try:
                        token_dict = cn.arrange(sent)
                        indexes = token_dict['index']
                        ner_set = set(token_dict['ner'])
                        for i in indexes:
                            j = int(i) -1
                            word = token_dict['originalText'][j]

                            if token_dict['ner'][j] in ("LOCATION",):
                                global location_queue
                                if token_dict['ner'][j-1] == "LOCATION":
                                    location_queue.append(word)
                                else:
                                    if len(location_queue) != 0:
                                        blogLocations.append(readLocEmptyQueue(src))
                                    location_queue.append(word)
                                #resultString = "{} {} {}".format(word, token_dict['pos'][j], token_dict['ner'][j])
                                #print(resultString)
                                
                    except UnicodeEncodeError as e:
                        print("ignore sentence : ", sent)
                        print(e)
                    except ValueError as e:
                        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
    noDup_blogLocations = list(set(blogLocations))
    
    #noDup_nltk_blogLocations = list(set(nltk_blogLocations))
    #all_locations = noDup_nltk_blogLocations + noDup_blogLocations
    #noDup_all_locations = list(set(all_locations))
    #print("NLTK found : {} locations : ".format(len(noDup_nltk_blogLocations)), end='')
    #print(noDup_nltk_blogLocations)
    #print("CoreNLP found : {} locations : ".format(len(noDup_blogLocations)), end='')
    #print(noDup_blogLocations)
    #print("Total found : {} locations : ".format(len(noDup_all_locations)), end='')
    #print(noDup_all_locations)
    #return noDup_all_locations
    
    return noDup_blogLocations#blogLocations

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
        
           
def main():
    parser = argparse.ArgumentParser(description="extract locations from blogs for given data")
    parser.add_argument("path", help="path to listOfCities json file")
    parser.add_argument("output_path", help="path to output")
    args = parser.parse_args()
    listOfCitiesPath = args.path
    output_path = args.output_path
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    process(output_path, listOfCitiesPath)
        
if __name__ == "__main__" : main()
