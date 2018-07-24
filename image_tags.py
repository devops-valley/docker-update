import argparse
import json
import logging
from datetime import datetime

from packaging import version
import requests


log = logging

TAGS = "https://registry.hub.docker.com/v2/repositories/{image}/tags/"
LIB_PREFIX = "library/"

TAG_STORE = {}

def api_call(url):
	result = requests.get(url)
	if not result.ok:
		log.error(result, result.url)
		return {}
	data = result.json()
	tags = {}
	for entry in data["results"]:
		tags[entry["name"]] = datetime.strptime(entry["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ") if entry["last_updated"] else "------"
	if data['next']:
		tags.update(api_call(data['next']))
	return tags

def get_tags(image):
	if "/" not in image:
		image = LIB_PREFIX + image
	if ":" in image:
		image = image.split(":")[0]
	url = TAGS.format(image=image)
	tags = api_call(url)
	if not len(tags):
		raise ValueError(f"Unknown image '{image}'")
	return tags

def replace(string, replacements):
	for k,v in replacements:
		string = string.replace(k,v)
	return string


def compare(base, other, replacements=[("-","+"),]):
	base = replace(base, replacements)
	other = replace(other, replacements)
	v1 = version.parse(base)
	v2 = version.parse(other)
	result = v1 < v2
	log.debug(f"{v1} < {v2}: {result}")
	return result

def get_new_tags(image):
	if not ":" in image:
		log.warn("using implicit latest, skip")
		return
	image_name, current_tag = image.split(":")
	if not image_name in TAG_STORE:
		TAG_STORE[image_name] = get_tags(image_name)
	#if current_tag in TAG_STORE[image_name]:
	#	first_update = TAG_STORE[image_name][current_tag]
	#else:
	#	print("!!! FALLBACK!")
	#	first_update = list(TAG_STORE[image_name].values())[0]
	#print(first_update)
	new_tags = {}
	for tag in TAG_STORE[image_name]:
		log.debug("check("+str(tag)+")")
		if compare(current_tag, tag):
			log.debug("NEWER!!!")
			update = TAG_STORE[image_name][tag]
			new_tags[tag] = str(update)
			log.debug(tag)
			
	return new_tags

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="list new docker image tags")
	parser.add_argument("image", nargs="+")
	parser.add_argument("--list", "-l", action="store_true")
	
	args= parser.parse_args()
	for i in args.image:
		log.debug(i)
		if args.list:
			print(json.dumps({k:str(v) for k,v in get_tags(i).items()}, indent=1))
		else:
			print(json.dumps(get_new_tags(i), indent=1))
# call with: `python3 image_tags.py -i alpine ubuntu:xenial debian`