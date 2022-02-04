import math #provides the math functions
import csv #provides the CSV related functions

#env vars declaration
#vet test values
#source test
#vet_RSSI_input = [-69, -50, -122, -40] #input data #TODO change to file reading
#source https://github.com/emanueleg/lora-rssi/blob/master/localization-2018_data/channel_data/indoor_LOS_avg_rssi_dist.txt
vet_RSSI_input = [-42.8, -41.77, -42.59, -41.68, -41.69, -41.96, -40.9, -40.66, -39.35, -35.11]
#source https://github.com/emanueleg/lora-rssi/blob/master/localization-2018_data/channel_data/indoor_LOS_raw_rssi.ods
#vet_RSSI_input = [-85,-79,-82,-78,-80,-81,-82,-79,-81,-79,-81,-74,-76,-76,-75,-76,-74,-74,-74,-74,-74,-74,-74,-74,-76,-76,-75,-75,-76,-76,-75,-75,-75,-76,-75,-76,-76,-75,-76,-76,-74,-74,-74,-74,-74,-74,-74,-74,-75,-75,-76,-76,-76,-76,-76,-76,-74,-74,-74,-74,-74,-74,-74,-74,-74,-74,-73,-74,-74,-74,-74,-73,-76,-76,-76,-76,-76,-76,-76,-76,-74,-74,-74,-74,-74,-74,-74,-73,-76,-76,-75,-75,-75,-75,-76,-76,-75,-76,-75,-76]
#source https://github.com/emanueleg/lora-rssi/blob/master/localization-2018_data/channel_data/outdoor_LOS_avg_rssi_dist.txt
#vet_RSSI_input = [-69.6,-70.3,-72.9,-79.0,-79.1,-80.5,-86.7,-88.4,-85.7,-89.3,-89.3,-91.5]
vet_RSSI_output = []
RSSI_average = 0
RSSI_standard_deviation = 0
RSSI_quant_threshold_upper = 0 #upper quantization threshold
RSSI_quant_threshold_lower = 0 #lower quantization threshold
#files to be used by the program
results_foldername = "results" #folder to store the results
results_filename = "results_bit-sequence.csv"

print ("Input values: " + str(vet_RSSI_input)) #print input values, just for testing

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
def process_RSSI_bits(vet_RSSI_input, vet_RSSI_output, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower):
    for i in vet_RSSI_input: #for each value in the input vector
        if (i > RSSI_quant_threshold_upper): #if the value is greater than the upper quantization threshold
            vet_RSSI_output.append(1) #append a 1 to the output vector
        elif (i < RSSI_quant_threshold_lower): #if the value is less than the lower quantization threshold
            vet_RSSI_output.append(0) #append a 0 to the output vector
        else: #if the value is between the two thresholds
            vet_RSSI_output.append(2) #append a 2 to the output vector
    return vet_RSSI_output

vet_RSSI_output = process_RSSI_bits(vet_RSSI_input, vet_RSSI_output, RSSI_quant_threshold_upper, RSSI_quant_threshold_lower)
print ("Output values: " + str(vet_RSSI_output))

def print_bit_sequence(vet_RSSI_output):
    print ("Bit sequence: ", end="") #inline print
    for i in vet_RSSI_output:
        if (i == 0):
            print ("0", end="")
        elif (i == 1):
            print ("1", end="")
        elif (i == 2):
            print ("2", end="")
    print ("")

print_bit_sequence(vet_RSSI_output)

def get_raw_bit_sequence(vet_RSSI_output):
    bit_sequence = ""
    for i in vet_RSSI_output:
        if (i == 0):
            bit_sequence = bit_sequence + "0"
        elif (i == 1):
            bit_sequence = bit_sequence + "1"
        elif (i == 2):
            bit_sequence = bit_sequence + "2"
    return bit_sequence

def write_bit_sequence_to_file(vet_RSSI_output, foldername, filename):
    results_path = foldername + "/" + filename
    row = str(get_raw_bit_sequence(vet_RSSI_output))
    print ("Writing the result to the file located at: " + str(results_path))
    with open(results_path, "w") as file: #open file to write
        """for i in vet_RSSI_output:
            if (i == 0):
                file.write("0")
            elif (i == 1):
                file.write("1")
            elif (i == 2):
                file.write("2")"""
        csvwriter = csv.writer(file) #creating a csv writer object 
        csvwriter.writerow([row]) #writing the row to the file
        #file.write("\n") #ends the file with a new line
        file.close() #close file
    print ("The writing process is done!")

write_bit_sequence_to_file(vet_RSSI_output, results_foldername, results_filename)