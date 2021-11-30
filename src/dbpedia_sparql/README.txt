curl -X POST -H "Accept: text/csv" --data-urlencode "query@locatedIn_california_query.sparql" http://dbpedia.org/sparql > locatedIn_california_query.csv
curl -X POST -H "Accept: text/csv" --data-urlencode "query@isPartOf_california_query.sparql" http://dbpedia.org/sparql > isPartOf_california_query.csv



$ curl -X POST -H "Accept: text/csv" --data-urlencode "query@locatedIn_california_query.sparql" http://dbpedia.org/sparql > locatedIn_california_query.csv
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  338k  100  337k  100   746   179k    396  0:00:01  0:00:01 --:--:--  181k

$ curl -X POST -H "Accept: text/csv" --data-urlencode "query@isPartOf_california_query.sparql" http://dbpedia.org/sparql > isPartOf_california_query.csv
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 3313k  100 3312k  100   777   392k     92  0:00:08  0:00:08 --:--:--  776k
$ 
