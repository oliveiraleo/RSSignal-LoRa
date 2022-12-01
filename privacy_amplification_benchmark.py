import hashlib
import time
import statistics

#env vars declaration
#NOTE supported hash codecs https://docs.python.org/3/library/hashlib.html
hash = hashlib.sha512()
#hash_digest = ''
hash2 = hashlib.new('sha512') #uses the OpenSSL implementation
#hash2_digest = ''
hash3 = hashlib.sha256()
#hash3_digest = ''
hash4 = hashlib.new('sha256') #uses the OpenSSL implementation
#hash4_digest = ''
hash5 = hashlib.sha224()
#hash5_digest = ''
hash6 = hashlib.new('sha224') #uses the OpenSSL implementation
#hash6_digest = ''
hash7 = hashlib.sha1()
#hash7_digest = ''
hash8 = hashlib.new('sha1') #uses the OpenSSL implementation
#hash8_digest = ''

#NOTE: below there are two input vars to help comparing the relation
#      between the size of the input and the time taken to generate the hash
#      change the var called 'input' according to the input size you want to test
input_small = b"Hello world" #byte stream small
input_long = b"cd08170f120c4637880574dbe6d36cb3c5b71a93e9ec2814ca8bb58b0007410368604ab8d72a42e321a62bbafc6c7e7bdcf8a6b25f52cc62d84746796a9ddb24" #byte stream 128 bits
input = input_long

iterations = 1000000 #number of iterations to run the benchmark
benchmark_results = []

#files and paths to be used by the program
#TODO read the input from ARGV
#TODO save the results in a file
#TODO add comments to the code
#NOTE Another option to get hash codecs is pycryptodome (https://www.pycryptodome.org/en/latest/src/hash/hash.html or https://github.com/Legrandin/pycryptodome)

def generate_hash(hash_codec, byte_stream):
    hash_codec.update(byte_stream)
    return hash_codec.digest()

def benchmark(hash_codec1, hash_codec2, hash_codec3, hash_codec4,
              hash_codec5, hash_codec6, hash_codec7, hash_codec8,
              byte_stream, messages_status):
    if messages_status: print("Benchmarking...")
    #creates some local vars to store the results
    time1 = 0
    time2 = 0
    time3 = 0
    time4 = 0
    time5 = 0
    time6 = 0
    time7 = 0
    time8 = 0
    results = []
    
    start_time = time.time_ns()
    hash_digest = generate_hash(hash_codec1, byte_stream)
    end_time = time.time_ns()

    start_time2 = time.time_ns()
    hash2_digest = generate_hash(hash_codec2, byte_stream)
    end_time2 = time.time_ns()

    start_time3 = time.time_ns()
    hash3_digest = generate_hash(hash_codec3, byte_stream)
    end_time3 = time.time_ns()

    start_time4 = time.time_ns()
    hash4_digest = generate_hash(hash_codec4, byte_stream)
    end_time4 = time.time_ns()

    start_time5 = time.time_ns()
    hash5_digest = generate_hash(hash_codec5, byte_stream)
    end_time5 = time.time_ns()

    start_time6 = time.time_ns()
    hash6_digest = generate_hash(hash_codec6, byte_stream)
    end_time6 = time.time_ns()

    start_time7 = time.time_ns()
    hash7_digest = generate_hash(hash_codec7, byte_stream)
    end_time7 = time.time_ns()

    start_time8 = time.time_ns()
    hash8_digest = generate_hash(hash_codec8, byte_stream)
    end_time8 = time.time_ns()


    time1 += end_time - start_time
    time2 += end_time2 - start_time2
    time3 += end_time3 - start_time3
    time4 += end_time4 - start_time4
    time5 += end_time5 - start_time5
    time6 += end_time6 - start_time6
    time7 += end_time7 - start_time7
    time8 += end_time8 - start_time8
    
    results = [hash_digest, hash2_digest, hash3_digest, hash4_digest,
               hash5_digest, hash6_digest, hash7_digest, hash8_digest,
               time1, time2, time3, time4, time5, time6, time7, time8]

    if messages_status: print("Done!")

    return results
    
