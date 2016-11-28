Launch fril from : 
FRIL-v2.1.5$ ./fril.sh

sequence-based measure: Edit Distance Similarity Measure was used to join the Datasets with
Approve Level : 0.1, Disapprove level : 0.3 (As recommended by FRIL documentation)
Condition weight : 50
on mention_name(allBlogLocation_City_Mentions_withYouTube.csv) and attraction_in(tripAdvisor_attraction_in_with_LatLong_withYouTube.csv)

Numeric-distance with 0 diff(exact match) bw:
Condition weight : 25 mention_latitude(allBlogLocation_City_Mentions_withYouTube.csv) and attraction_latitude(tripAdvisor_attraction_in_with_LatLong_withYouTube.csv)
Condition weight : 25 mention_longitude(allBlogLocation_City_Mentions_withYouTube.csv) and attraction_longitude(tripAdvisor_attraction_in_with_LatLong_withYouTube.csv)


Sorted neighbourhood method was used for Join Method Type

[12:55:12] cdc.impl.resultsavers.CSVFileSaver: Close in CSV saver for file /media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/data_record_linkage_csv/california/city_match/result.csv
[12:55:12] cdc.impl.resultsavers.CSVFileSaver: Close in CSV saver for file /media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/data_record_linkage_csv/california/city_match/minus-blogSrc.csv
[12:55:12] cdc.impl.resultsavers.CSVFileSaver: Close in CSV saver for file /media/ravirajukrishna/Windows/Users/Ravi/Desktop/USC/Courses_Sem3/Info_Integrate_Web/Project/Enroute-Genie/data_record_linkage_csv/california/city_match/minus-tripAdvisorSrc.csv
[12:55:12] cdc.gui.LinkageThread: SNMJoin(window size 8): Algorithm produced 248 joined tuples. Elapsed time: 756ms.


attraction_latitude and lat
Numeric distance value- 0 to value + 0.001
