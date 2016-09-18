# *** call tonyRecursion(0, <<search term>>) ***
# to get a list of ~600 urls to train on.

# search term should be one word (as in, no spaces).
# I suspect strange things would happen if there's a space...

from __future__ import print_function
import requests

# picked 600 because later results become more irrelevant. 
count = 600

headers = {
  "Ocp-Apim-Subscription-Key": "875fa8053fd2491d93dd442850e44a38"
}

def makeUrl(searchTerm, count, offset): 
  baseurl = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?count={}&offset={}&q={}"
  return baseurl.format(count, offset, searchTerm)

toReturn = []

f = None

def tonyRecursion(skip, searchTerm):
  global toReturn
  global f

  if skip >= count:
    f.close()
    return toReturn

  # clear the toReturn array, just in case it has been used before 
  # and still contains the previous results.
  if skip == 0:
    toReturn = []

  file = "../cache/links/" + searchTerm + ".txt"
  url = makeUrl(searchTerm, count, skip)

  r = requests.get(url, headers=headers)
  r = r.json()

  i = 0

  if f == None:
    f = open(file,'w')

  for image in r["value"]:
    toReturn.append(image["contentUrl"])
    print(image["contentUrl"], file=f)
    i += 1

  return tonyRecursion(skip + i, searchTerm)

# for testing purposes
# print(tonyRecursion(0, "green"))

