#!python
import HMAC_SHA1
import SHA1
from bottle import route, run, abort, request, template
from utils import *
import threading
import time
from timeit import default_timer as timer
import requests

hmac_key=random_bytes(16)
insecure_delay=0.05
server_retries=1

def insecure_compare(b1, b2):
    if len(b1)!=len(b2):
        return False
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            return False
        time.sleep(0.05)

    return True

@route('/test')
def test():
    file = request.query.file
    sig  = request.query.signature
    f = open(file, 'r')
    file_content=string_bytes(f.read())
    f.close()
    file_sig=HMAC_SHA1.generate(hmac_key, file_content)
    if insecure_compare(file_sig,hexstr_bytes(sig)):
        return "Great success!!"

    abort(500, "Sorry, access denied. Expected hash is " + bytes_hexstr(file_sig))

def server_main():
    print('Starting server thread')
    run(host='localhost', port=9000, debug=True)

def test_connection(file, signature):
    # Set payload
    payload = {'file': file, 'signature': bytes_hexstr(signature)}
    time_elapsed = 0
    for i in range(server_retries):
        # Measure request
        start = timer()
        r = requests.get('http://localhost:9000/test', params=payload)
        end = timer()
        time_elapsed += end - start
    # Return status code and time
    return r.status_code, time_elapsed, r.text

def main(delay=0.05, retries=1):
    # Set globals
    global insecure_delay
    global server_retries
    insecure_delay = delay
    server_retries = retries
    # Starting server
    server = threading.Thread(target=server_main)
    server.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    server.start()
    # File to attack
    attack_file = 'README.md';
    # Generate one signature and perform 1 dummy connection
    sig = bytearray(SHA1.digest(b''));
    sig = bytearray([0]*len(sig))
    test_connection(attack_file, sig)
    # Brute-force each byte in the signature
    for j in range(len(sig)):
        max_time  = 0
        max_index = 0
        for i in range(256):
            sig[j] = i
            code, time, text = test_connection(attack_file, sig)
            if (time > max_time):
                max_time = time;
                max_index = i;
        sig[j]=max_index
    # Verify signature
    code, time, text = test_connection(attack_file, sig)
    print (bytes_hexstr(text))

if __name__ == "__main__":
    main()

