#!/bin/sh

# temp simple test script before we have a proper testing system

api_url='http://localhost:8000'
user_id='66293465'
# routine_id='91323311'
# workout_id='84396080'

# curl -vL \
#     -X POST \
#     -H 'Content-Type: application/json' \
#     "${api_url}/user/1/workout"

# random="$(echo $RANDOM | md5sum | head -c 8)"
# curl -vL \
#     -X POST \
#     -H 'Content-Type: application/json' \
#     --data "{\"email\": \"${random}@testing.com\", \"name\": \"${random}\", \"password\": \"testing\"}" \
#     "${api_url}/signup"

# curl -vL \
#     -X POST \
#     -H 'Content-Type: application/json' \
#     --data '{"name": "my workout", "workout_type": "bicep_curl", "reps": 10}' \
#     "${api_url}/user/${user_id}/workout"

# workout_id='15317289'
# curl -vL \
#     -X GET \
#     "${api_url}/user/${user_id}/workout"

# curl -vL \
#     -X DELETE \
#     "${api_url}/user/${user_id}/workout/${workout_id}"

# curl -vL \
#     -X POST \
#     -H 'Content-Type: application/json' \
#     --data '{"name": "my routine"}' \
#     "${api_url}/user/${user_id}/routine"

# curl -vL \
#     -X PATCH \
#     -H 'Content-Type: application/json' \
#     --data "{\"workout_id\": ${workout_id}}" \
#     "${api_url}/user/${user_id}/routine/${routine_id}"

curl -vL \
    -X GET \
    "${api_url}/user/${user_id}/routine"
