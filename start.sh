#!/bin/bash
mkdir ./volumes/grafana
mkdir ./volumes/grafana/data
#mkdir ./volumes/grafana/configs
mkdir ./volumes/redis
mkdir ./volumes/influxdb
mkdir ./volumes/influxdb/data
mkdir ./volumes/influxdb/config
cd compose
docker-compose up --build
