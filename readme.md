Docker Update
=============

Try to show updates for your used docker images.


Requirements
------------

* Docker
* docker-compose
* Libraries: requirements.txt (`pip3 install -r requirements.txt` or docker ;))

You need a directory containing your service directories. These services must have a docker-compose.yml to get checked.

Example:
```
└── services
    ├── bitpoll.wiai.de
    │   ├── docker
    │   ├── docker-compose.yml
    ├── dockerui
    │   ├── docker-compose.yml
    └── zitate
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
* some images have … weird tags
* pull requests welcome
