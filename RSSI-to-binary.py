import math #provides the math functions
import csv #provides the CSV related functions

#env vars declaration
vet_RSSI_input = [] #vector of the RSSI values to be processed (values will be read from the input file)
vet_binary_output = [] #vector of the binary bit sequence output (values to be written to the results file)
RSSI_average = 0
RSSI_standard_deviation = 0
RSSI_quant_threshold_upper = 0 #upper quantization threshold
RSSI_quant_threshold_lower = 0 #lower quantization threshold
#files and paths to be used by the program
results_foldername = "results" #folder to store the results
results_filename = "bit-sequence_Goldoni_2022-indoor_LOS_raw_rssi-cut.csv"
data_file_foldername = "dataset-files" #folder where the data files are stored
data_file_filename = "Goldoni_2022-indoor_LOS_raw_rssi-cut.csv" #filename to be used by the program

#function created just for testing in bulk
"""def read_file_name():
    print ("Please, enter the name of the file to be processed: ", end="") #inline print
    filename = input()
    return filename

data_file_filename = read_file_name()
results_filename = "bit-sequence_" + data_file_filename"""

def read_input_file(foldername, filename):
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
            file.close() #close file
        print ("The reading process is done!")
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print ("The file " + str(filename) + " was not found!\nPlease, check the name making sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return vet_RSSI_values

vet_RSSI_input = read_input_file(data_file_foldername, data_file_filename) #loads the RSSI values from the file
#print ("Input values: " + str(vet_RSSI_input)) #print input values, just for testing

RSSI_average = sum(vet_RSSI_input) / len(vet_RSSI_input) #calculates the average of the RSSI values

print ("Average: " + str(RSSI_average))

def calculate_standard_deviation (vet_RSSI_input, RSSI_average): #calculates the standard deviation of the RSSI values
    vet_RSSI_std_deviation = []
    for i in vet_RSSI_input: #for each value in the input vector
        vet_RSSI_std_deviation.append(math.pow(i - RSSI_average, 2)) #calculates the square of the difference between the value and the average (first step)
    return math.sqrt(sum(vet_RSSI_std_deviation) / len(vet_RSSI_std_deviation)) #returns the square root of the sum of the square of the differences divided by the number of values

RSSI_standard_deviation = calculate_standard_deviation(vet_RSSI_input, RSSI_average)

print ("Standard Deviation: " + str(RSSI_standard_deviation))

# calculate the quantization thresholds
RSSI_quant_threshold_upper = RSSI_average + RSSI_standard_deviation
RSSI_quant_threshold_lower = RSSI_average - RSSI_standard_deviation

print ("Upper quantization threshold: " + str(RSSI_quant_threshold_upper))
print ("Lower quantization threshold: " + str(RSSI_quant_threshold_lower))

# processes the RSSI values to binary
def process_RSSI_bits(vet_RSSI_input, vet_bit_sequence, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower): #TODO remove vet_bit_sequence from arguments
    for i in vet_RSSI_input: #for each value in the input vector
        if (i > RSSI_quant_threshold_upper): #if the value is greater than the upper quantization threshold
            vet_bit_sequence.append(1) #append a 1 to the output vector
        elif (i < RSSI_quant_threshold_lower): #if the value is less than the lower quantization threshold
            vet_bit_sequence.append(0) #append a 0 to the output vector
        else: #if the value is between the two thresholds
            vet_bit_sequence.append(2) #append a 2 to the output vector
    return vet_bit_sequence

vet_binary_output = process_RSSI_bits(vet_RSSI_input, vet_binary_output, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower)
#print ("Output values: " + str(vet_binary_output))

def print_bit_sequence(vet_bit_sequence):
    print ("Bit sequence: ", end="") #inline print
    for i in vet_bit_sequence:
        if (i == 0):
            print ("0", end="")
        elif (i == 1):
            print ("1", end="")
        elif (i == 2):
            print ("2", end="")
    print ("")

print_bit_sequence(vet_binary_output)

def get_raw_bit_sequence(vet_bit_sequence):
    bit_sequence = ""
    for i in vet_bit_sequence:
        if (i == 0):
            bit_sequence = bit_sequence + "0"
        elif (i == 1):
            bit_sequence = bit_sequence + "1"
        elif (i == 2):
            bit_sequence = bit_sequence + "2"
    return bit_sequence

def write_bit_sequence_to_file(vet_bit_sequence, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the result to the file located at: " + str(results_path))
    #row = str(get_raw_bit_sequence(vet_bit_sequence))
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        #csvwriter.writerow([row]) #writing the row to the file
        csvwriter.writerow(vet_bit_sequence) #writing the rows to the file
        #file.write("\n") #ends the file with a new line
        file.close() #close file
    print ("The writing process is done!")

write_bit_sequence_to_file(vet_binary_output, results_foldername, results_filename)