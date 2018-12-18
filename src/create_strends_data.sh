#! /bin/bash
docker create --name strends_data alpine \
    -v "/var/lib/postgresql/data"
