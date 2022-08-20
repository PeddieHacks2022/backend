#!/bin/sh

# temp simple test script before we have a proper testing system

api_url='http://localhost:5000'
user_token=''

# curl -vL \
#     -X POST \
#     -H 'Content-Type: application/json' \
#     "${api_url}/user/1/workout"

random="$(echo $RANDOM | md5sum | head -c 8)"
curl -vL \
    -X POST \
    -H 'Content-Type: application/json' \
    --data "{\"email\": \"${random}@testing.com\", \"name\": \"${random}\", \"password\": \"testing\"}" \
    "${api_url}/signup"
