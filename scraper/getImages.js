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

var apiKey = "AIzaSyCe_hA3GopdanHqz9HHahkK3HKOefl7NEk"; // Grace's new gmail key

//"AIzaSyCMchj-5QlA8EeJP0bakf8_1FJ1rAlIzHU"; // Tony's key

//"AIzaSyDtdaThaXGyE-7O93cCoiJKyM4Hfh_fON0"; // Rachel's key

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
//  "pusheen"
];
/*
for (var i in textures) {
  tonyRecursion(0, textures[i]);
  sleep.sleep(30);
}
*/

tonyRecursion(100, "stripe")

function tonyRecursion(start, searchTerm) {

  if (start >= 120) {
    return;
  }

  console.log(start);

  var params = {
    "key": apiKey,
    "q": searchTerm,
    "searchType": "image",
    "cx": cx,
    "num": 10,
    "start": start
  };
  var file = "../cache/links" + searchTerm + ".txt";

  request({"url": url, "qs": params}, function(err, res, body) {
    if (err) {
      console.log(err);
      throw err;
    }

    var objBody = JSON.parse(body);

    for (var j in objBody.items) {
      fs.appendFileSync(file, objBody.items[j].link + "\n");
      console.log(objBody.items[j].link);
    }
    console.log();
  });

  sleep.sleep(2);

  return tonyRecursion(start + params.num, searchTerm);
}



