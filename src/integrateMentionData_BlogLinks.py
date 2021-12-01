import argparse, json, os

def rscandir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield (root, file)

def integrateBlogLinks(path_mentionData_output, path_blogLinksSrc, path_mentionData_withBlogLinks_output):
    for path,fileName in rscandir(path_mentionData_output):
        filePath = os.path.join(path, fileName)
        with open(filePath) as fp:
            data = json.load(fp)
            new_data = data.copy()
            mention_name = data['mention_name']
            print(mention_name)
            blogFilesInfo = data['mention_found_in_blogFiles']
            blogFiles = [blogFile.replace('\"','') for blogFile in blogFilesInfo.split(",")]
            print("No of blogFiles : {}".format(len(blogFiles)))
            blogLinksSet = set()
            for blogFile in blogFiles:
                blogFilePath = path_blogLinksSrc + blogFile
                if os.path.isfile(blogFilePath):
                    with open(blogFilePath) as blogFile:
                        blogData = json.load(blogFile)
                        #print()
                        #print(blogFile)
                        blogMentions = (blogData['location_BlogUrls'].keys())
                        for index,key in enumerate(blogMentions):
                            #print(index, key, key.lower())
                            if mention_name == key.lower():
                                blogLinks = blogData['location_BlogUrls'][key]
                                for blogLink in blogLinks:
                                    blogLinksSet.add(blogLink)
                        #print(blogLinks)
                else:
                    print("{} doesnt exists".format(blogFilePath))
            print("No of blogLinks fetched: {}".format(len(blogLinksSet)))
            new_data['blogLinks'] = list(blogLinksSet)
            newFilePath = path_mentionData_withBlogLinks_output + fileName
            with open(newFilePath, 'w') as newFile:
                json.dump(new_data, newFile, indent =4)
                print("Dumped results to {}".format(newFilePath))

#python integrateMentionData_BlogLinks.py mentionData_output/ output_candidate_location_from_blogs_using_NER/california/ mentionData_withBlogLinks_output/
def main():
    parser = argparse.ArgumentParser(description="dump mention json data with relevant blogLinks for enroute-genie mashup")
    parser.add_argument("path_mentionData_output", help="path to json directory containing mentions without blogLinks") #mentionData_output/
    parser.add_argument("path_blogLinksSrc", help="path to json directory containing blogLinks") #output_candidate_location_from_blogs_using_NER/california/
    parser.add_argument("path_mentionData_withBlogLinks_output", help="path to where integrated json data has to be dumped") #mentionData_withBlogLinks_output/
    args = parser.parse_args()
    path_mentionData_output = args.path_mentionData_output
    path_blogLinksSrc = args.path_blogLinksSrc
    path_mentionData_withBlogLinks_output = args.path_mentionData_withBlogLinks_output
    integrateBlogLinks(path_mentionData_output, path_blogLinksSrc, path_mentionData_withBlogLinks_output)
    
if __name__ == "__main__" : main()
