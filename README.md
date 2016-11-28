# Enroute-Genie
IIW Project

extractCities.py : extract NER locations from blogsUrls for every pair of popular destinations
    read input/california.json - collection of destinations from Google results of query : https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=popular+cities+in+california
    for every pair of destinations the query : 'places to visit between '  + city_a  + ' and '  + city_b + ' blogs' result links were collected
    for every bloglink content was extracted using beautiful soup
    Text content was tagged with NER LOCATION using StandfordCoreNLP
    output were recorded into json files for a pair city_a  + '_and_'  + city_b + '.json', 
    these can be found in output_candidate_location_from_blogs_using_NER/california
    
    
annotateInterestingPlaces_BlogUrls.py : annotate interesting locations from blogsUrls into city/attraction interest
    read blogUrls from each of location pairs in annotate_input_data/
    dump annotated results in annotated_output_data/


