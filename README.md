![Enroute Genie](https://github.com/raviraju/Enroute-Genie/blob/master/Capture.PNG "Enroute Genie")
## Statistics of Results
```
blogs_using_NER
    164260 : No of locations Parsed in output_candidate_location_from_blogs_using_NER/california/
    16453  : No of unique locations Parsed in output_candidate_location_from_blogs_using_NER/california/
geoCoded_locations
    94916 : No of locations Parsed in output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/
    7951  : No of unique locations Parsed in output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/

176 No of locations Parsed in merge_data/geoCodeLocations_output/los angeles_and_san francisco.json
    41    : No of Cities
    6     : No of Enriched Cities

    135   : No of NonCities
    22    : No of Enriched NonCities

**Summary** :
    94916 : No of locations Parsed in merge_data/geoCodeLocations_output/
    21820 : No of cities in merge_data/geoCodeLocations_output/
    73096 : No of noncities in merge_data/geoCodeLocations_output/

    7951  : No of unique locations
    79    : No of unique enriched cities
    477   : No of unique non_enriched cities
    517   : No of unique enriched noncities
    6878  : No of unique non_enriched noncities
```

## Project Source Code
1. **[extractCities.py](src/extractCities.py)** : extract NER locations from blogs for every pair of popular destinations 
   + read **input/california.json** - collection of destinations from Google results of query : https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=popular+cities+in+california
   ```
   ["Anaheim", "Avalon", "Bakersfield", "Berkeley", "Beverly Hills", "Big Bear Lake", "Carlsbad", "Fresno", "Fremont", ...]
   ```
   + for every pair of destinations the query : 'places to visit between '  + city_a  + ' and '  + city_b + ' blogs' result links collected using [GoogleScraper](https://github.com/NikolaiT/GoogleScraper)
   + for every bloglink content was extracted using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
   + extracted text content was tagged with NER LOCATION using [StandfordCoreNLP](https://github.com/hhsecond/corenlp_pywrap)
   + output were recorded into json files for a pair city_a  + '_and_'  + city_b + '.json', 
    these can be found in **data/output_candidate_location_from_blogs_using_NER/california/**
    ```
    ***data/output_candidate_location_from_blogs_using_NER/california/los angeles_and_san francisco.json***
    
    "location_BlogUrls": {
        "San Francisco Bay": [
            "http://gocalifornia.about.com/od/topcalifornia/ss/los-angeles-to-san-francisco.htm",
            "https://www.quora.com/Is-there-anything-interesting-to-see-on-the-drive-along-Interstate-5-between-San-Francisco-and-Los-Angeles"
        ],
        "New Zealand": [
            "http://www.trippy.com/question/California-Where-to-stay-half-way-between-S-F--and-L-A"
        ],....
    }
    ```

2. **[geoCodeLocations.py](src/geoCodeLocations.py)** : get [geoCode](http://geopy.readthedocs.io/en/latest/) for location mentions extracted from blogs and filter out distant/irrelavant location_mentions
    + read **data/output_candidate_location_from_blogs_using_NER/california/**
    ```
    ***output_candidate_location_from_blogs_using_NER/california/los angeles_and_san francisco.json***
    "location_BlogUrls": {
        "San Francisco Bay": [
            "http://gocalifornia.about.com/od/topcalifornia/ss/los-angeles-to-san-francisco.htm",
            "https://www.quora.com/Is-there-anything-interesting-to-see-on-the-drive-along-Interstate-5-between-San-Francisco-and-Los-Angeles"
        ],
        "New Zealand": [
            "http://www.trippy.com/question/California-Where-to-stay-half-way-between-S-F--and-L-A"
        ],....
    }
    ```
    + get geoCode for src and destination from fileName format 'cityA' + '_and_' + 'cityB' + '.json'
    + for each location mention find its distance from source and destination, if its distance is within distance bw src and destination, retain them into **geoCodeLocations_output/** else discard them into **geoCodeIgnoredLocations_output/**
    + output can be found in **data/output_geoCoded_locations_from_blogs_using_geopy_json/california/**
    ```
    ***data/output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/los angeles_and_san francisco.json***
    "san francisco bay": {
            "latitude": "37.708264",
            "closest_to": "san francisco",
            "address": "San Francisco Bay, Ferry Landing, Alameda, Alameda County, California, 94502, United States of America",
            "locType": "bay",
            "blogLinks": [
                "http://gocalifornia.about.com/od/topcalifornia/ss/los-angeles-to-san-francisco.htm",
                "https://www.quora.com/Is-there-anything-interesting-to-see-on-the-drive-along-Interstate-5-between-San-Francisco-and-Los-Angeles"
            ],
            "longitude": "-122.2802469"
        },
    ```
    
    ```
    ***data/output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeIgnoredLocations_output/los angeles_and_san francisco.json***
        "new zealand": {
            "latitude": "-41.1069272",
            "closest_to": "",
            "address": "California Drive, Totara Park, Upper Hutt, Upper Hutt City, Wellington, 5371, New Zealand/Aotearoa",
            "locType": "tertiary",
            "blogLinks": [
                "http://www.trippy.com/question/California-Where-to-stay-half-way-between-S-F--and-L-A"
            ],
            "longitude": "175.0832904"
        },
    ```
    
3. **[convertBlogLoctionMentionsJson_Csv.py](src/convertBlogLoctionMentionsJson_Csv.py)** : convert geoCoded relevant location mentions of blogs from json to csv, so as to be used for record linkage
    + produce 3 csv : allBlogLocationMentions.csv, allBlogLocation_City_Mentions.csv and allBlogLocation_nonCity_Mentions.csv
      which can be used to perform record linkage for city mention or non-city(actual attraction) abstraction level with trip advisor data
    + output can be found in **data/output_geoCoded_locations_from_blogs_using_geopy_csv/california/**
    ```
    san francisco bay,bay,68,"San Francisco Bay, Ferry Landing, Alameda, Alameda County, California, 94502, United States of America",-122.2802469,37.708264,232,"anaheim_and_berkeley.json,anaheim_and_fremont.json,anaheim_and_fresno,...,sausalito_and_stockton.json"
    ```

4. Configured an Instance-Based Data extraction wrapper to extract attraction reviews metadata from www.tripadvisor.com
   + **[Portia](https://www.zyte.com/blog/scrapely-the-brains-behind-portia-spiders/)** - A [visual web scraping tool](https://github.com/scrapinghub/portia) was used to extract data
       + Portia uses Scrapely to extract structured data from HTML pages.
       + To extract data, Portia employs machine learning using the [instance-based wrapper induction extraction](https://www.semanticscholar.org/paper/Extracting-Web-Data-Using-Instance-Based-Learning-Zhai-Liu/10b9fa968dd9cfbdf967ecfac676e8d77e1ca13d) method implemented by Scrapely.
           + [Extracting Web Data Using Instance-Based Learning](documentation/Extracting_Web_Data_Using_Instance-Based_Learning.pdf)
           + Scrapely reads the streams of tokens from the unannotated pages, and looks for regions that are similar to the sample’s annotations. To decide what should be extracted from new pages, it notes the tags that occur before and after the annotated regions, referred to as the prefix and suffix respectively.
           + This approach is handy as you don’t need a well-defined HTML page. It instead relies on the order of tags on a page. Another useful feature of this approach is that Scrapely doesn't need to find a 100% match, and instead looks for the best match. Even if the page is updated and tags are changed, Scrapely can still extract the data.   
   + Portia : https://portia.readthedocs.io/en/latest/index.html
   + CRAWLING RULES : Follow links that match these patterns : "/Attraction_Review-.*_California.html"

   + output can be found in **data/output_tripAdvisor_attractions_using_portia/california/california_tripadvisor.csv**
   ```
      "_cached_page_id","_template","_type","address","attraction","attraction_in","contact","knownFor","no_of_reviews","ranking","reviewComment","url"
    "f27898151d9d332e7a2f9dad0efa72b49adea1b4","f1b17f12b271f090607ff7b6e95e4c1a06353518","t","Lincoln Boulevard, near Doyle Drive and Fort Point , San Francisco , CA 94129","Golden Gate Bridge","San Francisco","415-921-5858","","32,693","#2","We hired bikes and rode over the bridge. It was not difficult as there was little wind that day. Great views of the city and Alcatraz and easy rise on to Sausalito. Something not... read more","https://www.tripadvisor.com/Attraction_Review-g60713-d104675-Reviews-Golden_Gate_Bridge-San_Francisco_California.html"
    "ea0a594d33494d39cc83a78f660139c627b7b19e","f1b17f12b271f090607ff7b6e95e4c1a06353518","t","Lincoln Boulevard, near Doyle Drive and Fort Point , San Francisco , CA 94129","Golden Gate Bridge","San Francisco","415-921-5858","","32,693","#2","Probably the most recognizable bridge in the world, the burnt orange hue in unmistakable. Built in the 1930's, it was marvel of technology and foresight. Awesome photos for the... read more","https://www.tripadvisor.com/Attraction_Review-g60713-d104675-Reviews-or10-Golden_Gate_Bridge-San_Francisco_California.html"
    ```

5. **[getAttractions.py](src/getAttractions.py)** : Cleanup Json Lines file from scrapinghub to get rid of default fields of portia ("_cached_page_id","_template","_type"), fetch latitude, longitude via geoCoding the address for each attractions

    + input and output files in **output_tripAdvisor_attractions_using_portia/california/**
    + input : california_tripadvisor.jl
    + output : tripAdvisor_attractions.csv, tripAdvisor_attraction_in.csv, tripAdvisor_attractions/
    ``` attraction_name,attraction_knownFor,attraction_reviewComment,attraction_ranking,attraction_no_of_reviews,attraction_contact,attraction_in,attraction_address,attraction_longitude,attraction_latitude,attraction_url,attraction_in_file
    Presidio of San Francisco,"Historic Sites , Military Bases & Facilities , National Parks , Sights & Landmarks , Nature & Parks , More ","The Presidio grounds were once a much sought after Army installation at the base of the Golden Gate Bridge...many trails lead to awesome views of the bridge, bay and across to... read more",25,"1,112",+1 415-561-5300,San Francisco,"San Francisco , CA 94129",-122.4155266,37.7924289,https://www.tripadvisor.com/Attraction_Review-g60713-d128930-Reviews-Presidio_of_San_Francisco-San_Francisco_California.html,san_francisco.json
    San Francisco Maritime National Historical Park,"Neighborhood: Fisherman’s Wharf Educational sites , National Parks , Specialty Museums , Sights & Landmarks , Nature & Parks , Museums , More",Every ship in this exhibit is worth visiting. We've been here several times because there is so much to see. Plus not every ship is open all the time. Our last visit was to the... read more,46,402,415-447-5000,San Francisco,"499 Jefferson St , San Francisco , CA 94109-1314",,,https://www.tripadvisor.com/Attraction_Review-g60713-d104217-Reviews-San_Francisco_Maritime_National_Historical_Park-San_Francisco_California.html,san_francisco.json
    ```

6. **[youTubeSearch.py](src/youTubeSearch.py)** : Leverage YouTube API to fetch youtube links for location mentions.
    + input/output files are present in **data/data_for_record_linkage_csv/california/**
    + an input file : allBlogLocation_City_Mentions.csv, 
    + youtubeIds shall be added for each location : "GdbRaajAVA0,UYjNTENqynE,pAaxxTSasWU"
    + corresponding output file : allBlogLocation_City_Mentions_withYouTube.csv

7. **[updateYouTubeLinks_TripAdvisorAttractions.py](src/updateYouTubeLinks_TripAdvisorAttractions.py)** : reads youTube ids of each attraction from csv file and updates respective json object present in tripAdvisor_attractions/
    + input : data/data_for_record_linkage_csv/california/tripAdvisor_attractions_with_LatLong_withYouTube.csv 
    + output : data/data_for_record_linkage_csv/california/tripAdvisor_attractions/

8. **Query DbPedia to Fetch Abstract and Comment for each location in California** : [dbpedia_sparql/isPartOf_california_query.sparql](src/dbpedia_sparql/isPartOf_california_query.sparql)
   ```
   $ curl -X POST -H "Accept: text/csv" --data-urlencode "query@isPartOf_california_query.sparql" http://dbpedia.org/sparql > isPartOf_california_query.csv
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 3313k  100 3312k  100   777   392k     92  0:00:08  0:00:08 --:--:--  776k
    $ 
   ```

9. **Record Linkage for Non-City(actual attractions) Mentions**
    + Under **data/data_for_record_linkage_csv/california/non_city_match/**
      config.xml
      EditDistance : (mention_name, attraction_name), (match-level-start=0.1, math-level-end=0.3) weight="100"
    + blogSrc : allBlogLocation_nonCity_Mentions.csv
    + tripAdvisorSrc : tripAdvisor_attractions_with_LatLong_withYouTube.csv
    + result in : result.csv
  
10. **Record Linkage for City Mentions**
    1. First Level of Match between City Mentions from Blogs and TripAdvisor, Attration_IN
     1. Under **data/data_for_record_linkage_csv/california/city_match/match_blog_tripAdvisor/**
      config.xml
      EditDistance : (mention_name, attraction_name), (match-level-start=0.1, math-level-end=0.3) weight="50"
      NumericDistance : (mention_latitude, attraction_latitude) exactMatch weight="25"
      NumericDistance : (mention_longitude, attraction_longitude) exactMatch weight="25"
      2. blogSrc : allBlogLocation_City_Mentions_withYouTube.csv
      3. tripAdvisorSrc : tripAdvisor_attraction_in_with_LatLong_withYouTube.csv
      4. result in : result.csv
    2. Second Level of Match between record linked blogTripAdvisor Mention with dbPedia City info
     1. Under **data/data_for_record_linkage_csv/california/city_match/**
      config.xml
      NumericDistance : (mention_lat_round, lat_round) exactMatch weight="50"
      NumericDistance : (mention_long_round, long_round) exactMatch weight="50"
      2. blogTripAdvSrc : match_blog_tripAvisor_result.csv
      3. dbPediaSrc : isPartOf_california_query.csv
      4. result in : result.csv
    3. Final Results of 2 types of record linkages are available in **data/record_linkage_results/**
       city_result.csv          nonCity_result.csv 

11. **fetchImages_dumpCityJson.py** : dump city json data with relevant images for enroute-genie mashup
    + input : record_linkage_results/city_result.csv
    + output : data/cityData_output/
    
12. **fetchImages_integrate_ReviewComments.py** : dump mention json data with relevant images and reviewComments_Urls of tripAdvisor for enroute-genie mashup
    + input : record_linkage_results/nonCity_result.csv, record_linkage_results/tripAdvisor_attractions/
    + output : data/mentionData_output/
    
13. **integrateMentionData_BlogLinks.py** : dump mention json data with relevant blogLinks for enroute-genie mashup
    + input : data/mentionData_output/ , data/output_candidate_location_from_blogs_using_NER/california/, /
    + output : mentionData_withBlogLinks_output/

14. **annotateInterestingPlaces_BlogUrls.py** : annotate interesting locations from blogsUrls into city/attraction interest
    + read blogUrls from each of location pairs in :    data/annotate_input_data/
    + dump annotated results to :                       data/annotated_output_data/

15. **enlist_annotated_attractions_to_csv.py** : annotate interesting locations from blogsUrls into city/attraction interest
    + read annotated cities and attraction in :     data/annotated_output_data/los\ angeles_and_san\ francisco.json 
    + dump annotated results in sorted order into : data/annotated_output_data/los angeles_and_san francisco.csv
    
16. **enlist_blogNER_attractions_to_csv.py** : read blog NER attractions from json and enlist in sorted order to csv
    + read blog NER attractions from json :             data/output_candidate_location_from_blogs_using_NER/california/los\ angeles_and_san\ francisco.json
    + dump attractions results in sorted order into :   data/output_candidate_location_from_blogs_using_NER/california/los angeles_and_san francisco.csv
    
17. **enlist_blogNER_geoCoded_relevant_attractions_to_csv.py** : read blog NER GeoCoded relevant attractions from json and enlist in sorted order to csv
    + read blog NER GeoCoded relevant attractions from json :   data/output_candidate_location_from_blogs_using_NER/california/los\ angeles_and_san\ francisco.json 
    + dump attractions results in sorted order into :           data/output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/los angeles_and_san francisco.csv


18. **overlap_auto_manual_attractions.txt** : analysis results of determining overlap bw enroute-genie auto and manual user annotation
    + we collect results of (15,16,17) into columns of data/annotated_output_data/compare_results_los angeles_and_san francisco_odt.ods
    ```
    >wc -l overlap_auto_manual_attractions.txt 
    76 overlap_auto_manual_attractions.txt
    ```
    
19. **new_mergeAllResults.py** : integrate data for enroute-genie mashup
    + read enriched metadata for mentions from  :  data/merge_data/mentionData_withBlogLinks_output/ and updates the respective mentions in  data/merge_data/geoCodeLocations_output/
    + read enriched metadata for city from  :  data/merge_data/cityData_output/ and updates the respective city mentions in data/merge_data/geoCodeLocations_output/

20. **sentimentAnalysis_ReviewComments.py** : perform sentiment analysis [using https://textblob.readthedocs.io/en/dev/api_reference.html#textblob.blob.TextBlob.sentiment] for review comments classifying them into positive, negative and neutral polarity classes
    + read and update reviewComments from data/merge_data/geoCodeLocations_output/

21. **loadData_CouchDb.py** : load data into NoSQL database CouchDB
    + read and upload json data from data/merge_data/geoCodeLocations_output/

22. **web_interface/index.html** : Basic UI to render the EnRoute Genie Magic

23. **summaryStatistics.py** : Script for Statistical Analysis of Results


31. **imageFetch.py** : an utility script to fetch images for specified query from yandex
32. **sortFileContents.py** : an utility script to alphabetically sort contents of a file
33. **fetchImages_Attractions.py** : an utility script to fetch images for the attractions given in a txt file
34. **sentimentAnalysis.py** : an utility script to fetch sentiment polarity for a review comment




