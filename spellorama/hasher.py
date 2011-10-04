import hashlib
import os

HASH_ITERATIONS = 50

def create_hash(password, salt=None):
    """ Hashes passwords 50 times to reduce chance of someone guessing 
    using brute force. """
    
    # If no hash provided then generate a random one
    if salt == None:
        salt = os. urandom(16)

    hash = password

    # Hash it 100 times
    for i in range(HASH_ITERATIONS):
        hash = hashlib.sha256(hash + salt).digest()
    
    # Return hash, but add salt at the front so that when testing we can find
    # what salt to add.
    return (salt+hash).encode("hex")

def test_hash(password, hash):
    """ Tests a given string to see if when hashed it matches a given hash. """

    # Decode the salt at the start of the given hash.
    salt = hash[:32].decode("hex")
    
    # Test to see if the hashed version is the same as given hash.
    return create_hash(password, salt) == hash

    
