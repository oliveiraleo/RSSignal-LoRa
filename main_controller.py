import sys #required for the args to work
import os #provides the interactions with bash
import numpy as np
import traceback #required to get the stack trace
# imports the other framework scripts
from RSSI_to_binary import main as main_quantization
from discard_RSSI_values_step1 import main as main_index_exchange_1
from discard_RSSI_values_step3 import main as main_index_exchange_3
from key_reconciliation_reed_solomon_step1 import main as main_key_reconciliation_1
from key_reconciliation_reed_solomon_step3 import main as main_key_reconciliation_3
from privacy_amplification_step1 import main as main_privacy_amplification_1
from privacy_amplification_benchmark import main as main_privacy_amplification_benchmark
sys.path.insert(1, "./modules/RSSignal-LoRa_randomness_testsuite") #adds the module test suite folder to the path
from CustomKeyEval import main as main_randomness_testsuite

# Definitions of the functions
# returns a float type range
def get_float_range(min, max):
    range_list = list(np.arange(min, max, 0.1))
    for i in range(len(range_list)):
        range_list[i] = round(range_list[i], 1)
    return range_list

# prints the script help messages
def help(file_name):
    print (f"\nUsage:\n python3 {file_name} option [arguments]")
    print("\nOptions:\n \
-> Main functionality:\n \
- s1: Packet exchange, RSSI data collection [RSSignal 1st step\n \
- s2: Preprocess the input [RSSignal 2nd step]\n \
- s3: Quantization [RSSignal 3rd step]\n \
- s4: Index exchange (calculates the indexes to be discarded) [RSSignal 4th step]\n \
- s5: Index exchange (erases the indexes discarded) [RSSignal 4th step]\n \
- s6: Key reconciliation (encodes the data and generates the ecc bits) [RSSignal 5th step]\n \
- s7: Key reconciliation (reconciliates the data and ecc bits) [RSSignal 5th step]\n \
- s8: Privacy amplification [RSSignal 6th step]\n \
-> Extra functionality:\n \
- auto-mode: Executes the steps 3 - 8 automatically\n \
- prepare-key-eval: Executes the preprocess script to prepare data for the key evaluation\n \
- key-eval: Executes the key evaluation for a given file\n \
- auto-key-eval: Executes the key evaluation for a given range of data automatically\n \
- hash-benchmark: Executes the hash benchmark\n \
\nArguments:\n \
Vary according to the choosen option\n \
        ")
    print(f"Examples:\n python3 {file_name} s1\n \
python3 {file_name} s2 \"dataset-files/file.csv -t -c 1 -s ','\"\n \
python3 {file_name} auto-mode file-ED 0.0 1.0 1 4\
        ")
    
