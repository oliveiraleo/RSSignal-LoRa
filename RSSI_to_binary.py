import math #provides the math functions
import csv #provides the CSV related functions

#function created just for testing in bulk
def read_input_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    vet_RSSI_values = []
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "r") as file: #open file to read
            csvreader = csv.reader(file) #creating a csv reader object
            i = 0
            for row in csvreader:
                #print (row)
                for i in range(0, len(row)):
                    vet_RSSI_values.append(float(row[i])) #float doesn't accept strings #TODO catch exception if the value is not a number
            file.close() #close file
        print ("The reading process is done!")
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return vet_RSSI_values

def calculate_RSSI_difference(vet_RSSI_input, m):
    arr_RSSI_difference = []
    for i in range(0, len(vet_RSSI_input) - m):
        #if i + m < len(vet_RSSI_input):
        arr_RSSI_difference.append(vet_RSSI_input[i] - vet_RSSI_input[i + m])
    return arr_RSSI_difference

def calculate_standard_deviation (vet_RSSI_input, RSSI_average): #calculates the standard deviation of the RSSI values
    vet_RSSI_std_deviation = []
    for i in vet_RSSI_input: #for each value in the input vector
        vet_RSSI_std_deviation.append(math.pow(i - RSSI_average, 2)) #calculates the square of the difference between the value and the average (first step)
    return math.sqrt(sum(vet_RSSI_std_deviation) / len(vet_RSSI_std_deviation)) #returns the square root of the sum of the square of the differences divided by the number of values

# processes the RSSI values and return the binary bit sequence
def process_RSSI_bits(vet_RSSI_input, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower):
    vet_bit_sequence = []
    for i in vet_RSSI_input: #for each value in the input vector
        if (i > RSSI_quant_threshold_upper): #if the value is greater than the upper quantization threshold
            vet_bit_sequence.append(1) #append a 1 to the output vector
        elif (i < RSSI_quant_threshold_lower): #if the value is less than the lower quantization threshold
            vet_bit_sequence.append(0) #append a 0 to the output vector
        else: #if the value is between the two thresholds
            vet_bit_sequence.append(2) #append a 2 to the output vector
    return vet_bit_sequence

# auxiliary function to print the bit sequence in a readable manner
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

def write_bit_sequence_to_file(vet_bit_sequence, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the result to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow(vet_bit_sequence) #writing the rows to the file
        file.close() #close file
    print ("The writing process is done!")

# defines the main function
def main(fileName, alpha = 1, m_value = 1):
    #updates dynamic variables
    RSSI_quant_threshold_alpha = alpha #thresholds offset
    filename = fileName #filename to be used by the program
    m = m_value #differentiation param (distance between measurements)

    #env vars declaration
    vet_RSSI_input = [] #vector of the RSSI values to be processed (values will be read from the input file)
    vet_binary_output = [] #vector of the binary bit sequence output (values to be written to the results file)
    RSSI_average = 0
    RSSI_standard_deviation = 0
    RSSI_quant_threshold_upper = 0 #upper quantization threshold
    RSSI_quant_threshold_lower = 0 #lower quantization threshold
    #RSSI_quant_threshold_alpha = 1 #thresholds offset
    #files and paths to be used by the program
    file_format = ".csv"
    results_foldername = "results" #folder to store the results
    bit_sequence_foldername = results_foldername + "/" + "bit-sequence" #folder to store the results
    bit_sequence_filename = "bit-sequence_" + filename + "_alpha-" + str(RSSI_quant_threshold_alpha) + "_m-" + str(m) + file_format
    data_file_foldername = "dataset-files" #folder where the data files are stored
    data_file_filename = filename + file_format #filename to be used as input by the program
    
    #execution starts here
    #print (f"Using alpha = {RSSI_quant_threshold_alpha} and m = {m}") #DEBUG
    
    vet_RSSI_input = read_input_file(data_file_foldername, data_file_filename) #loads the RSSI values from the file
    print ("Input values: ", vet_RSSI_input, len(vet_RSSI_input)) #print input values, just for testing #DEBUG

    arr_RSSI_diff = calculate_RSSI_difference(vet_RSSI_input, m) #calculates the RSSI difference
    print ("RSSI difference: ", arr_RSSI_diff, len(arr_RSSI_diff)) #print RSSI difference, just for testing #DEBUG
    print ("M value: ", m) #print M value, just for testing #DEBUG
    
    #RSSI_average = sum(vet_RSSI_input) / len(vet_RSSI_input) #calculates the average of the RSSI values
    RSSI_average = sum(arr_RSSI_diff) / len(arr_RSSI_diff) #calculates the average of the RSSI values
    print ("Average: ", RSSI_average)

    RSSI_standard_deviation = calculate_standard_deviation(arr_RSSI_diff, RSSI_average)
    print ("Standard Deviation: ", RSSI_standard_deviation)

    # calculate the quantization thresholds
    RSSI_quant_threshold_upper = RSSI_average + (RSSI_quant_threshold_alpha * RSSI_standard_deviation)
    RSSI_quant_threshold_lower = RSSI_average - (RSSI_quant_threshold_alpha * RSSI_standard_deviation)
    print ("Upper quantization threshold: ", RSSI_quant_threshold_upper)
    print ("Lower quantization threshold: ", RSSI_quant_threshold_lower)
    print ("Alpha threshold adjustment: "  , RSSI_quant_threshold_alpha)

    vet_binary_output = process_RSSI_bits(arr_RSSI_diff, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower)
    print ("Output values: ", vet_binary_output) #DEBUG
    print_bit_sequence(vet_binary_output)
    
    # saves the results to a file
    write_bit_sequence_to_file(vet_binary_output, bit_sequence_foldername, bit_sequence_filename)

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()