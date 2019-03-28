Docker Update
=============

Show available image-updates for your docker-compose managed services. Checks docker-compose image-tags as well as connected Dockerfiles in build-sections. 

Lists (possible) available updates and where the old image(-tag) is used. Optimized for use with "pinned" tags. (Use a specific minor version to fuse your infrastrucutre.)


Requirements
------------

* Docker
* docker-compose
* Python >=3.6
* Libraries: requirements.txt (`pip3 install -r requirements.txt` or docker ;))


Filesystem Structure
--------------------

You can call it on a single directory containing your `docker-compose.yml`. 

Or you can execute it on a directory containing your service directories. These services must have a docker-compose.yml to get checked.

Example:
```
└── services
    ├── bitpoll.example.org
    │   ├── docker
    │   │   └── Dockerfile
    │   └── docker-compose.yml
    ├── dockerui
    │   └── docker-compose.yml
    └── gitea
        └── docker-compose.yml
```

If there are files or directories without a docker-compse.yml, it will just notify you and ignore it. 

If the compose file contains a build-section, the Dockerfile is inspected, too.

Usage
----

### Docker

Modify mount of services directory. Mount your directory as `/services`.

```
docker-compose up
```

Output file: `updates.json`

### Command line

```
$ python3 show_updateable.py -h
usage: show_updateable.py [-h] [--output OUTPUT]
                          [--ignore IGNORE [IGNORE ...]] [--match-suffix]
                          compose_files [compose_files ...]
```

* output: json file for results
* ignore: ignore services (ignore is substring of service path)
* match-suffix: use only same suffixes in image labels (e.g. only -alpine images)
* compose files: service directories: see #example (multiple paths allowed)


Example Output
--------------

```
{
 "postgres:10-alpine": {
  "updates": {
   "10.1-alpine": "2018-01-10 04:44:17.433471",
   "10.2-alpine": "2018-02-19 19:43:46.911031",
   "10.3-alpine": "2018-05-12 10:44:57.814207",
   "10.4-alpine": "2018-08-01 14:49:09.002434",
   "11-alpine": "2018-08-01 14:46:34.449579"
  },
  "usages": [
   {
    "path": "/services/bitpoll.example.org/docker-compose.yml",
    "service_name": "dbbitpoll.example.org"
   },
   {
    "path": "/services/gitea/docker-compose.yml",
    "service_name": "dbgitea"
   }
  ]
 }
}
```


Advantages
----------

* No access to Docker-Socket
* No deamon
* No state
* Detect new major versions
* Report only, no uncontrolled automated actions
* tbc ...


Alternatives
------------

* https://github.com/v2tec/watchtower (seems quite dead, look for forks)
* https://github.com/pyouroboros/ouroboros
* https://engineering.salesforce.com/open-sourcing-dockerfile-image-update-6400121c1a
* https://stackoverflow.com/questions/26423515/how-to-automatically-update-your-docker-containers-if-base-images-are-updated
* tbc ...


Known Issues
------------

* Still WiP/PoC
* http/https sources are not implemented yet
* does not handle image updates without changing tags
* some images have … weird tags
* pull requests welcome

