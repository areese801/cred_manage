#!/bin/bash

###
### Just a script to run all of our test cases 
###

thisDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
localPython="${thisDir}/virtualenv/bin/python"
testsDir="${thisDir}/tests"

for f in $(ls ${testsDir}/*_test.py)
do
	${localPython} -m unittest ${f}
done	

