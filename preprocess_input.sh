#!/bin/sh
: ' This is bash program to filter the data
   and remove any char that is not a number
   but keeping the negative numbers intact
  '

# script vars
#var to store the uptaded working path
path=$(pwd)
#vars that stores the search patterns to be applied
search_pattern_float="-[0-9]|-[0-9][0-9]|-[0-9][0-9][0-9]" #filters any numbers with 1, 2 or 3 digits
search_pattern_int="-[0-9]$|-[0-9][0-9]$|-[0-9][0-9][0-9]$" #forces filtering only numbers with 1, 2 or 3 digits #NOTE this does NOT work with floats
search_pattern=$search_pattern_float #selects the desired pattern #TODO make this configurable through ARGS

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
  echo $0 "input.csv -t"
  echo $0 "input.csv -t -c 2"
  echo $0 "input.csv -t -s '\n'"
  echo $0 "input.csv -t -c 2 -s '\n'"
  echo $0 "input.csv -o output.csv"
  echo $0 "input.csv -o output.csv -c 1"
  echo $0 "input.csv -o output.csv -s '\t'"
  echo $0 "input.csv -o output.csv -c 1 -s '\t'"
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
      awk -F $7 '/'$search_pattern'/{print $'$5'}' $1 > $3
      print_Sucessful_Save $3
    else
      print_Error_Args
    fi
  elif [ "$4" == "-c" ] || [ "$4" == "--column" ] && [ $# -eq 5 ]; then #checks if the parameters are correct
    awk '/'$search_pattern'/{print $'$5'}' $1 > $3
    print_Sucessful_Save $3
  elif [ "$4" == "-s" ] || [ "$4" == "--separator" ] && [ $# -eq 5 ]; then #checks if the parameters are correct
    awk -F $5 '/'$search_pattern'/{print}' $1 > $3
    print_Sucessful_Save $3
  else
    print_Error_Args
  fi
}

option_Column_and_Separator()
{
  if [ "$3" == "-c" ] || [ "$3" == "--column" ] && [ $# -eq 6 ]; then #checks if the parameters are correct
    if [ "$5" == "-s" ] || [ "$5" == "--separator" ]; then #continues checking if the parameters are correct
      awk -F $6 '/'$search_pattern'/{print $'$4'}' $1
    else
      print_Error_Args
    fi
  elif [ "$3" == "-c" ] || [ "$3" == "--column" ] && [ $# -eq 4 ]; then #checks if the parameters are correct
    awk '/'$search_pattern'/{print $'$4'}' $1
  elif [ "$3" == "-s" ] || [ "$3" == "--separator" ] && [ $# -eq 4 ]; then #checks if the parameters are correct
    awk -F $4 '/'$search_pattern'/{print}' $1
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
    # my_help
    exit 1
  fi
  
  #tests which execution flow to execute
  case "$2" in
    -o|--output)
      if [ $# -eq 3 ]; then
        awk '/'$search_pattern'/{print}' $1 > $3 #filters negative numbers with 1, 2 or 3 digits
        print_Sucessful_Save $3
      else
        option_Column_and_Separator_with_Save $@ #$@ sends all the ARGS from main to the function scope
      fi
      ;;
    -t|--test)
      echo "WARNING: Test mode is enabled"
      if [ $# -eq 2 ]; then
        awk '/'$search_pattern'/{print}' $1 #filters negative numbers with 1, 2 or 3 digits
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