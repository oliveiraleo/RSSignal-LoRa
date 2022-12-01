import csv #provides the CSV related functions

#definitions of the functions
def read_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    binary_bits = []
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            csvreader = csv.reader(file, delimiter=',') #creating a csv reader object
            #csvreader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC) #creating a csv reader object (reads the numbers as floats, not as strings)
            for row in csvreader:
                #print (row) #DEBUG
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
            #print ("Index value: " + str(index)) #DEBUG
        index += 1
    #print (str(len(RSSI_values)) + " values were read.") #DEBUG
    return index_values

def write_indexes_to_file(vet_discard_indexes, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the discard indexes to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(vet_discard_indexes) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

# defines the main function
def main(fileName):
    #updates dynamic variables
    filename = fileName #filename to be used by the program

    #env vars declaration
    RSSI_index_values = []
    binary_bit_sequence = ""
    
    #files and paths to be used by the program
    file_format = ".csv"
    results_foldername = "results"
    bit_sequence_foldername = results_foldername + "/" + "bit-sequence" #folder to get the results from
    bit_sequence_filename = "bit-sequence_" + filename + file_format #filename of the bit sequence file
    discard_foldername = results_foldername + "/" + "discard" #folder to store the results
    discard_filename = "discard-indexes_" + filename + file_format #filename for the file with results

    #execution starts here
    binary_bit_sequence = read_input_file(bit_sequence_foldername, bit_sequence_filename) #loads the binary bit sequence from the file
    RSSI_index_values = get_index_values(binary_bit_sequence) #gets the index values of the RSSI values to discard

    #status report, just to check if everything is ok (for testing purposes)
    print ("The bit sequence is: ",  binary_bit_sequence)
    print ("The indexes of RSSI values to discard are: ", RSSI_index_values)

    # saves the results to a file
    write_indexes_to_file(RSSI_index_values, discard_foldername, discard_filename)

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()