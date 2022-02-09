#import math #provides the math functions
import csv #provides the CSV related functions

#env vars declaration
RSSI_values = []
RSSI_index_values = []
binary_bit_sequence = ""
#files and paths to be used by the program
bit_sequence_foldername = "results" #folder to store the results
bit_sequence_filename = "bit-sequence_Goldoni_2018-indoor_LOS_raw_rssi-cut.csv"
data_file_foldername = "dataset-files" #folder where the data files are stored
data_file_filename = "Goldoni_2018-indoor_LOS_raw_rssi-cut.csv" #filename to be used by the program

#definitions of the functions
def read_RSSI_input_file(foldername, filename):
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
    return vet_RSSI_values

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

#execution starts here
RSSI_values = read_RSSI_input_file(data_file_foldername, data_file_filename) #loads the RSSI values from the file
binary_bit_sequence = read_binary_input_file(bit_sequence_foldername, bit_sequence_filename) #loads the binary bit sequence from the file
RSSI_index_values = get_index_values(binary_bit_sequence) #gets the index values of the RSSI values to discard

#status report, just to check if everything is ok (for testing purposes)
print ("The RSSI values are: ", RSSI_values)
print ("The bit sequence is: ",  binary_bit_sequence)
print ("The indexes of RSSI values to discard are: ", RSSI_index_values) #TODO function to discard the indexes obtained here