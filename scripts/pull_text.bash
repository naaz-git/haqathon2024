#!/bin/bash

export CURRENT_TIME=$(date +%Y%m%d%H%M%S)

if [ ! -d $1 ]; then
	echo "creating temporary directory: $1"
	mkdir $1
fi

curl -u alexander.j.freddo@gmail.com:ATATT3xFfGF0SxAQa0zb4p-QH5MCWzCxrNJ_CKgijQH_gWK4hT5XKdyET1M47dJQvDLSBTAw3ggV5TqFuZE4Zko2jnVz6FcY4cx1nYftG6LOFOl9hGu94JSRSNtdX_-kkJHaq1lLowACDCdcQ5myNt77deU2Aeip6B40jmpldVBaSNGDnm5Q4K8=5B83E0D1 $2 |
python3 -mjson.tool > $1/num$3_raw_$CURRENT_TIME.json
