import hashlib

#env vars declaration
hash_codec = hashlib.new('sha512') #uses the OpenSSL implementation
hash_digest = ''
hash_hex_digest = ''
#input_small = b"Hello world" #small byte stream
#input_64 = b"fc296a303b33c5b9ea8871ede4be3bfd6dc5ca136b43f55e97d9833bc35748b7" #byte stream 64 bytes
#input_128 = b"98fcf454833a1bd74c10c7c1f846bf162932df34efa9055a4e109e30fa93fac1c438b720e6a80cd4953d5d828971585a523020136ad529bdadb4de2477af21aa" #byte stream 128 bytes
#input_256 = b"fc296a303b33c5b9ea8871ede4be3bfd6dc5ca136b43f55e97d9833bc35748b798fcf454833a1bd74c10c7c1f846bf162932df34efa9055a4e109e30fa93fac1c438b720e6a80cd4953d5d828971585a523020136ad529bdadb4de2477af21aafc296a303b33c5b9ea8871ede4be3bfd6dc5ca136b43f55e97d9833bc35748b7" #byte stream 256 bytes
#input = input_256 #change that to select another input #TODO adapt to use ARGV

#files and paths to be used by the program
#TODO read the input from ARGV
filename = "DaCruz2021-preliminar1-cut-tab-1" #filename to be used by the program
#file_format = ".csv"
results_foldername = "results"
results_file_format = ".bin" #file format for the results file
keys_foldername = results_foldername + "/" + "keys-after-reconciliation" #folder to get the input key
keys_filename = "keys_" + filename + results_file_format #filename for the file with the key
digest_file_format = ".txt" #file format for the results file #TODO change the format to something appropriate
digest_foldername = results_foldername + "/" + "keys-digest" #folder to save the digest
digest_filename = "digest_" + filename + digest_file_format #filename for the file with the digest

def read_input_from_binary_file(foldername, filename):
    data_file_path = foldername + "/" + filename
    #binary_key = []
    content = bytearray(b'')
    print ("Reading the file located at: ", data_file_path)
    #checks if the file exists
    try:
        with open(data_file_path, "rb") as file: #open file to read
            content = bytearray(file.read())
            file.close() #close file
        print ("The reading process is done!")
    #if not, prints a message and closes the program
    except FileNotFoundError:
        print (f"The file {filename} was not found!\nPlease, check the name, make sure it exists and try again.")
        exit(code=2) #TODO change that to something that makes the entire program stop (as this file can be used by other programs in the future)
    return content

def write_hex_digest_to_file(digest, foldername, filename):
    results_path = foldername + "/" + filename
    print ("Writing the digest to the file located at: ", results_path)
    with open(results_path, "w") as file: #open file to write
        file.write(digest) #writing the digest to the file
        file.close() #close file
    print ("The writing process is done!")

def main():
    input = read_input_from_binary_file(keys_foldername, keys_filename)
    hash_codec.update(input) #NOTE: input must be of byte type
    hash_digest = hash_codec.digest()
    hash_hex_digest = hash_codec.hexdigest()
    #hash_size = hash_codec.digest_size

    print("The input was: ", input)
    print("Input's length: ", len(input), " bytes")
    #print("Digest size: ", hash_size, " bytes (", hash_size * 8, " bits )") #if using SHA3-512 should be always 512 bits
    print("The hash digest is: ", hash_digest)
    print("The hash hex digest is: ", hash_hex_digest)

    write_hex_digest_to_file(hash_hex_digest, digest_foldername, digest_filename)

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()