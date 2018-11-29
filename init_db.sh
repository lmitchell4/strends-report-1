#! /bin/bash
docker run --name strends_db \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_USER=usr \
    -e POSTGRES_DB=strends \
    -p 5432:5432 \
    -d postgres