# script's main menu functionality (e.g. workflow control)
def script_chooser(arguments):
    if(arguments[1] == "-h" or arguments[1] == "--help" or arguments[1] == "help"):
        help(arguments[0])
    # Main functionality #
    elif (arguments[1] == "s1"): #step 1 - Probing, collects RSSI values
        print("Probing: TODO\nSkipping...")
    elif (arguments[1] == "s2"): #step 2 - Preprocessing, filters RSSI values (removes everything else from the file)
            try:
                os.system("./preprocess_input.sh " + arguments[2]) #TODO change the options to be more flexible
            except IndexError:
                print ("E: Not enough arguments were given!\nUsage:\npython3 " + arguments[0] + " " + arguments[1] + " [script args]")
                print("NOTE: script args are those from the examples below")
                os.system("./preprocess_input.sh") #displays the help 

    elif (arguments[1] == "s3"): #step 3 - Quantization, RSSI to binary
        if(len(arguments) == 5):
            try:
                main_quantization(arguments[2], float(arguments[3]), int(arguments[4]))
            except IndexError:
                print ("E: Not enough arguments were given!\nUsage:\npython3 " + arguments[0] + " " + arguments[1] + " [filename] [alpha] [m]")
        
    elif (arguments[1] == "s4"): #step 4 - Index exchange, discard RSSI values step 1 (calculates the indexes to be discarded)
        main_index_exchange_1(arguments[2])

    elif (arguments[1] == "s5"): #step 5 - Index exchange, discard RSSI values step 3 (erases the indexes discarded)
        main_index_exchange_3(arguments[2], arguments[3])

    elif (arguments[1] == "s6"): #step 6 - Key reconciliation, RS step 1 (encodes the data and generates the ecc bits)
        main_key_reconciliation_1(arguments[2])

    elif (arguments[1] == "s7"): #step 7 - Key reconciliation, RS step 3 (reconciliates the data and ecc bits)
        main_key_reconciliation_3(arguments[2], arguments[3])

    elif (arguments[1] == "s8"): #step 8 - Privacy amplification
        main_privacy_amplification_1(arguments[2])
    
    # Extra functionality #
    elif (arguments[1] == "auto-mode"): #Executes steps 3 to 8 automatically
        if(len(arguments) == 8):
            range1 = get_float_range(float(arguments[4]), float(arguments[5]) + 0.1) #adds 0.1 to the max value because the range is exclusive (ie. [min, max) )
            range2 = range(int(arguments[6]),int(arguments[7]) + 1, 1) #adds 1 to the max value because the range is exclusive (ie. [min, max) )
            # try:
            for i in range1:
                for j in range2:
                    #executes the step 2
                    main_quantization(arguments[2], float(i), int(j))
                    main_quantization(arguments[3], float(i), int(j))
            for i in range1:
                for j in range2:
                    #updates the names of the files each iteration
                    updated_file_name_alice = arguments[2] + "_alpha-" + str(float(i)) + "_m-" + str(int(j))
                    updated_file_name_bob = arguments[3] + "_alpha-" + str(float(i)) + "_m-" + str(int(j))
                    #executes the step 3
                    main_index_exchange_1(updated_file_name_alice)
                    main_index_exchange_1(updated_file_name_bob)
                    #executes the step 4
                    main_index_exchange_3(updated_file_name_alice, updated_file_name_bob)
                    main_index_exchange_3(updated_file_name_bob, updated_file_name_alice)
                    #executes the step 5
                    main_key_reconciliation_1(updated_file_name_alice)
                    main_key_reconciliation_1(updated_file_name_bob)
                    #executes the step 6
                    main_key_reconciliation_3(updated_file_name_bob, updated_file_name_alice)
                    #executes the step 7
                    main_privacy_amplification_1(updated_file_name_alice)
                    main_privacy_amplification_1(updated_file_name_bob)
                    #TODO: add an option to compare the hashes
                    #TODO: add an option to automatically process and test the keys
        else:
            print ("E: Not enough arguments were given!\nUsage:\npython3 " + arguments[0] + " " + arguments[1] + " [dataset-filename-alice] [dataset-filename-bob] [alpha-min] [alpha-max] [m-min] [m-max]")

    elif (arguments[1] == "prepare-key-eval"): #Extra - Key Evaluation preprocessing
        if(len(arguments) == 7):
            filename = arguments[2]
            params = arguments[3] + " " + arguments[4] + " " + arguments[5] + " " + arguments[6]
            command = "./results/key-after-reconciliation/gen_txt_for_evaluation.sh " + " " + filename + " " + params
            os.system(command)
            print("I: Files successfully processed")
        else:
            print ("E: Not enough arguments were given!\nUsage:\npython3 " + arguments[0] + " " + arguments[1] + " [filename-bob] [alpha-min] [alpha-max] [m-min] [m-max]")

    elif (arguments[1] == "key-eval"): #Extra - Key Evaluation
        try:
            main_randomness_testsuite(arguments[2])
        except FileNotFoundError:
            traceback.print_exc() # prints the error stack trace
            print("E: The input file wasn't found\nTry to run the \"gen_txt_for_evaluation.sh\" script located inside the \"key-after-reconciliation\" folder")
    
    elif (arguments[1] == "auto-key-eval"): #Extra - Key Evaluation
        if(len(arguments) == 7):
            range1 = get_float_range(float(arguments[3]), float(arguments[4]) + 0.1) #adds 0.1 to the max value because the range is exclusive (ie. [min, max) )
            range2 = range(int(arguments[5]),int(arguments[6]) + 1, 1) #adds 1 to the max value because the range is exclusive (ie. [min, max) )
            filename = arguments[2]
            # with open("./results/key-evaluation/" + filename + ".txt", "a+") as f: # TODO save the results to a file
            for i in range1:
                for j in range2:
                    name = "keys_" + str(arguments[2]) + "_alpha-" + str(float(i)) + "_m-" + str(int(j))
                    main_randomness_testsuite(name)
                        # content = main_randomness_testsuite(name)
                        # f.writelines(content)
            print("I: For saving the results in a file, try the command below:\npython ")
            for i in arguments:
                print(i + " ", end="")
            print("> key-eval-output.txt")
        else:
            print ("E: Not enough arguments were given!\nUsage:\npython3 " + arguments[0] + " " + arguments[1] + " [filename-bob] [alpha-min] [alpha-max] [m-min] [m-max]")
    
    elif (arguments[1] == "hash-benchmark" or arguments[1] == "benchmark"): #Extra - Hash Benchmark
        main_privacy_amplification_benchmark()
    
    else:
        print ("E: An invalid option was chosen!\nExiting...")
        sys.exit()

def main():
    args = sys.argv #update the dynamic variables
    #execution starts here
    #print (args, len(args)) #DEBUG

    #checks if the arguments are valid
    if (len(args) > 1): #TODO check if the arguments are valid
        script_chooser(args)
    else:
        print ("E: No arguments were given!")
        help(args[0]) #prints the help
        sys.exit()

if __name__ == "__main__":
    main()