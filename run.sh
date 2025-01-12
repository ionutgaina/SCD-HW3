#! /bin/bash

docker swarm init

export SCD_DVP=/var/lib/docker/volumes

docker compose -f stack.yml build
docker stack deploy -c stack.yml scd3