import network, utility, tx

class Verifier:
    __tx = None

    def __init__(self, txid):
        self.__tx = tx.Transaction(txid)

    def verify_transaction(self):
        '''
        Verifies the transaction
        Returns True if verified
        Returns False if not
        '''
        inputs = self.__tx.get_input_list()

        inputs_verified = 0
        i = 1

        for input_obj in inputs:
            # hash160 of public key from address (base58 checksum check)
            addr_hash160 = self.calc_hash160(input_obj.get_pubkey())
            prev_pubkeyhash, prev_script_with_size = self.extract_prev_script_and_pubkey(input_obj.get_prev_txid(), input_obj.get_prev_out())

            if prev_pubkeyhash != addr_hash160:
                print('Verification failed: the public key of the input is not the same as the output')


            new_raw_tx = self.build_new_tx(input_obj, inputs, prev_script_with_size)


            # now that we have the new raw transaction, we have to apply sha256 on it
            tx_sha256 = utility.sha256(new_raw_tx)

            # now we have all what is needed for signature verification
            # pubkey, signature and tx_sha256
            if utility.verify_transaction(input_obj.get_pubkey(), input_obj.get_sig(), tx_sha256):
                print(f'The input {i}/{len(inputs)} has been verified successfully')
                inputs_verified += 1
            else:
                print(f'The verification of input {i}/{len(inputs)} has failed')

            i += 1
        
        if inputs_verified == len(inputs):
            print('The transaction has been verified successfully!')
            return True
        else:
            return False


    def calc_hash160(self, pubkey):
        '''
        Calculates the hash160 of the address, given the corresponding public key
        '''
        # address derived from public key by hash160ing and encoding to base58
        address = utility.pubkeyToAddress(pubkey)

        # hash160 of public key from address (base58 checksum check)
        return utility.hash160_address(address)


    def extract_prev_script_and_pubkey(self, prev_txid, prev_out):
        '''
        Given a transaction ID, and the output index, returns the pubKeyHash and the complete script with size
        '''
        # now we have to get the output of the previous transaction corresponding to this input
        prev_tx = network.get_tx_from_txid(prev_txid)

        prev_script = prev_tx['out'][prev_out]['script']

        prev_script_size_hex = prev_script[4:6]
        prev_script_size = int(prev_script_size_hex, 16)
        prev_pubkeyhash = prev_script[6:6+prev_script_size*2]

        prev_script_with_size = int(len(prev_script)/2).to_bytes(1, 'big') + bytes.fromhex(prev_script) #####

        return prev_pubkeyhash, prev_script_with_size


    def build_new_tx(self, input_obj, inputs, prev_script_with_size):
        '''
        Given the input from which we want to build the transaction, the inputs list
        and the script with size of the previous transaction,
        it builds the new transaction needed to verify the signature
        '''
        # the new raw transaction is needed to verify the signature, it is the same as the original transaction
        # but the inputs section is replaced with the script from the previous output (with size)
        # and after the outputs there is 01000000 which stands for SIGHASH_ALL
        raw_tx = self.__tx.get_raw_tx()
        new_raw_tx = raw_tx[0:5]
        for i in inputs:
            if i == input_obj:
                new_raw_tx = new_raw_tx + raw_tx[i.get_start():i.get_script_start()] + prev_script_with_size + raw_tx[i.get_script_end():i.get_end()]
            else:
                new_raw_tx = new_raw_tx + raw_tx[i.get_start():i.get_script_start()] + bytes.fromhex('00') + raw_tx[i.get_script_end():i.get_end()]

        new_raw_tx += raw_tx[inputs[len(inputs)-1].get_script_end()+4:] + bytes.fromhex('01000000')
        
        return new_raw_tx