import argparse
import json
import os
import subprocess
import logging

import yaml

from collections import namedtuple

log = logging # TODO: config

COMPOSE_FILE = "docker-compose.yml"
DOCKERFILE = "Dockerfile"

Image = namedtuple("Image", ["image", "tag"])
Service = namedtuple("Service", ["path", "name"])

UNTAGGED = Image(image="unnamed", tag="untagged")

def load_compose_config(f):
	config = subprocess.check_output(["docker-compose", "-f", f, "config"])
	#print(config.decode("utf8"))
	struct = yaml.load(config)
	#json.dump(struct, open(f"{f}.json", "w"), indent=1)
	#print(struct)
	return struct

def source_to_image(source):
	return source.strip().split(" ")[1]

def parse_dockerfile(f):
	if not f.endswith(DOCKERFILE):
		log.warn(f"guessing Döckerfile… {f}")
		f = os.path.join(f, DOCKERFILE)
	if f.startswith("http"):
		log.warn("HTTP sources are not yet supported")
		return [f]
	keyword = "FROM"
	with open(f, "r") as src:
		sources = [source_to_image(line) for line in src if line.strip().startswith(keyword)]
	return sources

def image_info(image):
	splitted = image.strip().split(":")
	if len(splitted) > 1:
		image, tag = splitted
	else:
		image = splitted[0]
		tag = "latest"
	return Image(image=image, tag=tag)

class Collector:
	def __init__(self):
		self.store = {}
	
	def add(self, config, path):
		self.store[path] = config
	
	def get_images(self):
		images = []
		for path, config in self.store.items():
			if not "services" in config:
				log.error(f"no services defined in {path}")
				continue
			images += [service["image"] for name,service in config["services"].items() if "image" in service]
		return images
	
	def get_services_info(self):
		images = {}
		for path, config in self.store.items():
			services = {}
			if not "services" in config:
				log.error(f"no services defined in {path}")
				continue
			for name, service in config["services"].items():
				services[name] = {}
				for k in ["image", "build"]:
					if k in service:
						services[name][k] = service[k]
			images[path] = services
		return images
	
	def get_images_sources(self):
		services = self.get_services_info()
		images = {}
		for path, services in services.items():
			for name, service in services.items():
				service_info = {
					"path": path,
					"service_name": name
				}
				image = UNTAGGED
				if "build" in service:
					service_info["base_images"] = parse_dockerfile(service["build"]["context"])
				if "image" in service:
					image = image_info(service["image"])
				if not image.image in images:
					images[image.image] = {}
				if not image.tag in images[image.image]:
					images[image.image][image.tag] = [service_info]
				else:
					images[image.image][image.tag] += [service_info]
		return images

def start(files):
	collector = Collector()
	for f in files:
		if not f.endswith(COMPOSE_FILE):
			log.warn(f"guessing docker-compöse.yml… {f}")
			f = os.path.join(f, COMPOSE_FILE)
		if not os.path.exists(f):
			log.error(f"file {f} does not exist")
			continue
		config = load_compose_config(f)
		collector.add(config, f)
	#print(json.dumps(collector.get_services_info(), indent=1))
	print(json.dumps(collector.get_images_sources(), indent=1))
		
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Docker-compose parser")
	parser.add_argument("compose_files", nargs="+")
	
	args = parser.parse_args()
	
	start(args.compose_files)