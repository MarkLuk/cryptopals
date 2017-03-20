#!python
import HMAC_SHA1
import SHA1
import gevent.monkey; gevent.monkey.patch_all()
from bottle import route, run, abort, request, template
from utils import *
import threading
import time
#from timeit import default_timer as timer
import time
import requests
from multiprocessing import Process, Value

hmac_key=random_bytes(16)

##########################################################################################
# Start of server code
##########################################################################################

def insecure_compare(b1, b2):
    global insecure_delay
    if len(b1)!=len(b2):
        return False
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            return False
        time.sleep(insecure_delay)

    return True

@route('/test')
def test():
    file = request.query.file
    sig  = request.query.signature
    f = open(file, 'r')
    file_content=string_bytes(f.read())
    f.close()
    hmac_digest=HMAC_SHA1.generate(hmac_key, file_content)
    if insecure_compare(hmac_digest,hexstr_bytes(sig)):
        return "Great success!!"
    print(bytes_hexstr(hmac_digest))
    abort(500, "Sorry, access denied. Expected hash is " + bytes_hexstr(hmac_digest))

def server_main_thread(delay):
    global insecure_delay
    insecure_delay = delay
    print('Starting server thread')
    run(host='localhost', port=9000, debug=False, server='gevent')

def server_start(delay):
    server = Process(target=server_main_thread, args=[delay])
    server.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    server.start()

##########################################################################################
# End of server code
##########################################################################################

##########################################################################################
# Start of client code
##########################################################################################
global_lock = threading.Lock()

def test_connection(file, signature, server_retries):
    # Set payload
    payload = {'file': file, 'signature': bytes_hexstr(bytes(signature))}
    time_elapsed = []
    for i in range(server_retries):
        time.sleep(0.05 + random_num(0,100)/100)
        # Measure request
        start = time.clock()
        r = requests.get('http://localhost:9000/test', params=payload)
        end = time.clock()
        time_elapsed += [end - start]
    time_min = sorted(time_elapsed)[0]
    # Return status code and time
    return r.status_code, time_min, r.text

def test_connection_thread(file, sig, byte_num, guess, dict, server_retries):
    global_lock.acquire()
    local_sig = list(sig)
    global_lock.release()
    local_sig[byte_num] = guess
    code, time, text = test_connection(file, local_sig, server_retries)
    global_lock.acquire()
    dict[guess]=time
    global_lock.release()

def test_connection_multithreaded(file, sig, byte_num, num_of_threads, server_retries):
    dict    = {}
    guess = 0
    for k in range(256//num_of_threads):
        threads = []
        # Dispatch all threads to check all permutations of single byte signature
        for i in range(num_of_threads):
            threads.append(threading.Thread(target=test_connection_thread, args=(file, sig, byte_num, guess, dict, server_retries)))
            threads[-1].daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            threads[-1].start()
            guess += 1

        # Join all threads
        for i in range(num_of_threads):
            threads[i].join()

    sorted_guesses = sorted(dict, key=dict.__getitem__,reverse=True);
    sig[byte_num]=sorted_guesses[0];

##########################################################################################
# End of client code
##########################################################################################

def main(insecure_delay=0.05, server_retries=10, num_of_threads=64):
    # Starting server
    server_start(insecure_delay)
    # File to attack
    attack_file = 'README.md';
    # Generate one signature and perform 1 dummy connection
    sig = bytearray(SHA1.digest(b''));
    sig = bytearray([0]*len(sig))
    # Brute-force each byte in the signature
    for j in range(len(sig)):
        test_connection_multithreaded(attack_file, sig, j, num_of_threads, server_retries)

    # Verify signature
    code, time, text = test_connection(attack_file, sig, 1)
    print (text)

if __name__ == "__main__":
    main()

