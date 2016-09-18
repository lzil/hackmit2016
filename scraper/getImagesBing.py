# call tonyRecursion(0, <<search term>>) 
# to get a list of ~600 urls to train on.

# search term should be one word (as in, no spaces).
# I suspect strange things would happen if there's a space...

#from __future__ import print_function 
import requests

# picked 600 because later results become more irrelevant. 
count = 600

headers = {
  "Ocp-Apim-Subscription-Key": "875fa8053fd2491d93dd442850e44a38"
}

def makeUrl(searchTerm, count, offset): 
  return "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=" + searchTerm + "&count=" + str(count) + "&offset=" + str(offset)
  """
  if offset == 0:
    baseurl = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count={}"
    return baseurl.format(searchTerm, count)

  baseurl = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count={}&offset={}"
  return baseurl.format(searchTerm, count, offset)
  """

toReturn = []

def tonyRecursion(skip, searchTerm):
  if skip >= count:
    return toReturn

  # clear the toReturn array, just in case it has been used before 
  # and still contains the previous results.
  if skip == 0:
    toReturn = []
  

  url = makeUrl(searchTerm, count, skip);
  print(url)

  payload = {
    "q": searchTerm,
    "count": count,
    "offset": skip
  }

  r = requests.get(url, params=payload, headers=headers)
  r = r.json()

  print(r)

  for thing in r: 
    print(thing)

  #file = "../cache/links" + searchTerm + ".txt"
  i = 0

  for image in r["value"]:
    toReturn.append(image["contentUrl"])
    #print(image["contentUrl"], file)
    i += 1

  return tonyRecursion(skip + i, searchTerm)


print(tonyRecursion(0, "green"))

