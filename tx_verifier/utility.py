from string import hexdigits
import base58, hashlib, ecdsa


def sha256(binstr):
    return hashlib.sha256(binstr).digest()


def double_sha256(binstr):
    return hashlib.sha256(hashlib.sha256(binstr).digest()).digest()


def hash160(hex):
    # The hashing is algorithm is a HASH160 which is a SHA256 followed by a RIPEMD160 hash
    pubkey = bytearray.fromhex(hex)

    h256 = hashlib.sha256()
    rmd160 = hashlib.new('ripemd160')

    h256.update(pubkey)
    hash1 = h256.digest()

    rmd160.update(hash1)
    return rmd160.digest()


def convertPKHToAddress(prefix, addr):
    data = prefix + addr
    addr_checksum = double_sha256(data)[:4]
    return base58.b58encode(data + addr_checksum)


def pubkeyToAddress(pubkey_hex):
    '''
    pubkey_hex: public key in hex
    returns: address in base58
    '''
    return convertPKHToAddress(b'\x00', hash160(pubkey_hex))


def hash160_address(addr):
    return base58.b58decode_check(addr)[1:].hex()


def verify_transaction(pub_key, sig, tx_h256):
    '''
    It hashes the transaction hash and then verifies the signature
    '''
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub_key), curve=ecdsa.SECP256k1)
    return vk.verify(sig, tx_h256, hashlib.sha256)
