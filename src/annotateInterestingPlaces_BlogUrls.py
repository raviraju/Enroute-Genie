import argparse, json, os
import urllib.request
from pprint import pprint
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import nltk

def comboResultsKnown(output_path, keyFileName):
    return os.path.isfile(output_path + keyFileName) 

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
        if req:
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
        #return (cityLocations, mentionLocations)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        return (cityLocations, mentionLocations)

def getDirName(fileName):
    return fileName.replace('.json','')
    
    
def annotate(annotate_input_path, annotated_output_path):
    for path,fileName in rscandir(annotate_input_path):
        filePath = os.path.join(path, fileName)
        print("\nReading blogUrls from {}".format(fileName))
        allAnnotatedData = {}
        allAnnotatedData["cities"] = list()
        allAnnotatedData["attractions"] = list()
        allAnnotatedData["urlDetails"] = list()
        if comboResultsKnown(annotated_output_path, fileName):
            print("Annotated data is already available at {}".format(annotated_output_path + fileName))
            continue 
        with open(filePath, 'r') as blogUrlsFile:
            data = json.load(blogUrlsFile)
            blogUrls = data["blogUrl_Locations"].keys()
            #print(blogUrls)
            index = 1
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
                    dirName = getDirName(fileName)
                    dirPath = annotated_output_path + dirName + '/' 
                    if not os.path.exists(dirPath):
                        os.makedirs(dirPath)
                    tempBlogFileName = dirPath + "blog_" + str(index) + ".json"
                    with open(tempBlogFileName, 'w') as tempBlogFile:
                        json.dump(urlDict, tempBlogFile, indent=4)
                        print("Captured temp results in {}".format(tempBlogFileName))
                    index += 1
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