def run_benchmark():
    benchmark_results = benchmark(hash, hash2, hash3, hash4, hash5, hash6, hash7, hash8, input, True)

    print("=> Benchmark results:")                     #DEBUG
    print("Input size: " + str(len(input)) + " bits")  #DEBUG

    print("-> Python SHA-512 hashlib implementation")  #DEBUG
    print("Hash digest: ", benchmark_results[0])       #DEBUG
    print(f"Running time: {benchmark_results[8]} ns")  #DEBUG

    print("-> OpenSSL SHA-512 implementation")         #DEBUG
    print("Hash digest: ", benchmark_results[1])       #DEBUG
    print(f"Running time: {benchmark_results[9]} ns")  #DEBUG

    print("-> Python SHA-256 hashlib implementation")  #DEBUG
    print("Hash digest: ", benchmark_results[2])       #DEBUG
    print(f"Running time: {benchmark_results[10]} ns") #DEBUG

    print("-> OpenSSL SHA-256 implementation")         #DEBUG
    print("Hash digest: ", benchmark_results[3])       #DEBUG
    print(f"Running time: {benchmark_results[11]} ns") #DEBUG

    print("-> Python SHA-224 hashlib implementation")   #DEBUG
    print("Hash digest: ", benchmark_results[4])        #DEBUG
    print(f"Running time: {benchmark_results[12]} ns")  #DEBUG

    print("-> OpenSSL SHA-224 implementation")          #DEBUG
    print("Hash digest: ", benchmark_results[5])        #DEBUG
    print(f"Running time: {benchmark_results[13]} ns")  #DEBUG

    print("WARNING: Please note that SHA-1 is not cryptographically secure anymore, so it should not be used!")
    print("-> Python SHA-1 hashlib implementation")     #DEBUG
    print("Hash digest: ", benchmark_results[6])        #DEBUG
    print(f"Running time: {benchmark_results[14]} ns")  #DEBUG

    print("WARNING: Please note that SHA-1 is not cryptographically secure anymore, so it should not be used!")
    print("-> OpenSSL SHA-1 implementation")            #DEBUG
    print("Hash digest: ", benchmark_results[7])        #DEBUG
    print(f"Running time: {benchmark_results[15]} ns")  #DEBUG


