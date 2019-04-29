#! /bin/bash
echo "Initializing Tables..."

docker create --name strends_data alpine \
    -v "/var/lib/postgresql/data"

echo "Tables Initialized..."