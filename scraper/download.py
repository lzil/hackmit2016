# takes a list of urls and downloads them all to a folder.

import urllib
import os

# searchTerm *must* match the file name.

def download(searchTerm):
  directory = "../cache/tmp/" 

  # find the file and go through each line (each url)
  lines = [line.rstrip('\n') for line in open('../cache/links/' + searchTerm + ".txt")]

  # create the directory if necessary

  # download the image and save it in cache/tmp/<searchTerm>
  num = 0
  for line in lines:
    filename = directory + str(num) + ".jpg"
    # create necessary directories and files
    if not os.path.exists(os.path.dirname(filename)):
      try: 
        os.makedirs(os.path.dirname(filename))
      except OSError as exc:
        if exc.errno != errno.EExist:
          raise
    urllib.urlretrieve(line, filename)
    print(num)
    print(filename)
    num += 1

    """
    filename = str(num)
    file = open("../cache/tmp/" + searchTerm + "/" + filename + ".jpg")
    urllib.urlretrieve(line, "../cache/tmp/" + searchTerm + "/" + filename + ".jpg")
    num += 1
    file.close()
    """

download("green")


