# call tonyRecursion(0, <<search term>>) 
# to get a list of ~600 urls to train on.

import requests

# picked 600 because later results become more irrelevant. 
count = 600

headers = {
  "Ocp-Apim-Subscription-Key": "875fa8053fd2491d93dd442850e44a38"
}

def makeUrl(searchTerm, count, offset): 
  baseurl = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count={}&offset={}"
  return baseurl.format(searchTerm, count, offset)

toReturn = []

def tonyRecursion(skip, searchTerm):
  if skip >= count:
    return toReturn
  

  # clear the toReturn array, just in case it has been used before 
  # and still contains the previous results.
  if skip == 0:
    toReturn = []
  

  url = makeUrl(searchTerm, count, skip);

  payload = {
    "q": searchTerm,
    "count": count,
    "offset": skip
  }

  r = requests.get(url, params=payload, headers=headers)
  r = r.json()

  i = 0

  for image in r["value"]:
    toReturn.append(image["contentUrl"])
    i += 1

  return tonyRecursion(skip + i, searchTerm)


print(tonyRecursion(0, "green"))

