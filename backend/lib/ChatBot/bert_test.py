import json


dictObj = {
	'andy':{
		'age': 23,
		'city': 'shsdada打算等hai',
		'skill': 'python'
	},
	'william': {
		'age': 33,
		'city': 'hangz的撒大hou',
		'skill': 'js'
	}}
with open("jsonobj.json","w",encoding="utf-8") as f:
    json.dump(dictObj,f,ensure_ascii=False)
