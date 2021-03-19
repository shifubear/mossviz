from lxml import html
import mosspy
import os 
import sys
import requests 
import re
import csv
from bs4 import BeautifulSoup


class Pair:
    """
    Class that defines the match level between two students. Mostly just a utility class
    """
    def __init__(self, a, b, matcha, matchb):
        self.a = a
        self.b = b
        self.matcha = matcha
        self.matchb = matchb

    def __str__(self):
        return "Match " + str(self.a) + " (" + str(self.matcha) + "%) and " + str(self.b) + " (" + str(self.matchb) + "%)"

    def __iter__(self):
        return iter([self.a, self.b, self.matcha, self.matchb])


# You can get a userid by emailing moss
userid = 

m = mosspy.Moss(userid, "cc")

#######################################################################
# Load files to moss object
# 
# File structure should be in the following format: 
# 
# base/ contains all the base files of the assignment
# submissions/ contains directories for each student's assignment. 
# 
# This format is what you get when
# downloading from gradescope 
#######################################################################

# Base Files
_, _, basefiles = next(os.walk("./base/"))

for bf in basefiles:
    m.addBaseFile("base/" + bf)

# Submission Files
m.addFilesByWildcard("submissions/*/*.cpp")
m.addFilesByWildcard("submissions/*/*.h")


# Send the file to moss
url = m.send()
print()

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, "./report.html")

# Download whole report locally including code diff links
mosspy.download_report(url, "./report/", connections=8, log_level=10) 
# log_level=logging.DEBUG (20 to disable)
# on_read function run for every downloaded file


########################################################################################################################
# Convert the downloaded report into csv                                                                               #
########################################################################################################################
with open("report.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

links = soup.table.find_all('a')

# Create pairs of matches
pairs = []

for idx in range(len(links)): 
    if (idx % 2 == 0):
        # Parse the matching pairs. 
        ## First parse the two IDs of the students
        a = re.search("_[0-9]+", links[idx].text).group(0)[1:]
        b = re.search("_[0-9]+", links[idx+1].text).group(0)[1:]
        ## Next parse the match percentages
        matcha = int(re.search("[0-9]+%", links[idx].text).group(0)[:-1])   # How similar a is to b
        matchb = int(re.search("[0-9]+%", links[idx+1].text).group(0)[:-1]) # How similar b is to a
        ## Append the parsed data to our pairs array
        pairs.append(Pair(a, b, matcha, matchb))

with open('mossdata.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["StudentA" ,"StudentB", "MatchAtoB", "MatchBtoA"])
    writer.writerows(pairs)
