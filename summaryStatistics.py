
# coding: utf-8

# In[4]:

import json, os

def rscandir(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.json'):
				yield (root, file)


# In[28]:

path_blogLocation = 'output_candidate_location_from_blogs_using_NER/california/'
total_no_locations_parsed = 0
unique_locations_parsed = set()
for path,fileName in rscandir(path_blogLocation):
    filePath = os.path.join(path, fileName)
    with open(filePath) as data_file:    
        data = json.load(data_file)
        locationsParsed = (data['location_BlogUrls'].keys())
        for location in locationsParsed:
            unique_locations_parsed.add(location)
        all_locations_count = len(locationsParsed)
        total_no_locations_parsed += all_locations_count
        #print("No of locations Parsed in {} : {}".format(filePath, all_locations_count))
print("{} : No of locations Parsed in {}".format(total_no_locations_parsed, path_blogLocation))
print("{} : No of unique locations Parsed in {}".format(len(unique_locations_parsed), path_blogLocation))


# In[30]:

path_geoCodedLocations = 'output_geoCoded_locations_from_blogs_using_geopy_json/california/geoCodeLocations_output/'
total_no_locations_parsed = 0
unique_locations_parsed = set()
for path,fileName in rscandir(path_geoCodedLocations):
    filePath = os.path.join(path, fileName)
    with open(filePath) as data_file:    
        data = json.load(data_file)
        locationsParsed = (data['mentions'].keys())
        for location in locationsParsed:
            unique_locations_parsed.add(location)
        all_locations_count = len(locationsParsed)
        total_no_locations_parsed += all_locations_count
        #print("No of locations Parsed in {} : {}".format(filePath, all_locations_count))
print("{} : No of locations Parsed in {}".format(total_no_locations_parsed, path_geoCodedLocations))
print("{} : No of unique locations Parsed in {}".format(len(unique_locations_parsed), path_geoCodedLocations))


# In[46]:

final_merge_data = 'merge_data/geoCodeLocations_output/'
total_no_locations_parsed = 0
unique_locations_parsed = set()
unique_enriched_cities = set()
unique_enriched_non_cities = set()
unique_non_enriched_cities = set()
unique_non_enriched_non_cities = set()
total_no_of_cities = 0
total_no_of_non_cities = 0
total_no_of_enriched_cities = 0
total_no_of_enriched_non_cities = 0
for path,fileName in rscandir(final_merge_data):
    filePath = os.path.join(path, fileName)
    with open(filePath) as data_file:    
        data = json.load(data_file)
        locationsParsed = (data['mentions'].keys())
        for location in locationsParsed:
            unique_locations_parsed.add(location)
        all_locations_count = len(locationsParsed)
        total_no_locations_parsed += all_locations_count
        if filePath == 'merge_data/geoCodeLocations_output/los angeles_and_san francisco.json':
            print("{} No of locations Parsed in {}".format(all_locations_count, filePath))
        no_of_cities = 0
        no_of_non_cities = 0
        no_of_enriched_cities = 0
        no_of_enriched_non_cities = 0
        for mention in data['mentions']:
            if data['mentions'][mention]['locType'] == 'city':
                no_of_cities +=1
                if 'enrich_metadata' in data['mentions'][mention]:
                    no_of_enriched_cities +=1
                    unique_enriched_cities.add(mention)
                else:
                    unique_non_enriched_cities.add(mention)
            else:
                no_of_non_cities += 1
                if 'enrich_metadata' in data['mentions'][mention]:
                    no_of_enriched_non_cities +=1
                    unique_enriched_non_cities.add(mention)
                else:
                    unique_non_enriched_non_cities.add(mention)
        total_no_of_cities += no_of_cities
        total_no_of_non_cities += no_of_non_cities
        total_no_of_enriched_cities += no_of_enriched_cities
        total_no_of_enriched_non_cities += no_of_enriched_non_cities
        if filePath == 'merge_data/geoCodeLocations_output/los angeles_and_san francisco.json':
            print("\t{0: <5} : No of Cities".format(no_of_cities))
            print("\t{0: <5} : No of Enriched Cities".format(no_of_enriched_cities))
            print()
            print("\t{0: <5} : No of NonCities".format(no_of_non_cities))
            print("\t{0: <5} : No of Enriched NonCities".format(no_of_enriched_non_cities))
print()
print("Summary :")
print("{} : No of locations Parsed in {}".format(total_no_locations_parsed, final_merge_data))
print("{} : No of cities in {}".format(total_no_of_cities, final_merge_data))
print("{} : No of noncities in {}".format(total_no_of_non_cities, final_merge_data))
print()
print("{0: <5} : No of unique locations".format(len(unique_locations_parsed)))
print("{0: <5} : No of unique enriched cities".format(len(unique_enriched_cities)))
print("{0: <5} : No of unique non_enriched cities".format(len(unique_non_enriched_cities)))
print("{0: <5} : No of unique enriched noncities".format(len(unique_enriched_non_cities)))
print("{0: <5} : No of unique non_enriched noncities".format(len(unique_non_enriched_non_cities)))

