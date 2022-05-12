import csv
import os
#from importlib.machinery import SourceFileLoader as loader #needed to import NIST sp800-22-tests module

def list_to_int(input_arr):
    for i in range(0, len(input_arr)):
        input_arr[i] = int(input_arr[i])
    return input_arr

def read_input_from_file(foldername, foldername2, filename):
    data_file_path = foldername + "/" + filename
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            #csvreader = csv.reader(file, delimiter=',') #creating a csv reader object
            csvreader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC) #creating a csv reader object (reads the numbers as floats, not as strings)
            for row in csvreader:
                binary_key = row
            file.close() #close file
        print ("The reading process is done!")
    #if the file does not exist, tries to read the file from the other folder
    except FileNotFoundError:
        try:
            print (f"The file {filename} was not found inside {foldername}")
            data_file_path = foldername2 + "/" + filename
            print (f"Trying to check if the file located at: {data_file_path} exists...")
            
            with open(data_file_path, "r") as file: #open file to read
                #csvreader = csv.reader(file, delimiter=',') #creating a csv reader object
                csvreader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC) #creating a csv reader object (reads the numbers as floats, not as strings)
                for row in csvreader:
                    binary_key = row
                file.close() #close file
            print ("Yes, it does.\nThe reading process is done!")
        #if it still not found, prints a message and closes the program
        except FileNotFoundError:
            print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
            exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    finally:
        try:
            binary_key = bytearray(list_to_int(binary_key)) #converts the input array to a bytearray
        except UnboundLocalError:
            print ("An error ocurred during the reading process. Please, check the messages above.")
            exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
        return binary_key

def write_bin_file(binary_key, foldername, filename):
    path = foldername + "/" + filename
    print ("Writing the binary key to the file located at: ", path)
    
    with open(path, "wb") as file:
        file.write(binary_key)
    file.close()
    
    print ("The writing process is done!")

def run_test_module(foldername, filename):
    print ("Running the test module...")
    #os.system("modules/sp800_22_tests/sp800_22_tests.py" + " " + foldername + "/" + filename)
    output = os.popen("modules/sp800_22_tests/sp800_22_tests.py" + " " + foldername + "/" + filename).read()
    print ("The test module is done!")

    return output

def check_key_is_approved(test_output):
    status = test_output.find("FAIL")
    if status == -1:
        print("The key was approved! You are good to go")
    else:
        print("Oh no, the key was NOT approved!")

def main(fileName):
    #key_test_module = loader("sp800_22_tests", "modules/sp800_22_tests/sp800_22_tests.py")
    #updates dynamic variables
    filename = fileName

    #files and paths to be used by the program
    #filename = "DaCruz2021-preliminar1-cut-tab-1" #filename to be used by the program
    file_format = ".csv"
    bin_file_format = ".bin"
    results_foldername = "results"
    keys_foldername = results_foldername + "/" + "key-after-reconciliation" #folder to get the input key
    keys_backup_foldername = results_foldername + "/" + "key-reconciliation" #folder to get the input key
    keys_filename = "keys_" + filename + file_format #filename for the file with the key
    keys_bin_foldername = results_foldername + "/" + "key-evaluation" #folder to get the input key
    keys_bin_filename = "keys_" + filename + bin_file_format #filename for the file with the key

    #execution starts here
    key = read_input_from_file(keys_foldername, keys_backup_foldername, keys_filename) #reads the key from the file
    write_bin_file(key, keys_bin_foldername, keys_bin_filename) #writes the key to a binary file (NOTE: required to be used by the test module)
    test_module_output = run_test_module(keys_bin_foldername, keys_bin_filename) #runs the test module
    #print(test_module_output)
    check_key_is_approved(test_module_output) #checks if the key is approved

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()