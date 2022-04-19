#!/bin/bash
chown -R root:root ./data/grafana
cd compose
docker-compose up --build
