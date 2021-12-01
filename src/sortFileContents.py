# PS C:\Users\Ravi\Desktop\USC\Courses_Sem3\Info_Integrate_Web\Project\Enroute-Genie\compare_attractions> ls
# Mode                LastWriteTime         Length Name
# ----                -------------         ------ ----
# -a----       11/12/2016   9:39 AM         127203 attraction_name.txt
# -a----       11/12/2016   9:39 AM         120979 mention_name.txt
# PS C:\Users\Ravi\Desktop\USC\Courses_Sem3\Info_Integrate_Web\Project\Enroute-Genie\compare_attractions> python3 ..\sortF
# ileContents.py .\attraction_name.txt
# PS C:\Users\Ravi\Desktop\USC\Courses_Sem3\Info_Integrate_Web\Project\Enroute-Genie\compare_attractions> python3 ..\sortF
# ileContents.py .\mention_name.txt
# PS C:\Users\Ravi\Desktop\USC\Courses_Sem3\Info_Integrate_Web\Project\Enroute-Genie\compare_attractions> ls
# Mode                LastWriteTime         Length Name
# ----                -------------         ------ ----
# -a----       11/12/2016   9:39 AM         127203 attraction_name.txt
# -a----       11/12/2016  10:50 AM         127203 attraction_name_sorted.txt
# -a----       11/12/2016   9:39 AM         120979 mention_name.txt
# -a----       11/12/2016  10:50 AM         120979 mention_name_sorted.txt
# PS C:\Users\Ravi\Desktop\USC\Courses_Sem3\Info_Integrate_Web\Project\Enroute-Genie\compare_attractions>

import argparse

def sortFile(fileName):
    places = []
    sortedFileName = fileName.rstrip('.txt') + '_sorted.txt'
    with open(fileName, 'r') as infile:
        for line in infile:
            places.append(line)
    places.sort()
    with open(sortedFileName, 'w') as outfile:
        for place in places:
            print(place,file = outfile,end = '')
def main():
	parser = argparse.ArgumentParser(description="sorts file alphabetically")
	parser.add_argument("fileName", help="file to be sorted")
	args = parser.parse_args()
	fileName = args.fileName

	sortFile(fileName)

if __name__ == "__main__" : main()