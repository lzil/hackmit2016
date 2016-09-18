# call tonyRecursion(0, <<search term>>) 
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

def tonyRecursion(skip, searchTerm):
  if skip >= count:
    return toReturn

  # clear the toReturn array, just in case it has been used before 
  # and still contains the previous results.
  if skip == 0:
    toReturn = []
  

  url = makeUrl(searchTerm, count, skip)

  print(url)

  print()

  r = requests.get(url, headers=headers)
  r = r.json()

  print(r)

  print()

  i = 0

  for image in r["value"]:
    toReturn.append(image["contentUrl"])
    i += 1

  return tonyRecursion(skip + i, searchTerm)


print(tonyRecursion(0, "green"))

