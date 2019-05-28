#!/bin/bash
ROOTDIR=$(cd "$(dirname "$0")" ; pwd -P)
PROJECT_NAME="MediaMachinery"
DOCKER_LOGS="True"

function stop_docker() {
    echo Stopping Containers...
    docker-compose --project-name ${PROJECT_NAME} \
        -f ${ROOTDIR}"/compose-mediamachinery.yml" \
        down --remove-orphans
}

function start_docker() {
    echo Starting Containers...
    docker-compose --project-name ${PROJECT_NAME} \
        -f ${ROOTDIR}"/compose-mediamachinery.yml" \
        up --force-recreate -d --remove-orphans
    if [[ ${DOCKER_LOGS} == "True" ]]; then
        docker-compose --project-name ${PROJECT_NAME} \
        -f ${ROOTDIR}"/compose-mediamachinery.yml" \
        logs -f &
    fi
    sleep 60
    echo "Jackett:      http://localhost:9117"
    echo "Radarr:       http://localhost:7878"
    echo "Sonarr:       http://localhost:8989"
    echo "Bazarr:       http://localhost:6767"
    echo "Emby:         http://localhost:8096"
    echo "Transmission: http://localhost:9091"
    echo "FileBrowser:  http://localhost:1000"
    echo "Portainer:    http://localhost:9000"
}


if [[ "$1" = "start" ]]; then
    DOCKER_LOGS="True"
    start_docker
    exit
elif [[ "$1" = "stop" ]]; then
    stop_docker
    exit
else
    echo "ERROR: Either 'start' or 'stop' need to be provided as argument"
fi
