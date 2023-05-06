#!/bin/sh

#
# This script converts the CSV key files to a TXT file that is directly
# readable by the NIST test suite installed in the modules folder
#

# Vars
#define the ranges
#NOTE: LC_NUMERIC=en_US.UTF-8 forces the var to behave in a way that seq uses dot (not comma) as decimal separator
range1=$( LC_NUMERIC=en_US.UTF-8 seq $2 0.1 $3)
range2=$(seq $4 $5)
#var to store the script path
path=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

# Runs the sed utility and saves the result
for i in $range1 ; do
    for j in $range2 ; do
        sed 's/,//g' $path/keys_$1_alpha-$i\_m-$j.csv > $path/keys_$1_alpha-$i\_m-$j.txt # this sed command removes all the commas from the input
    done
done

# Vars explanation
# $1 is the file name
# $2 and $3 define the alpha range
# $4 and $5 define the m range


# References used
# https://stackoverflow.com/questions/23884934/seq-uses-comma-as-decimal-separator
# https://codefather.tech/blog/bash-get-script-directory/

