import argparse
import json

import docker_compose
import image_tags




def main(args):
	updates = {}
	images = docker_compose.start(args.compose_files, args.ignore)
	for image in images:
		for tag in images[image]:
			image_ref = f"{image}:{tag}"
			try:
				newer_tags = image_tags.get_new_tags(image_ref)
			except ValueError as e:
				newer_tags = e.args
			updates[image_ref] = {
				"updates": newer_tags,
				"usages": images[image][tag]
			}
	if args.output:
		with open(args.output, "w") as out:
			json.dump(updates, out, indent=1, sort_keys=True)
	else:
		print(json.dumps(updates, indent=1))
			

if __name__=="__main__":
	parser = docker_compose.args_setup("Show updates for docker-compose style services")
	args = parser.parse_args()
	main(args)
	