import csv #provides the CSV related functions

#env vars declaration
RSSI_values = []
RSSI_index_values = []
RSSI_index_values2 = []
RSSI_new_values = []
binary_bit_sequence = ""
binary_bit_sequence_discard_indexes = ""
new_key = []
#files and paths to be used by the program
filename = "DaCruz2021-preliminar1-cut-tab-1_alpha-0.1" #filename to be used by the program
file_format = ".csv"
results_foldername = "results"
bit_sequence_foldername = results_foldername + "/" + "bit-sequence" #folder to get the results from
bit_sequence_filename = "bit-sequence_" + filename + file_format #filename of the bit sequence file
#data_file_foldername = "dataset-files" #folder where the data files are stored
#data_file_filename = filename #filename of the data file
discard_foldername = results_foldername + "/" + "discard" #folder to store the results
discard_filename = "discard-indexes_" + "DaCruz2021-preliminar1-cut-tab-2_alpha-0.1" + file_format #filename for the file with results
discard_filename2 = "discard-indexes_" + filename + file_format #filename for the file with results
#key_foldername = results_foldername + "/" + "keys"
#key_filename = "key_" + filename
new_key_foldername = results_foldername + "/" + "keys"
new_key_filename = "bit-stream_" + filename + file_format


#definitions of the functions
def read_binary_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    binary_bits = []
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            #csvreader = csv.reader(file, delimiter=',') #creating a csv reader object
            csvreader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC) #creating a csv reader object (reads the numbers as floats, not as strings)
            #binary_bits = file.readline() #read the file
            for row in csvreader:
                #print (row)
                binary_bits = row
            file.close() #close file
        print ("The reading process is done!")
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return binary_bits

def array_to_int(input_arr):
    for i in range(0, len(input_arr)):
        input_arr[i] = int(input_arr[i])
    return input_arr

def union_of_arrays(array1, array2):
    return list(set(array1) | set(array2))

def erase_bit_values(bit_values, arr_discard_indexes):
    bit_values_copy = bit_values.copy() #copies the list of RSSI values to prevent modifying the original list
    bit_values_clean = []
    #flags all values to be discarded
    for i in range(0, len(arr_discard_indexes)):
        bit_values_copy[arr_discard_indexes[i]] = -1
    #removes the discarded values from the list
    for i in range(0, len(bit_values_copy)):
        if bit_values_copy[i] != -1:
            bit_values_clean.append(bit_values_copy[i])
    return bit_values_clean

def write_new_key_to_file(key, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the final key to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(key) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

def main():
    # execution starts here
    #read input files
    RSSI_index_values = read_binary_input_file(discard_foldername, discard_filename)
    RSSI_index_values2 = read_binary_input_file(discard_foldername, discard_filename2)
    binary_bit_sequence = read_binary_input_file(bit_sequence_foldername, bit_sequence_filename)
    #convert the arrays to integers
    RSSI_index_values = array_to_int(RSSI_index_values)
    RSSI_index_values2 = array_to_int(RSSI_index_values2)
    binary_bit_sequence = array_to_int(binary_bit_sequence)
    
    print ("The old key is: ", binary_bit_sequence) #displays the old key
    
    binary_bit_sequence_discard_indexes = union_of_arrays(RSSI_index_values, RSSI_index_values2) #get all the indexes of the values to be discarded
    binary_bit_sequence = erase_bit_values(binary_bit_sequence, binary_bit_sequence_discard_indexes) #erase the bit values that are not needed

    #print ("The binary bit discard indexes are: ", binary_bit_sequence_discard_indexes) #displays the indexes of the values to be discarded
    print ("The new key is: ", binary_bit_sequence) #displays the new key

    write_new_key_to_file(binary_bit_sequence, new_key_foldername, new_key_filename) #writes the new key to a file

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()