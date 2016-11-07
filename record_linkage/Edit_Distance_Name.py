import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd
import os, sys

blogTablePath = '/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/csvResults.csv'
tripAdvisorTablePath = '/media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/enroute_items.csv'
# Load csv files as dataframes.
blogTable = pd.read_csv(blogTablePath)
tripAdvisorTable = pd.read_csv(tripAdvisorTablePath)
print('Number of records in blogTable: ' + str(len(blogTable)))
print('Number of records in tripAdvisorTable: ' + str(len(tripAdvisorTable)))

# profile attributes in table blogTable
ssj.profile_table_for_join(blogTable)
# profile attributes in table tripAdvisorTable
ssj.profile_table_for_join(tripAdvisorTable)

# find all pairs from blogTable and tripAdvisorTable such that the edit distance
# on 'name' and 'attraction' is at most 5.
# l_out_attrs and r_out_attrs denote the attributes from the 
# left table (A) and right table (B) that need to be included in the output.
#name	locType	longitude	latitude	closest_to	blogLinks	src	dest	address	srcLoc	destLoc
#attraction_in	no_of_attractions	no_of_reviews	url	reviewComment	activity_type	rank	max_rank	
#attraction	contact_no	knownFor	address	pinCode

output_pairs = ssj.edit_distance_join(blogTable, tripAdvisorTable, 
                                'name', 'url', 
                                'name', 'attraction', 
                                3,
                                l_out_prefix='blogs_',
                                r_out_prefix='tripAdvisor_',
                                l_out_attrs=['name','locType','address'],
                                      
                                r_out_attrs=['attraction','knownFor','address','pinCode',
                                             'reviewComment','no_of_reviews','url','contact_no',
                                             'rank','max_rank',
                                             'activity_type','attraction_in','no_of_attractions'],
                                n_jobs=-1)

print(len(output_pairs))
# examine the output pairs
csvFile = open('editDistance.csv', 'w')
output_pairs.to_csv(csvFile)
print(output_pairs.loc[:,'_sim_score'])

