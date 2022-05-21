import csv #provides the CSV related functions
import array #provides the array structure datatype (more flexible than the bytearray)
import math #provides the math functions
from importlib.machinery import SourceFileLoader as loader

#definitions of the functions
# returns an array of ints, just for testing purposes
def populate_array(array, max_number):
    for i in range(0, max_number):
        array.append(i % 2)
    return array

def read_key_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    binary_key = []
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
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return binary_key

# returns the next power of 2 (greater than or equal to) of the input value
def get_next_power_of_2(n):
    #funcion adapted from the one contributed by user 'Smitha' on Geekforgeeks
    #source: https://www.geeksforgeeks.org/smallest-power-of-2-greater-than-or-equal-to-n/
    #Time complexity: O(log n)
    
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n += 1
    
    if n < 256: #reeedsolomon_max_length default value is 256, so no need to get values below 256
        return 256
    else:
        return n

#returns an array with the ecc bits
def get_rs_data(rs_encoded_data, ecc_symbols_length):
    #checks if it's possible to use the bytearray structure
    #because bytearrays can only store an element which is below 256
    try:
        ecc = bytearray(b'') #creates an empty bytearray
        bits = bytearray(b'') #creates an empty bytearray
        
        ecc = rs_encoded_data[len(rs_encoded_data) - ecc_symbols_length:] #gets only the ecc_symbols from the array
        bits = rs_encoded_data[:len(rs_encoded_data) - ecc_symbols_length] #gets only the data bits from the array
    
    except ValueError: #if not possible, use the array structure (the same way as the reedsolo module)
        ecc = array.array('i', []) #creates an empty array
        bits = array.array('i', []) #creates an empty array
        
        ecc = rs_encoded_data[len(rs_encoded_data) - ecc_symbols_length:] #gets only the ecc_symbols from the array
        bits = rs_encoded_data[:len(rs_encoded_data) - ecc_symbols_length] #gets only the data bits from the array
    
    return bits,ecc

# converts the elements of (almost) any type from an array to int
def array_to_int(input_arr):
    #int_arr = []
    for i in range(0, len(input_arr)):
        input_arr[i] = int(input_arr[i])
    return input_arr

def write_array_to_file(array, foldername, filename, file_type):
    results_path = foldername + "/" + filename #constructs the path to the file
    if file_type == 0:
        print ("Writing the key to the file located at: ", results_path)
    elif file_type == 1:
        print ("Writing the ECC symbols to the file located at: ", results_path)
    elif file_type == 2:
        print ("Writing the codec parameters to the file located at: ", results_path)
    else:
        print ("Wrong file type chosen!\n Writing process failed.\nExiting...")
        exit(code=2)
    with open(results_path, "w") as file:
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(array) #writing the rows to the file
        file.close()
    print ("The writing process is done!")

# defines the main function
def main(fileName):
    #updates dynamic variables
    filename = fileName

    #env vars declaration
    reedsolomon_module = loader("reedsolo", "modules/reedsolomon/reedsolo.py").load_module()
    reeedsolomon_max_length = 0 #NOTE: this value must be a power of 2. The default is 256.
    reedsolomon_num_correction_symbols = 0 #12 #TODO update this value according to the input
    key = []
    #files and paths to be used by the program
    #filename = "DaCruz2021-preliminar1-cut-tab-1" #filename to be used by the program
    file_format = ".csv"
    results_foldername = "results"
    bit_stream_foldername = results_foldername + "/" + "keys" #folder where the keys were stored
    bit_stream_filename = "bit-stream_" + filename + file_format
    keys_foldername = results_foldername + "/" + "key-reconciliation" #folder to store the produced data (keys + ecc + params) from this step
    #keys_file_format = ".csv" #file format for the results file
    keys_filename = "keys_" + filename + file_format #TODO: comments here
    ecc_filename = "ecc_" + filename + file_format 
    parameters_filename = "parameters_" + filename + file_format 

    #execution starts here
    key = read_key_input_file(bit_stream_foldername, bit_stream_filename) #reads the key from the file
    '''key = []
    key = populate_array(key, 262) #generates a test key with a length of 262 bits'''
    #updates the number of correction symbols according to the input key's length
    reedsolomon_num_correction_symbols = math.ceil(len(key)*2) #NOTE: codec operations only accpet integers and length/2 can return a float number, eg. if len = odd int
    #updates the value of the max length of the codec according to the input key's length
    reeedsolomon_max_length = get_next_power_of_2(len(key) + reedsolomon_num_correction_symbols) #NOTE: length of total message+ecc, as required by the codec ("message" is what we are calling "key" here)
    #converts the array to an integer array (codec operations only accpet integers and CSV files are being read as floats)
    key = array_to_int(key)
    
    #codec encode operations
    reedsolomon_codec = reedsolomon_module.RSCodec(reedsolomon_num_correction_symbols, nsize=(reeedsolomon_max_length-1)) #creates a codec object with desired params
    reedsolomon_array = reedsolomon_codec.encode(key) #encodes the key
    reedsolomon_data_bits, reedsolomon_ecc_symbols = get_rs_data(reedsolomon_array, reedsolomon_num_correction_symbols) #separates the bits from the ecc symbols
    reedsolomon_params = (reedsolomon_num_correction_symbols, reeedsolomon_max_length) #saves the parameters of the codec

    print ("The key is: "                           , key)
    print ("The input's length is: "                , len(key))
    print ("The Reed Solomon message data is: "     , reedsolomon_array)
    print ("The Reed Solomon message's length is: " , len(reedsolomon_array))
    print ("The Reed Solomon data bits are: "       , reedsolomon_data_bits)
    print ("The Reed Solomon data bits' length is: ", len(reedsolomon_data_bits))
    print ("The Reed Solomon ecc bits are: "        , reedsolomon_ecc_symbols)
    print ("The Reed Solomon ecc bits' length is: " , len(reedsolomon_ecc_symbols))
    print ("RS params: "                            , reedsolomon_params)
    reedsolomon_max_errors, reedsolomon_max_erasures = reedsolomon_codec.maxerrata(verbose=True) #gets the max number of errors and erasures

    write_array_to_file(reedsolomon_data_bits, keys_foldername, keys_filename, 0) #writes the key to the file
    write_array_to_file(reedsolomon_ecc_symbols, keys_foldername, ecc_filename, 1) #writes the ecc symbols to the file
    write_array_to_file(reedsolomon_params, keys_foldername, parameters_filename, 2) #writes the codec params to the file

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()