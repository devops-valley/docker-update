import argparse
import json

import docker_compose
import image_tags


def find_updates(image_ref, usages):
	try:
		newer_tags = image_tags.get_new_tags(image_ref)
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
			updates[image_ref] = find_updates(image_ref, images[image][tag])
			for usage in images[image][tag]:
				if "base_image" in usage:
					continue
				for base in usage["base_image"]:
					if base in updates:
						continue
					else:
						info = {
							"base_image": True,
							"path:" images[image][tag]["path"],
							"service_name": images[image][tag]["service_name"]
						}
						updates[base] = find_updates(base, info)
						
				
	if args.output:
		with open(args.output, "w") as out:
			json.dump(updates, out, indent=1, sort_keys=True)
	else:
		print(json.dumps(updates, indent=1))
			

if __name__=="__main__":
	parser = docker_compose.args_setup("Show updates for docker-compose style services")
	args = parser.parse_args()
	main(args)
	