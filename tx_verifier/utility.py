import hashlib, ecdsa


def sha256(binstr):
    return hashlib.sha256(binstr).digest()


def hash160(hex):
    # The hashing is algorithm is a HASH160 which is a SHA256 followed by a RIPEMD160 hash
    pubkey = bytearray.fromhex(hex)

    h256 = hashlib.sha256()
    rmd160 = hashlib.new('ripemd160')

    h256.update(pubkey)
    hash1 = h256.digest()

    rmd160.update(hash1)
    return rmd160.digest()


def verify_transaction(pub_key, sig, tx_h256):
    '''
    It hashes the transaction hash and then verifies the signature
    '''
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub_key), curve=ecdsa.SECP256k1)
    return vk.verify(sig, tx_h256, hashlib.sha256)
