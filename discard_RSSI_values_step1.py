import csv #provides the CSV related functions

#env vars declaration
RSSI_values = []
RSSI_index_values = []
RSSI_new_values = []
binary_bit_sequence = ""
new_key = []
#files and paths to be used by the program
filename = "DaCruz2021-preliminar1-cut-tab-2_alpha-1" #filename to be used by the program
file_format = ".csv"
results_foldername = "results"
bit_sequence_foldername = results_foldername + "/" + "bit-sequence" #folder to get the results from
bit_sequence_filename = "bit-sequence_" + filename + file_format #filename of the bit sequence file
data_file_foldername = "dataset-files" #folder where the data files are stored
data_file_filename = filename + file_format #filename of the data file
discard_foldername = results_foldername + "/" + "discard" #folder to store the results
discard_filename = "discard-indexes_" + filename + file_format #filename for the file with results
values_after_discard_foldername = discard_foldername #folder to store the new list of RSSI values
values_after_discard_filename = "new-RSSI_" + filename + file_format #filename for the file with results
new_key_foldername = results_foldername + "/" + "keys"
new_key_filename = "key_" + filename + file_format

#definitions of the functions
'''def read_RSSI_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    vet_RSSI_values = []
    print ("Reading the file located at: " + str(data_file_path))
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            csvreader = csv.reader(file) #creating a csv reader object
            i = 0
            for row in csvreader:
                #print (row)
                for i in range(0, len(row)):
                    vet_RSSI_values.append(float(row[i])) #TODO check if float is okay here
                    #vet_RSSI_values.append(row[i]) #TODO check if float is okay here
            file.close() #close file
        print ("The reading process is done!")
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return vet_RSSI_values'''

def read_binary_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    binary_bits = []
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            csvreader = csv.reader(file, delimiter=',') #creating a csv reader object
            #csvreader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC) #creating a csv reader object (reads the numbers as floats, not as strings)
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

# returns the indexes of the RSSI values that are going to be discarded
def get_index_values(RSSI_values):
    index_values = []
    index = 0
    for i in range(0, len(RSSI_values)):
        if int(RSSI_values[i]) == 2: #checks if the value i of RSSI_values is 2
            index_values.append(int(index)) #if yes, adds the index to the list of indexes
            #print ("Index value: " + str(index))
        index += 1
    #print (str(len(RSSI_values)) + " values were read.")
    return index_values

# returns only the RSSI values that will be used
'''def erase_RSSI_values(RSSI_values, vet_discard_indexes):
    RSSI_values_copy = RSSI_values.copy() #copy the list of RSSI values to prevent modifying the original list
    RSSI_clean_values = []
    #flags all values to be discarded
    for i in range(0, len(vet_discard_indexes)):
        RSSI_values_copy[vet_discard_indexes[i]] = -1
    #removes the discarded values from the list
    for i in range(0, len(RSSI_values_copy)):
        if RSSI_values_copy[i] != -1:
            RSSI_clean_values.append(RSSI_values_copy[i])
    return RSSI_clean_values'''

def generates_new_key(bits):
    new_key = []
    for i in range(0, len(bits)):
        if bits[i] != "2":
            new_key.append(bits[i])
        #else:
         #   new_key += "0"
    return new_key

def write_indexes_to_file(vet_discard_indexes, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the discard indexes to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(vet_discard_indexes) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

def write_RSSI_values_to_file(RSSI_values, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the new RSSI values to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(RSSI_values) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

def write_new_key_to_file(key, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the new key to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(key) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

# defines the main function
def main():
    #execution starts here
    #RSSI_values = read_RSSI_input_file(data_file_foldername, data_file_filename) #loads the RSSI values from the file
    binary_bit_sequence = read_binary_input_file(bit_sequence_foldername, bit_sequence_filename) #loads the binary bit sequence from the file
    RSSI_index_values = get_index_values(binary_bit_sequence) #gets the index values of the RSSI values to discard
    #RSSI_new_values = erase_RSSI_values(RSSI_values, RSSI_index_values) #erases the RSSI values that are going to be discarded
    #new_key = generates_new_key(binary_bit_sequence) #generates the new key

    #status report, just to check if everything is ok (for testing purposes)
    #print ("The RSSI values are: ", RSSI_values)
    print ("The bit sequence is: ",  binary_bit_sequence)
    print ("The indexes of RSSI values to discard are: ", RSSI_index_values)
    #print ("The new RSSI values are: ", RSSI_new_values)
    #print ("The new key is: ", new_key)

    # saves the results to a file
    write_indexes_to_file(RSSI_index_values, discard_foldername, discard_filename)
    #write_RSSI_values_to_file(RSSI_new_values, values_after_discard_foldername, values_after_discard_filename) #done for testing purposes
    #write_new_key_to_file(new_key, new_key_foldername, new_key_filename)

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()