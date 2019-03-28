import argparse
import json
import logging

import docker_compose
import image_tags

log = logging

def find_updates(image_ref, usages, match_suffix=False):
	try:
		newer_tags = image_tags.get_new_tags(image_ref, match_suffix)
	except ValueError as e:
		newer_tags = e.args
	return {
		"updates": newer_tags,
		"usages": usages,
	}


def main(args):
	updates = {}
	images = docker_compose.start(args.compose_files, args.ignore)
	for image in images:
		for tag in images[image]:
			image_ref = f"{image}:{tag}"
			if image_ref in updates:
				continue
			updates[image_ref] = find_updates(image_ref, images[image][tag], args.match_suffix)
			for usage in images[image][tag]:
				if not "base_images" in usage:
					continue
				for base in usage["base_images"]:
					info = {
						"is_base_image": True,
						"path": usage["path"],
						"service_name": usage["service_name"]
					}
					if base in updates:
						updates[base]["usages"].append(info)
					else:
						log.info(f"find base image updates for {base}")
						updates[base] = find_updates(base, [info], args.match_suffix)
				
	if args.output:
		with open(args.output, "w") as out:
			json.dump(updates, out, indent=1, sort_keys=True)
	else:
		print(json.dumps(updates, indent=1))
			

if __name__=="__main__":
	parser = docker_compose.args_setup("Show updates for docker-compose style services")
	args = parser.parse_args()
	print(args)
	main(args)
