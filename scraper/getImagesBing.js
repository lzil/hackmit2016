// the searchTerm should be one token.
// weird things might happen otherwise...

var searchTerm = process.argv[2];

if (searchTerm === undefined) {
  return;
}

var request = require("request");
var fs = require("fs");

var apiKey = "875fa8053fd2491d93dd442850e44a38";

var count = 600;

var offset = 0;

var file = "../images/" + searchTerm + ".txt";

function makeUrl(searchTerm, count, offset) {
  return "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=" + searchTerm + "&count=" + count + "&offset=" + offset;
}

var header = {
  "Ocp-Apim-Subscription-Key": "875fa8053fd2491d93dd442850e44a38"
}

var i = 0;

tonyRecursion(0, searchTerm);


function tonyRecursion(skip, searchTerm) {
  if (skip >= count) {
    return;
  }

  var url = makeUrl(searchTerm, count, skip);

  request({"url": url, "headers": header}, function(error, res, body) {
    if (error) throw error;

    body = JSON.parse(body);

    var images = body.value;

    var j = 0;

    for (var pic in images) {
      console.log(images[pic].contentUrl);
      fs.appendFileSync(file, images[pic].contentUrl + "\n");
      j++;
    }

    tonyRecursion(skip + j, searchTerm);
  });
}