def run_in_bulk_benchmark(is_debugging_results):
    total_run_time1 = 0
    max_run_time1   = 0
    min_run_time1   = 0
    total_run_time2 = 0
    max_run_time2   = 0
    min_run_time2   = 0
    total_run_time3 = 0
    max_run_time3   = 0
    min_run_time3   = 0
    total_run_time4 = 0
    max_run_time4   = 0
    min_run_time4   = 0
    total_run_time5 = 0
    max_run_time5   = 0
    min_run_time5   = 0
    total_run_time6 = 0
    max_run_time6   = 0
    min_run_time6   = 0
    total_run_time7 = 0
    max_run_time7   = 0
    min_run_time7   = 0
    total_run_time8 = 0
    max_run_time8   = 0
    min_run_time8   = 0

    arr_results1 = []
    arr_results2 = []
    arr_results3 = []
    arr_results4 = []
    arr_results5 = []
    arr_results6 = []
    arr_results7 = []
    arr_results8 = []

    quartiles_results1 = []
    quartiles_results2 = []
    quartiles_results3 = []
    quartiles_results4 = []
    quartiles_results5 = []
    quartiles_results6 = []
    quartiles_results7 = []
    quartiles_results8 = []

    print("=> Benchmarking in bulk mode <=\nPlease, wait...")

    i = iterations
    while i >= 0:
        progress = (iterations - i) / iterations * 100
        benchmark_results = benchmark(hash, hash2, hash3, hash4, hash5, hash6, hash7, hash8, input, False)
        total_run_time1 += benchmark_results[8]
        total_run_time2 += benchmark_results[9]
        total_run_time3 += benchmark_results[10]
        total_run_time4 += benchmark_results[11]
        total_run_time5 += benchmark_results[12]
        total_run_time6 += benchmark_results[13]
        total_run_time7 += benchmark_results[14]
        total_run_time8 += benchmark_results[15]
        
        #store the results in arrays
        arr_results1.append(benchmark_results[8])
        arr_results2.append(benchmark_results[9])
        arr_results3.append(benchmark_results[10])
        arr_results4.append(benchmark_results[11])
        arr_results5.append(benchmark_results[12])
        arr_results6.append(benchmark_results[13])
        arr_results7.append(benchmark_results[14])
        arr_results8.append(benchmark_results[15])
        
        if benchmark_results[8] > max_run_time1: max_run_time1 = benchmark_results[8]
        if benchmark_results[9] > max_run_time2: max_run_time2 = benchmark_results[9]
        if benchmark_results[10] > max_run_time3: max_run_time3 = benchmark_results[10]
        if benchmark_results[11] > max_run_time4: max_run_time4 = benchmark_results[11]
        if benchmark_results[12] > max_run_time5: max_run_time5 = benchmark_results[12]
        if benchmark_results[13] > max_run_time6: max_run_time6 = benchmark_results[13]
        if benchmark_results[14] > max_run_time7: max_run_time7 = benchmark_results[14]
        if benchmark_results[15] > max_run_time8: max_run_time8 = benchmark_results[15]

        if i == iterations:
            min_run_time1 = benchmark_results[8]
            min_run_time2 = benchmark_results[9]
            min_run_time3 = benchmark_results[10]
            min_run_time4 = benchmark_results[11]
            min_run_time5 = benchmark_results[12]
            min_run_time6 = benchmark_results[13]
            min_run_time7 = benchmark_results[14]
            min_run_time8 = benchmark_results[15]
        else:
            if benchmark_results[8] < min_run_time1: min_run_time1 = benchmark_results[8]
            if benchmark_results[9] < min_run_time2: min_run_time2 = benchmark_results[9]
            if benchmark_results[10] < min_run_time3: min_run_time3 = benchmark_results[10]
            if benchmark_results[11] < min_run_time4: min_run_time4 = benchmark_results[11]
            if benchmark_results[12] < min_run_time5: min_run_time5 = benchmark_results[12]
            if benchmark_results[13] < min_run_time6: min_run_time6 = benchmark_results[13]
            if benchmark_results[14] < min_run_time7: min_run_time7 = benchmark_results[14]
            if benchmark_results[15] < min_run_time8: min_run_time8 = benchmark_results[15]
        
        if progress % 5 == 0:
            print(f"Progress: {progress}%")

        i -= 1
        
    quartiles_results1 = statistics.quantiles(arr_results1)
    quartiles_results2 = statistics.quantiles(arr_results2)
    quartiles_results3 = statistics.quantiles(arr_results3)
    quartiles_results4 = statistics.quantiles(arr_results4)
    quartiles_results5 = statistics.quantiles(arr_results5)
    quartiles_results6 = statistics.quantiles(arr_results6)
    quartiles_results7 = statistics.quantiles(arr_results7)
    quartiles_results8 = statistics.quantiles(arr_results8)

    # prints the arrays containing results, just for testing purposes
    if is_debugging_results:
        print("=> Printing the entire data used for this benchmark:")
        print("Test 1:", arr_results1)
        print("Test 2:", arr_results2)
        print("Test 3:", arr_results3)
        print("Test 4:", arr_results4)
        print("Test 5:", arr_results5)
        print("Test 6:", arr_results6)
        print("Test 7:", arr_results7)
        print("Test 8:", arr_results8)
        print("") #new line

    print(f"=> Benchmark results for {iterations} iterations:")                 #DEBUG
    print("Input size: " + str(len(input)) + " bits")                           #DEBUG
    print("-> Python SHA-512 hashlib implementation")                           #DEBUG
    #print("Hash digest: ", benchmark_results[0])                               #DEBUG
    print(f"Running time (max): {max_run_time1} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time1 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time1} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results1} ns") #DEBUG

    print("-> OpenSSL SHA-512 implementation")                                  #DEBUG
    #print("Hash digest: ", benchmark_results[1])                               #DEBUG
    print(f"Running time (max): {max_run_time2} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time2 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time2} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results2} ns") #DEBUG

    print("-> Python SHA-256 hashlib implementation")                           #DEBUG
    #print("Hash digest: ", benchmark_results[2])                               #DEBUG
    print(f"Running time (max): {max_run_time3} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time3 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time3} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results3} ns") #DEBUG

    print("-> OpenSSL SHA-256 implementation")                                  #DEBUG
    #print("Hash digest: ", benchmark_results[3])                               #DEBUG
    print(f"Running time (max): {max_run_time4} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time4 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time4} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results4} ns") #DEBUG

    print("-> Python SHA-224 hashlib implementation")                           #DEBUG
    #print("Hash digest: ", benchmark_results[4])                               #DEBUG
    print(f"Running time (max): {max_run_time5} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time5 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time5} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results5} ns") #DEBUG

    print("-> OpenSSL SHA-224 implementation")                                  #DEBUG
    #print("Hash digest: ", benchmark_results[5])                               #DEBUG
    print(f"Running time (max): {max_run_time6} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time6 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time6} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results6} ns") #DEBUG

    print("WARNING: Please note that SHA-1 is not cryptographically secure anymore, so it should not be used!")
    print("-> Python SHA-1 hashlib implementation")                             #DEBUG
    #print("Hash digest: ", benchmark_results[6])                               #DEBUG
    print(f"Running time (max): {max_run_time7} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time7 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time7} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results7} ns") #DEBUG

    print("WARNING: Please note that SHA-1 is not cryptographically secure anymore, so it should not be used!")
    print("-> OpenSSL SHA-1 implementation")                                    #DEBUG
    #print("Hash digest: ", benchmark_results[7])                               #DEBUG
    print(f"Running time (max): {max_run_time8} ns")                            #DEBUG
    print(f"Running time (avg): {total_run_time8 / iterations} ns")             #DEBUG
    print(f"Running time (min): {min_run_time8} ns")                            #DEBUG
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results8} ns") #DEBUG

def main():
    #execution starts here
    print("Please, uncomment the line you want to run.\nExiting...")
    #NOTE: uncomment the option you want to test below
    #run_benchmark()
    #run_in_bulk_benchmark(False) #NOTE: change to True to print the data used for the benchmark

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()