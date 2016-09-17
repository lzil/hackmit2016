import dbconnector

searchID = "pusheen"

cat = { "searchID": searchID,
		"meow": "hello",
		"woof": "scary"}

dbconnector.insert(searchID, cat)