#!/bin/sh
# This is bash program to filter the data
# and remove any char that is not a number
# but keeping the negative numbers intact

path=$(pwd) # var to store the uptaded path

# Help function, displays the usage of the script
Help()
{
  echo "Usage:"
  echo $0 "input_file_name [options]"
  echo "Options:"
  echo "-t  --test     Enables the test mode (only displays the result on stdout)"
  echo "-o  --output   Specifies the output file where results will be saved"
  echo "Examples:"
  echo $0 "input.txt -t"
  echo $0 "input.txt -o output.txt"
  exit
}

# Main functionality
case "$2" in
  -o|--output)
    awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1 >> $3 #filters only negative numbers with 2 or 3 digits
    echo "The preprocessed results were saved at" $path"/"$3
    ;;
  -t|--test)
    echo "WARNING: Test mode is enabled"
    awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1 #filters only negative numbers with 2 or 3 digits
    echo "CAUTION: This is only a preview, the results were NOT saved yet"
    ;;
  *)
    Help
esac
