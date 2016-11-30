import argparse, json, os
from pprint import pprint
from textblob import TextBlob
from collections import namedtuple

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)

def classifyReviews(reviewComments, reviewUrls):
    Sentiment = namedtuple('Sentiment', ['reviewComment', 'polarity', 'subjectivity', 'reviewUrl'])
    classifiedReviewComments = {'positive' : [], 'negative' : [],'neutral' : []}
    for index,reviewComment in enumerate(reviewComments):
        if reviewUrls:
            reviewUrl = reviewUrls[index]
        else:
            reviewUrl = ""
        reviewTextBlob = TextBlob(reviewComment)
        polarity = reviewTextBlob.sentiment.polarity
        subjectivity = reviewTextBlob.sentiment.subjectivity
        #print(reviewComment, reviewTextBlob.sentiment)
        if polarity > 0 :
            classifiedReviewComments['positive'].append(Sentiment(reviewComment, polarity, subjectivity, reviewUrl))
        elif polarity < 0 :
            classifiedReviewComments['negative'].append(Sentiment(reviewComment, polarity, subjectivity, reviewUrl))
        else:#polarity == 0
            classifiedReviewComments['neutral'].append(Sentiment(reviewComment, polarity, subjectivity, reviewUrl))
    return classifiedReviewComments
        
def analyseSentiment(geoCodeLocations_output):
    for path,fileName in rscandir(geoCodeLocations_output):
        filePath = os.path.join(path, fileName)
        print("\nReading data from {}".format(fileName))
        currentJsonData = {}
        newJsonData = {}
        with open(filePath) as data_file:
            currentJsonData = json.load(data_file)
            mentions = currentJsonData["mentions"]
            for mention in mentions:
                if "enrich_metadata" in currentJsonData["mentions"][mention]:
                    if "attraction_reviewComments" in currentJsonData["mentions"][mention]["enrich_metadata"]:
                        newJsonData = currentJsonData.copy()
                        reviewComments = currentJsonData["mentions"][mention]["enrich_metadata"]["attraction_reviewComments"]
                        reviewUrls = currentJsonData["mentions"][mention]["enrich_metadata"]["attraction_reviewUrls"]
                        if len(reviewComments) == len(reviewUrls):
                            classifiedReviewComments = classifyReviews(reviewComments, reviewUrls)
                        else:
                            classifiedReviewComments = classifyReviews(reviewComments, None)
                        #pprint(classifiedReviewComments['negative'])
                        newJsonData["mentions"][mention]["enrich_metadata"]['classified_attraction_reviewComments'] = classifiedReviewComments
        if newJsonData:
            with open(filePath, 'w') as updated_data_file:
                json.dump(newJsonData, updated_data_file, indent=4)
                print("Updated Classified ReviewComments in {}".format(filePath))

#python sentimentAnalysis_ReviewComments.py merge_data/geoCodeLocations_output/
def main():
    parser = argparse.ArgumentParser(description="perform sentiment analysis for review comments")
    parser.add_argument("geoCodeLocations_output", help="path to geoCodeLocations_output") #merge_data/geoCodeLocations_output/

    args = parser.parse_args()

    geoCodeLocations_output = args.geoCodeLocations_output

    analyseSentiment(geoCodeLocations_output)


if __name__ == "__main__" : main()
