import csv #provides the CSV related functions
import array #provides the array structure datatype (more flexible than the bytearray)
from importlib.machinery import SourceFileLoader as loader #needed to import reedsolo module

#env vars declaration
reedsolomon_module = loader("reedsolo", "modules/reedsolomon/reedsolo.py").load_module()
reeedsolomon_max_length = 0 #NOTE: this value must be a power of 2. The default is 256.
reedsolomon_num_correction_symbols = 12 #TODO adaptar esse valor de acordo com o tamanho da chave
#RSSI_values = []
#RSSI_index_values = []
#RSSI_new_values = []
key = []
#files and paths to be used by the program
filename = "DaCruz2021-preliminar1-cut-tab-1" #filename to be used by the program
file_format = ".csv"
results_foldername = "results"
bit_stream_foldername = results_foldername + "/" + "keys" #folder where the keys were stored
bit_stream_filename = "bit-stream_" + filename + file_format
keys_foldername = results_foldername + "/" + "keys-after-reconciliation" #folder to get the new list of RSSI values
keys_filename = "keys_" + filename #filename for the file with results
ecc_filename = "ecc_" + filename #filename for the file with results

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
    
    if n < 256: #reeedsolomon_max_length default value is 256, so no need to have values below 256
        return 256
    else:
        return n

#returns an array with the ecc bits
def get_ecc_symbols(rs_encoded_data, ecc_symbols_length):
    #checks if it's possible to use the bytearray structure
    #because bytearrays can only store an element which is lower than 256
    try:
        ecc = bytearray(b'') #creates an empty bytearray
        get_ecc_symbols_aux(rs_encoded_data, ecc_symbols_length, ecc)
    
    except ValueError: #if not possible, use the array structure (the same way as the reedsolo module)
        ecc = array.array('i', []) #creates an empty array
        get_ecc_symbols_aux(rs_encoded_data, ecc_symbols_length, ecc)
    
    return ecc

def get_ecc_symbols_aux(rs_encoded_data, ecc_symbols_length, array_ecc):
    array_length = len(rs_encoded_data)
    for i in range((array_length - ecc_symbols_length), array_length):
        array_ecc.append(rs_encoded_data[i])
    return array_ecc

# converts the elements of (almost) any type from an array to int
def array_to_int(input_arr):
    #int_arr = []
    for i in range(0, len(input_arr)):
        #int_arr.append(int(string_arr[i]))
        input_arr[i] = int(input_arr[i])
    return input_arr

def write_array_to_file(array, foldername, filename, is_ecc_data):
    results_path = foldername + "/" + filename
    if is_ecc_data:
        print ("Writing the ECC symbols to the file located at: ", results_path)
    else:
        print ("Writing the key to the file located at: ", results_path)
    
    if type(array) is bytearray:
        with open(results_path, "wb") as file: #open file to write
            for i in range(0, len(array)):
                file.write(bytes([array[i]]))
            file.close() #close file
    else:
        with open(results_path + ".csv", "w") as file:
            csvwriter = csv.writer(file) #creating a csv writer object 
            csvwriter.writerow(array) #writing the rows to the file
            file.close()
    print ("The writing process is done!")

# defines the main function
def main():
    #execution starts here
    #key = read_key_input_file(bit_stream_foldername, bit_stream_filename) #reads the key from the file
    key = []
    key = populate_array(key, 262) #'''
    reeedsolomon_max_length = get_next_power_of_2(len(key)) #updates the value of the max length of the codec according to the input key length
    key = array_to_int(key) #converts the array to an integer array (codec operations only accpet integers and CSV files is being read as floats)

    reedsolomon_codec = reedsolomon_module.RSCodec(reedsolomon_num_correction_symbols, nsize=(reeedsolomon_max_length-1)) #creates a codec object with desired params
    reedsolomon_array = reedsolomon_codec.encode(key) #encodes the key
    reedsolomon_array[1] = 0 #introduces an error in the array
    reedsolomon_ecc_symbols = get_ecc_symbols(reedsolomon_array, reedsolomon_num_correction_symbols) #gets the ecc symbols
    reedsolomon_data = reedsolomon_codec.decode(reedsolomon_array) #decodes the key with corrections (if any) applied

    print ("The Reed Solomon data is: ", reedsolomon_array)
    print ("The Reed Solomon ecc bits are: ", reedsolomon_ecc_symbols)
    print ("-After decoding-")
    print ("RS retrieving the data: ", list(reedsolomon_data[0])) #array of the data
    print ("RS data: ", reedsolomon_data[1]) #array of the data with ecc bits
    print ("RS bytes corrected: ", list(reedsolomon_data[2])) #corrections made (it displays which byte was corrected)'''

    write_array_to_file(reedsolomon_array, keys_foldername, keys_filename, False) #writes the key to the file
    write_array_to_file(reedsolomon_ecc_symbols, keys_foldername, ecc_filename, True) #writes the ecc symbols to the file

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()