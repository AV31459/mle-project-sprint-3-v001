#!/bin/bash

[ ! -f .env ] || export $(grep -v '^#' .env | xargs)

PORT=${1:-$APP_PORT_EXTERNAL}

echo -n Using app port:
echo $PORT

echo Ping http://localhost:$PORT/healthcheck...
echo -n Response: 
curl http://localhost:$PORT/healthcheck
echo
echo Testing http://localhost:$PORT/predict...
echo -n Response: 
curl -X POST http://localhost:$PORT/predict -H "Content-Type: application/json" -d "@tests/request_example.json"
echo