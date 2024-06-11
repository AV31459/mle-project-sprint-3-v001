#!/bin/bash

[ ! -f .env ] || export $(grep -v '^#' .env | xargs)

SERVICE=${1:-"$HOST_EXTERNAL:$APP_PORT_EXTERNAL"}

echo ---------------------------------
echo -n "Targeting service at: "
echo $SERVICE
echo ---------------------------------
echo ">>> Request (GET) : curl http://$SERVICE/healthcheck"
echo -n "<<< Response: "
curl http://$SERVICE/healthcheck
echo
echo ----------------------------------
echo ">>> Request (POST): curl -X POST http://$SERVICE/predict <...>"
echo -n "<<< Response: "
curl -X POST http://$SERVICE/predict -H "Content-Type: application/json" -d "@tests/request_example.json"
echo
echo ----------------------------------