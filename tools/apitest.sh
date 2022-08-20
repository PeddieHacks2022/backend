#!/bin/sh

# temp simple test script before we have a proper testing system

api_url='http://localhost:5000'
user_token=''

curl -vL \
    -X POST \
    -H 'Content-Type: application/json' \
    "${api_url}/user/1/workout"

curl -vL \
    -X POST \
    -H 'Content-Type: application/json' \
    --data '{"email": "testing@testing.com", "name": "testing", "password": "testing"}' \
    "${api_url}/signup"
