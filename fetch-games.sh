#!/usr/bin/env bash

LICHESS_API_TOKEN=`cat .api-token`
curl "https://lichess.org/api/games/user/pigeonpal?rated=true&perfType=ultraBullet,bullet,blitz,rapid,classical,correspondence&pgnInJson=true&clocks=true&evals=true&opening=true" -H "Authorization: Bearer $LICHESS_API_TOKEN" -H "Accept: application/x-ndjson"
