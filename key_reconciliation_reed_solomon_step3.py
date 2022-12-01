import csv #provides the CSV related functions
import array #provides the array structure datatype (more flexible than the bytearray)
from importlib.machinery import SourceFileLoader as loader #required to load the reedsolo module

# returns an array of ints, just for testing purposes
def populate_array(array, max_number):
    for i in range(0, max_number):
        array.append(i % 2)
    return array

def read_input_file(foldername, filename):
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
    
    if n < 256: #reeedsolomon_max_length default value is 256, so no need to have values below 256
        return 256
    else:
        return n

#returns a tuple containing payload data and ecc bits
def get_payload_and_ecc_symbols(rs_encoded_data, ecc_symbols_length):
    #checks if it's possible to use the bytearray structure
    #because bytearrays can only store an element which is lower than 256
    try:
        ecc = bytearray(b'') #creates an empty bytearray
        payload = bytearray(b'') #creates an empty bytearray
        payload = rs_encoded_data[0:len(rs_encoded_data) - ecc_symbols_length]
        ecc = rs_encoded_data[len(rs_encoded_data) - ecc_symbols_length:]
    
    except ValueError: #if not possible, use the array structure (the same way as the reedsolo module)
        ecc = array.array('i', []) #creates an empty array
        payload = array.array('i', []) #creates an empty array
        payload = rs_encoded_data[0:len(rs_encoded_data) - ecc_symbols_length]
        ecc = rs_encoded_data[len(rs_encoded_data) - ecc_symbols_length:]
    
    return (payload, ecc)

# converts the elements of (almost) any type from an array to int
def array_to_int(input_arr):
    for i in range(0, len(input_arr)):
        input_arr[i] = int(input_arr[i])
    return input_arr

def write_output_to_file(array, foldername, filename):
    results_path = foldername + "/" + filename #constructs the path to the file
    print ("Writing the reconciliated key to the file located at: ", results_path)

    with open(results_path, "w") as file:
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(array) #writing the rows to the file
        file.close()
    print ("The writing process is done!")

# defines the main function
def main(fileName, fileName2):
    #updates dynamic variables
    filename = fileName #filename to be used by the program
    filename2 = fileName2 #filename to be used by the program

    #env vars declaration
    reedsolomon_module = loader("reedsolo", "modules/reedsolomon/reedsolo.py").load_module()
    reeedsolomon_max_length = 0 #NOTE: this value must be a power of 2. The default is 256.
    reedsolomon_num_correction_symbols = 0 
    key = []
    #files and paths to be used by the program
    file_format = ".csv"
    results_foldername = "results"
    #bit_stream_foldername = results_foldername + "/" + "keys" #folder where the keys were stored
    #bit_stream_filename = "bit-stream_" + filename + file_format
    keys_foldername = results_foldername + "/" + "key-reconciliation" #folder to get the data from
    keys_filename = "keys_" + filename + file_format #TODO: comments here
    ecc_filename = "ecc_" + filename2 + file_format 
    parameters_filename = "parameters_" + filename + file_format
    output_keys_foldername = results_foldername + "/" + "key-after-reconciliation" #folder to store the data
    output_keys_filename = "keys_" + filename + file_format #TODO: comment here

    #execution starts here
    key = read_input_file(keys_foldername, keys_filename) #reads the key from the file
    ecc = read_input_file(keys_foldername, ecc_filename) #reads the ecc bits from the file
    reedsolomon_parameters = read_input_file(keys_foldername, parameters_filename) #reads the codec parameters from the file
    
    key = array_to_int(key) #converts the array to an integer array (codec operations only accpet integers and CSV files is being read as floats)
    ecc = array_to_int(ecc) #converts the elements of the array to int
    reedsolomon_parameters = array_to_int(reedsolomon_parameters) #converts the elements of the array to int
    #updates the RS codec parameters
    reedsolomon_num_correction_symbols = reedsolomon_parameters[0]
    reeedsolomon_max_length = reedsolomon_parameters[1]
    
    #print("The key was: ", key, len(key), len(ecc), reedsolomon_num_correction_symbols, reeedsolomon_max_length) #NOTE: uncomment this line to see more information on screen
    print("The key was: ", key) #prints the key, just for debug purposes

    #codec operations
    reedsolomon_codec = reedsolomon_module.RSCodec(reedsolomon_num_correction_symbols, nsize=(reeedsolomon_max_length-1)) #creates a codec object with desired params
    reedsolomon_payload = key + ecc #generates the payload (NOTE: payload or message is the key + ecc symbols or data + ecc symbols)
    print("The RS payload is: ", reedsolomon_payload) #prints the payload #DEBUG
    print("The RS payload length is: ", len(reedsolomon_payload)) #prints the payload length #DEBUG
    reedsolomon_array = reedsolomon_codec.decode(reedsolomon_payload) #decodes the key with corrections (if any) applied

    print ("-After decoding-") #DEBUG
    print ("RS retrieved data is: ", list(reedsolomon_array[0])) #prints the decoded data (with corrections applied if any) #DEBUG
    #print ("RS payload is: ", reedsolomon_payload) #prints the payload #DEBUG
    print ("RS ecc bits are: ", ecc) #displays the ecc symbols #DEBUG
    print ("RS no. of bytes corrected: ", list(reedsolomon_array[2])) #corrections made (it displays which byte was corrected aka byte position index) #DEBUG
    
    write_output_to_file(list(reedsolomon_array[0]), output_keys_foldername, output_keys_filename) #writes the corrected key to the file

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()