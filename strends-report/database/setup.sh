#!/bin/bash
set -e

/etc/init.d/postgresql start
psql -f create_fixtures.sql
/etc/init.d/postgresql stop