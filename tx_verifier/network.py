import requests

BLOCKCHAIN_API_ENDPOINT = 'https://blockchain.info/rawtx/{}'

def get_raw_tx_from_txid(txid):
    '''
    returns transaction as an hex string
    '''
    return requests.get(BLOCKCHAIN_API_ENDPOINT.format(txid), params={'format': 'hex'}).text

def get_tx_from_txid(txid):
    '''
    returns transaction in json format
    '''
    return requests.get(BLOCKCHAIN_API_ENDPOINT.format(txid)).json()
