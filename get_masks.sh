#!/bin/bash

mkdir -p ./OID/
cd ./OID/

mkdir -p ./masks/
cd ./masks/
mkdir -p ./zips/

for NUM in 0 1 2 3 4 5 6 7 8 9 a b c d e f
do
	mkdir -p ./0$NUM/

	# 	FIXME UNCOMMENT BELOW TO DOWNLOAD TEST/TRAIN
	for SET in validation # test train
	do
		wget https://storage.googleapis.com/openimages/v5/$SET-masks/$SET-masks-$NUM.zip

		echo -n Unzipping $SET: $NUM...
		unzip -n -d ./0$NUM/ $SET-masks-$NUM.zip | awk 'BEGIN {ORS="."} {if(NR%150==0)print "."}'
		echo ''
		mv $SET-masks-$NUM.zip ./zips/
	done
done
