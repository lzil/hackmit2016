var request = require("request");
var fs = require("fs");

var apiKey = "875fa8053fd2491d93dd442850e44a38";

var count = 500;

var texture = "pusheen";

// do we want to add safeSearch? or are we confident that nothing too.. questionable will be returned?

var url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=" + texture + "&count=" + count;

var header = {
  "Ocp-Apim-Subscription-Key": "875fa8053fd2491d93dd442850e44a38"
}

request({"url": url, "headers": header}, function(error, res, body) {
  if (error) throw error;

  body = JSON.parse(body);

  var file = "images/pusheen.txt";

  var images = body.value;

  for (var pic in images) {

    console.log(images[pic].contentUrl);

    fs.appendFileSync(file, images[pic].contentUrl + "\n");
    
  }
});


