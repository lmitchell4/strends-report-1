#! /bin/bash
docker run --name strends_psql \
    -e POSTGRES_USER=usr \
    -e POSTGRES_DB=strends \
    -p 5432:5432 \
	-d --volumes-from strends_data postgres