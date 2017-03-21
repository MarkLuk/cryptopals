#!python

from utils import *
import threading


p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
alice_id = 0
bob_id = 1
public_keys = [0, 0];
public_keys_ready = [threading.Condition(), threading.Condition()];
thread_names = ['Alice', 'Bob']

def thread_main(my_id, party_id,public_keys, public_keys_ready):
    # Generate public key
    my_a = bytes_int(random_bytes(16))
    my_public = modular_pow(g, my_a, p)

    # Publish public key
    public_keys_ready[my_id].acquire();
    public_keys[my_id] = my_public
    public_keys_ready[my_id].notify();
    public_keys_ready[my_id].release();

    # Wait for other public key
    public_keys_ready[party_id].acquire();
    while (public_keys[party_id] == 0):
        public_keys_ready[party_id].wait();
    pub_key = public_keys[party_id];
    public_keys_ready[party_id].release();

    # Generate session key
    session_key = modular_pow(pub_key, my_a, p);
    print ('Thread', thread_names[my_id], 'session key: ', hex(session_key))


def main():
    # Start Alice thread
    alice = threading.Thread(target=thread_main, args=(alice_id, bob_id, public_keys, public_keys_ready))
    alice.start()
    # Start Bob thread
    bob = threading.Thread(target=thread_main, args=(bob_id, alice_id, public_keys, public_keys_ready))
    bob.start()

    # Wait for threads to finish
    alice.join();
    bob.join();

if __name__ == "__main__":
    main()