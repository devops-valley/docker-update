import requests
from datetime import datetime
import argparse
import json

TAGS = "https://registry.hub.docker.com/v2/repositories/{image}/tags/"
LIB_PREFIX = "library/"

TAG_STORE = {}

def get_tags(image):
	if "/" not in image:
		image = LIB_PREFIX + image
	url = TAGS.format(image=image)
	result = requests.get(url)
	data = result.json()
	tags = {}
	for entry in data["results"]:
		tags[entry["name"]] = datetime.strptime(entry["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
	return tags

def get_new_tags(image):
	if not ":" in image:
		print("using implicit latest, skip")
		return
	image_name, current_tag = image.split(":")
	if not image_name in TAG_STORE:
		TAG_STORE[image_name] = get_tags(image_name)
	if current_tag in TAG_STORE[image_name]:
		first_update = TAG_STORE[image_name][current_tag]
	else:
		print("!!! FALLBACK!")
		first_update = TAG_STORE[image_name].entry_set()[0]
	print(first_update)
	new_tags = {}
	for tag in TAG_STORE[image_name]:
		print("("+str(tag)+")")
		update = TAG_STORE[image_name][tag]
		if update > first_update:
			new_tags[tag] = str(update)
	return new_tags

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="list new docker image tags")
	parser.add_argument("--image", "-i", nargs="+")
	
	args= parser.parse_args()
	for i in args.image:
		print(i)
		print(json.dumps(get_new_tags(i), indent=1))
# call with: `python3 image_tags.py -i alpine ubuntu:xenial debian`