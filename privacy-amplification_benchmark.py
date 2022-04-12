import hashlib
import time

#env vars declaration
#NOTE supported hash codecs https://docs.python.org/3/library/hashlib.html
hash = hashlib.sha512()
#hash_digest = ''
hash2 = hashlib.new('sha512') #uses the OpenSSL implementation
#hash2_digest = ''
#NOTE: two input vars to help comparing the relation between the size of the input and the time taken to generate the hash
#uncomment one of them according to the input size you want to test
#input = b"Hello world" #byte stream small
input = b"cd08170f120c4637880574dbe6d36cb3c5b71a93e9ec2814ca8bb58b0007410368604ab8d72a42e321a62bbafc6c7e7bdcf8a6b25f52cc62d84746796a9ddb24" #byte stream 128 bits
iterations = 1000000
benchmark_results = []

#files and paths to be used by the program
#TODO TBD

def generate_hash(hash_codec, byte_stream):
    hash_codec.update(byte_stream)
    return hash_codec.digest()

def benchmark(hash_codec1, hash_codec2, byte_stream, messages_status):
    if messages_status: print("Benchmarking...")
    time1 = 0
    time2 = 0
    results = []
    
    start_time = time.time_ns()
    hash_digest = generate_hash(hash_codec1, byte_stream)
    end_time = time.time_ns()

    start_time2 = time.time_ns()
    hash2_digest = generate_hash(hash_codec2, byte_stream)
    end_time2 = time.time_ns()

    time1 += end_time - start_time
    time2 += end_time2 - start_time2
    
    results = [hash_digest, hash2_digest, time1, time2]

    if messages_status: print("Done!")

    return results
    
def run_benchmark():
    benchmark_results = benchmark(hash, hash2, input, True)

    print("=> Benchmark results:")
    print("-> Python hashlib implementation")
    print("Hash digest: ", benchmark_results[0])
    print(f"Running time: {benchmark_results[2]} ns")
    print("-> OpenSSL implementation")
    print("Hash digest: ", benchmark_results[1])
    print(f"Running time: {benchmark_results[3]} ns")

def run_in_bulk_benchmark():
    total_run_time1 = 0
    max_run_time1 = 0
    min_run_time1 = 0
    total_run_time2 = 0
    max_run_time2 = 0
    min_run_time2 = 0

    i = iterations
    while i >= 0:
        benchmark_results = benchmark(hash, hash2, input, False)
        total_run_time1 += benchmark_results[2]
        total_run_time2 += benchmark_results[3]
        if benchmark_results[2] > max_run_time1: max_run_time1 = benchmark_results[2]
        if benchmark_results[3] > max_run_time2: max_run_time2 = benchmark_results[3]
        if i == iterations:
            min_run_time1 = benchmark_results[2]
            min_run_time2 = benchmark_results[3]
        else:
            if benchmark_results[2] < min_run_time1: min_run_time1 = benchmark_results[2]
            if benchmark_results[3] < min_run_time2: min_run_time2 = benchmark_results[3]
        i -= 1

    print(f"=> Benchmark results for {iterations} iterations:")
    print("-> Python hashlib implementation")
    #print("Hash digest: ", benchmark_results[0])
    print(f"Running time (max): {max_run_time1} ns")
    print(f"Running time (avg): {total_run_time1 / iterations} ns")
    print(f"Running time (min): {min_run_time1} ns")
    print("-> OpenSSL implementation")
    #print("Hash digest: ", benchmark_results[1])
    print(f"Running time (max): {max_run_time2} ns")
    print(f"Running time (avg): {total_run_time2 / iterations} ns")
    print(f"Running time (min): {min_run_time2} ns")

def main():
    #execution starts here
    print("Please, uncomment the line you want to run.\nExiting...")
    #NOTE: uncomment the option you want to test below
    #run_benchmark()
    #run_in_bulk_benchmark()

# checks if the file is being run directly to avoid running it mistakenly
if __name__ == "__main__":
    main()