#!/bin/sh
: ' This is bash program to filter the data
   and remove any char that is not a number
   but keeping the negative numbers intact
  '

path=$(pwd) # var to store the uptaded path
#TODO Filter lines with only one digit
# Help function, displays the usage of the script
my_help()
{
  echo #new line
  echo "Usage:"
  echo $0 "input_file_name [options]"
  echo #new line
  echo "Options:"
  echo "-t  --test        Enables the test mode (only displays the result on stdout)"
  echo "-o  --output      Specifies the output file where results will be saved (WARNING: it will overwrite the file specified by this param)"
  echo "-c  --column      Specifies which column to get data from (default is 0, which prints all columns)"
  echo "-s  --separator   Specifies which separator to use when reading data (defaults to SPACE)"
  echo #new line
  echo "Examples:"
  echo $0 "input.txt -t"
  echo $0 "input.txt -t -c 2"
  echo $0 "input.txt -t -s '\n'"
  echo $0 "input.txt -t -c 2 -s '\n'"
  echo $0 "input.txt -o output.txt"
  echo $0 "input.txt -o output.txt -c 1"
  echo $0 "input.txt -o output.txt -s '\t'"
  echo $0 "input.txt -o output.txt -c 1 -s '\t'"
  exit
}

# prints an error message to stderr
err()
{
    echo "E: $*" >>/dev/stderr
}

print_Sucessful_Save()
{
  echo "The preprocessed results were saved at" $path"/"$1
}

print_Error_Args()
{
  err "Error processing options... Please check them and try again"
  my_help
}

option_Column_and_Separator_with_Save()
{
  if [ "$4" == "-c" ] || [ "$4" == "--column" ] && [ $# -eq 7 ]; then #checks if the parameters are correct
    if [ "$6" == "-s" ] || [ "$6" == "--separator" ]; then #continues checking if the parameters are correct
      awk -F $7 '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print $'$5'}' $1 > $3
      print_Sucessful_Save $3
    else
      print_Error_Args
    fi
  elif [ "$4" == "-c" ] || [ "$4" == "--column" ] && [ $# -eq 5 ]; then #checks if the parameters are correct
    awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print $'$5'}' $1 > $3
    print_Sucessful_Save $3
  elif [ "$4" == "-s" ] || [ "$4" == "--separator" ] && [ $# -eq 5 ]; then #checks if the parameters are correct
    awk -F $5 '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1 > $3
    print_Sucessful_Save $3
  else
    print_Error_Args
  fi
}

option_Column_and_Separator()
{
  if [ "$3" == "-c" ] || [ "$3" == "--column" ] && [ $# -eq 6 ]; then #checks if the parameters are correct
    if [ "$5" == "-s" ] || [ "$5" == "--separator" ]; then #continues checking if the parameters are correct
      awk -F $6 '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print $'$4'}' $1
    else
      print_Error_Args
    fi
  elif [ "$3" == "-c" ] || [ "$3" == "--column" ] && [ $# -eq 4 ]; then #checks if the parameters are correct
    awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print $'$4'}' $1
  elif [ "$3" == "-s" ] || [ "$3" == "--separator" ] && [ $# -eq 4 ]; then #checks if the parameters are correct
    awk -F $4 '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1
  else
    print_Error_Args
  fi
}

# Main functionality
main()
{
  #checks if the number of ARGS are ok
  if [ $# -lt 2 ]; then
    err "Not enough ARGS!"
  elif [ $# -gt 7 ]; then
    err "Too many ARGS!"
  elif [ ! -s $1 ]; then
    err "File $1 not found!"
    my_help
  fi
  
  #tests which execution flow to execute
  case "$2" in
    -o|--output)
      if [ $# -eq 3 ]; then
        awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1 > $3 #filters only negative numbers with 2 or 3 digits
        print_Sucessful_Save $3
      else
        option_Column_and_Separator_with_Save $@ #$@ sends all the ARGS from main to the function scope
      fi
      ;;
    -t|--test)
      echo "WARNING: Test mode is enabled"
      if [ $# -eq 2 ]; then
        awk '/-[0-9][0-9]$|-[0-9][0-9][0-9]$/{print}' $1 #filters only negative numbers with 2 or 3 digits
      else
        option_Column_and_Separator $@ #$@ sends all the ARGS from main to the function scope
      fi
      echo "CAUTION: This is only a preview, the results were NOT saved yet"
      ;;
    *)
      print_Error_Args
  esac
}

main $@ #calls the program's main function