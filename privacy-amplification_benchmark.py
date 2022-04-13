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
#NOTE: two input vars to help comparing the relation between the size of the input and the time taken to generate the hash
#uncomment one of them according to the input size you want to test
#input = b"Hello world" #byte stream small
input = b"cd08170f120c4637880574dbe6d36cb3c5b71a93e9ec2814ca8bb58b0007410368604ab8d72a42e321a62bbafc6c7e7bdcf8a6b25f52cc62d84746796a9ddb24" #byte stream 128 bits
iterations = 100 #number of iterations to run the benchmark
benchmark_results = []

#files and paths to be used by the program
#TODO TBD

def generate_hash(hash_codec, byte_stream):
    hash_codec.update(byte_stream)
    return hash_codec.digest()

def benchmark(hash_codec1, hash_codec2, hash_codec3, hash_codec4, byte_stream, messages_status):
    if messages_status: print("Benchmarking...")
    time1 = 0
    time2 = 0
    time3 = 0
    time4 = 0
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

    time1 += end_time - start_time
    time2 += end_time2 - start_time2
    time3 += end_time3 - start_time3
    time4 += end_time4 - start_time4
    
    results = [hash_digest, hash2_digest, hash3_digest, hash4_digest, time1, time2, time3, time4]

    if messages_status: print("Done!")

    return results
    
def run_benchmark():
    benchmark_results = benchmark(hash, hash2, hash3, hash4, input, True)

    print("=> Benchmark results:")
    print("Input size: " + str(len(input)) + " bits")
    print("-> Python SHA-512 hashlib implementation")
    print("Hash digest: ", benchmark_results[0])
    print(f"Running time: {benchmark_results[4]} ns")
    print("-> OpenSSL SHA-512 implementation")
    print("Hash digest: ", benchmark_results[1])
    print(f"Running time: {benchmark_results[5]} ns")
    print("-> Python SHA-256 hashlib implementation")
    print("Hash digest: ", benchmark_results[2])
    print(f"Running time: {benchmark_results[6]} ns")
    print("-> OpenSSL SHA-256 implementation")
    print("Hash digest: ", benchmark_results[3])
    print(f"Running time: {benchmark_results[7]} ns")

def run_in_bulk_benchmark():
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

    arr_results1 = []
    arr_results2 = []
    arr_results3 = []
    arr_results4 = []
    quartiles_results1 = []
    quartiles_results2 = []
    quartiles_results3 = []
    quartiles_results4 = []

    i = iterations
    while i >= 0:
        benchmark_results = benchmark(hash, hash2, hash3, hash4, input, False)
        total_run_time1 += benchmark_results[4]
        total_run_time2 += benchmark_results[5]
        total_run_time3 += benchmark_results[6]
        total_run_time4 += benchmark_results[7]
        
        #store the results in arrays
        arr_results1.append(benchmark_results[4])
        arr_results2.append(benchmark_results[5])
        arr_results3.append(benchmark_results[6])
        arr_results4.append(benchmark_results[7])
        
        if benchmark_results[4] > max_run_time1: max_run_time1 = benchmark_results[4]
        if benchmark_results[5] > max_run_time2: max_run_time2 = benchmark_results[5]
        if benchmark_results[6] > max_run_time3: max_run_time3 = benchmark_results[6]
        if benchmark_results[7] > max_run_time4: max_run_time4 = benchmark_results[7]
        if i == iterations:
            min_run_time1 = benchmark_results[4]
            min_run_time2 = benchmark_results[5]
            min_run_time3 = benchmark_results[6]
            min_run_time4 = benchmark_results[7]
        else:
            if benchmark_results[4] < min_run_time1: min_run_time1 = benchmark_results[4]
            if benchmark_results[5] < min_run_time2: min_run_time2 = benchmark_results[5]
            if benchmark_results[6] < min_run_time3: min_run_time3 = benchmark_results[6]
            if benchmark_results[7] < min_run_time4: min_run_time4 = benchmark_results[7]
        i -= 1
        
    quartiles_results1 = statistics.quantiles(arr_results1)
    quartiles_results2 = statistics.quantiles(arr_results2)
    quartiles_results3 = statistics.quantiles(arr_results3)
    quartiles_results4 = statistics.quantiles(arr_results4)

    print(f"=> Benchmark results for {iterations} iterations:")
    print("Input size: " + str(len(input)) + " bits")
    print("-> Python SHA-512 hashlib implementation")
    #print("Hash digest: ", benchmark_results[0])
    print(f"Running time (max): {max_run_time1} ns")
    print(f"Running time (avg): {total_run_time1 / iterations} ns")
    print(f"Running time (min): {min_run_time1} ns")
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results1} ns")

    print("-> OpenSSL SHA-512 implementation")
    #print("Hash digest: ", benchmark_results[1])
    print(f"Running time (max): {max_run_time2} ns")
    print(f"Running time (avg): {total_run_time2 / iterations} ns")
    print(f"Running time (min): {min_run_time2} ns")
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results2} ns")

    print("-> Python SHA-256 hashlib implementation")
    #print("Hash digest: ", benchmark_results[2])
    print(f"Running time (max): {max_run_time3} ns")
    print(f"Running time (avg): {total_run_time3 / iterations} ns")
    print(f"Running time (min): {min_run_time3} ns")
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results3} ns")

    print("-> OpenSSL SHA-256 implementation")
    #print("Hash digest: ", benchmark_results[3])
    print(f"Running time (max): {max_run_time4} ns")
    print(f"Running time (avg): {total_run_time4 / iterations} ns")
    print(f"Running time (min): {min_run_time4} ns")
    print(f"Running time quartiles (25% / 50% / 75%): {quartiles_results4} ns")

def main():
    #execution starts here
    print("Please, uncomment the line you want to run.\nExiting...")
    #NOTE: uncomment the option you want to test below
    #run_benchmark()
    #run_in_bulk_benchmark()

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()