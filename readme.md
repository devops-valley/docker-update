Docker Update
=============

Try to show updates for your used docker images.


Requirements
------------

TODO

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



Usage
----

Modify mount of services directory. Mount your directory as `/services`.

```
docker-compose up
```

Output file: `updates.json`


Advantages
----------

* No access to Docker-Socket
* tbc ...


Alternatives
------------

* https://github.com/v2tec/watchtower
* https://engineering.salesforce.com/open-sourcing-dockerfile-image-update-6400121c1a
* https://stackoverflow.com/questions/26423515/how-to-automatically-update-your-docker-containers-if-base-images-are-updated
* tbc ...



