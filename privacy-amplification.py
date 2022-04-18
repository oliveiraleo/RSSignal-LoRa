import hashlib

#env vars declaration
hash_codec = hashlib.new('sha512') #uses the OpenSSL implementation
hash_digest = ''
hash_hex_digest = ''
input = b"Hello world" #byte stream

#files and paths to be used by the program
#TODO read the input from file
#TODO read the input from ARGV
filename = "DaCruz2021-preliminar1-cut-tab-1" #filename to be used by the program
file_format = ".csv"
results_foldername = "results"
results_file_format = ".csv" #file format for the results file #TODO change the format to match the desired input file format
#bit_stream_foldername = results_foldername + "/" + "keys" #folder where the keys were stored
#bit_stream_filename = "bit-stream_" + filename + file_format
keys_foldername = results_foldername + "/" + "keys-after-reconciliation" #folder to get the input key
keys_filename = "keys_" + filename + results_file_format #filename for the file with the key
#ecc_filename = "ecc_" + filename #filename for the file with results
digest_file_format = ".txt" #file format for the results file #TODO change the format to something appropriate
digest_foldername = results_foldername + "/" + "keys-digest" #folder to save the digest
digest_filename = "digest_" + filename + digest_file_format #filename for the file with the digest

def write_hex_digest_to_file(digest, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the digest to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        #csvwriter = csv.writer(file) #creating a csv writer object 
        #csvwriter.writerow(vet_discard_indexes) #writing the rows to the file
        file.write(digest) #writing the digest to the file
        file.close() #close file
    print ("The writing process is done!")

def main():
    #execution starts here
    hash_codec.update(input) #NOTE: input must be of byte type
    hash_digest = hash_codec.digest()
    hash_hex_digest = hash_codec.hexdigest()

    print("The input was: ", input)
    print("Input's length: ", len(input), " bits")
    print("The hash digest is: ", hash_digest)
    print("The hash hex digest is: ", hash_hex_digest)

    write_hex_digest_to_file(hash_hex_digest, digest_foldername, digest_filename)

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()