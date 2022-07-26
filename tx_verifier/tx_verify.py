import verifier as v, argparse

parser = argparse.ArgumentParser(
    description = 'Bitcoin Pay-to-PubkeyHash (P2PKH) transactions verifier for Cryptography Course at UniMi'
)

parser.add_argument('-t', '--txid', help = 'The ID of the transaction to verify', type = str, metavar = 'TXID', required = True)

args = parser.parse_args()

if args.txid:
    txv = v.Verifier(args.txid)
    txv.verify_transaction()