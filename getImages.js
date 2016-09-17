/* use if you want to call getImages.js
 * with a custom search query

var searchTerm = process.argv[2];

if (searchTerm === undefined) {
  return;
}

*/

var request = require("request");
var fs = require("fs");
var sleep = require("sleep");

var url = "https://www.googleapis.com/customsearch/v1";

var apiKey = "AIzaSyDtdaThaXGyE-7O93cCoiJKyM4Hfh_fON0"; // Rachel's key

//"AIzaSyBHMdlmmquC1RO2VY-52HPTp9vJjdZdyqY" // Grace's ios key
//"AIzaSyCpdIYWYqgoX2kJCMheF3hcg99LE-jjs_I"; // Grace's geocoding key that works with the custom search api apparently.



// do we want to specify imgSize?

var cx = "004922645253613332712:xjvhuhhyrgu";

var textures = [
  "stripe",
  "polka dot"
//  "zig zag",
//  "plaid",
//  "checkerboard"
];

for (var i in textures) {
  tonyRecursion(0, textures[i]);
  sleep.sleep(20);
}


function tonyRecursion(start, searchTerm) {
  console.log(start);

  if (start >= 500) {
    return;
  }
  var params = {
    "key": apiKey,
    "q": searchTerm,
    "searchType": "image",
    "cx": cx,
    "num": 10,
    "start": start
  };
  var file = "images/" + searchTerm + ".txt";

  request({"url": url, "qs": params}, function(err, res, body) {
    if (err) throw err;

    var objBody = JSON.parse(body);

    for (var j in objBody.items) {
      fs.appendFileSync(file, objBody.items[j].link + "\n");
      console.log(objBody.items[j].link);
    }
  console.log();
  });

  sleep.sleep(1);
  
  return tonyRecursion(start + params.num, searchTerm);
}



