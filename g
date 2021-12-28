

#!/bin/bash


function fuck () {

python2 svmap.py -m INVITE -v -t0.0 $target >>results.txt
}

for target in `cat range.txt`
do 
echo $target 
fuck $target &
sleep 0.3
done
