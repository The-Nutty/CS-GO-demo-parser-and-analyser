import os
from selenium import webdriver
import urllib.request
import shutil
from pyunpack import Archive

#Example events
# http://www.hltv.org/?pageid=357&eventid=2410
# http://www.hltv.org/?pageid=357&eventid=2239
# http://www.hltv.org/?pageid=357&eventid=2062
#the event Id
event = "2410"

print("Getting Demo Id's")
#we use panatomJS because its headless
driver = webdriver.PhantomJS()
driver.get(
    "http://www.hltv.org/?pageid=28&eventid=" + event)

#Find all links in the page(slow TODO find a faster way)
links = driver.find_elements_by_xpath("//*[@href]")

#For each link check if its one that we are intrested in, if so extrat teh demo id
demoIds = []
for link in links:
    text = str(link.get_attribute("href"))
    if "comments" not in text and "demoid" in text and "?pageid=28&&eventid=" + event in text:
        index = text.index("demoid")  #
        demoIds.append(text[index + 7:])
print("Got all demoId's")

#before we start downloading make sure the correct folders exist
for dir in ["tmp", "demos", "demos/" + event]:
    if not os.path.exists(dir):
        os.makedirs(dir)

#HLTV throws a 403 if you dont have the correct userAgent
userAgent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

baseUrl = "http://www.hltv.org/interfaces/download.php?demoid="

for id in demoIds:
    print("Getting demo with id " + id)
    tmpFileName = "tmp/" + id + ".rar"

    #request and save to file the rar
    request = urllib.request.Request(baseUrl + id, headers=userAgent)

    with urllib.request.urlopen(request) as response, open(tmpFileName, 'wb+') as out_file:
        shutil.copyfileobj(response, out_file)
    #extract the rar to the corect place (demos folder)
    Archive(tmpFileName).extractall("demos/" + event + "/")

print("Removing Temp Files")
shutil.rmtree("tmp")
print("Done")