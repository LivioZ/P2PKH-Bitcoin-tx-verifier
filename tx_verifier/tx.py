import network, input

class Transaction:
    __txid = None
    __raw_tx = None
    __version = None
    __input_count = None
    __inputs = []


    def __init__(self, txid):
        self.__txid = txid
        self.__raw_tx = bytearray.fromhex(network.get_raw_tx_from_txid(txid))
        self.__version = self.extract_version()
        self.__input_count = self.extract_input_count()
        self.__inputs = self.extract_inputs()

    def get_input_list(self):
        return self.__inputs

    def get_raw_tx(self):
        return self.__raw_tx


    def extract_version(self):
        '''
        Returns transaction version (hex)
        '''
        # version: 4 bytes
        return self.__raw_tx[0:4].hex()

    def extract_input_count(self):
        '''
        Return input count (int)
        '''
        # input count: 1 byte
        return int.from_bytes(self.__raw_tx[4:5], 'little')


    def extract_inputs(self):
        '''
        Returns a list of Input objects extracted from the raw transaction
        '''
        x = 5
        input_list = []

        for i in range(self.__input_count):
            # previous tx id: 32 bytes
            start = x
            y = x + 32
            prev_txid = self.__raw_tx[x:y]
            prev_txid.reverse()
            prev_txid = prev_txid.hex()

            #previous tx output: 4 bytes
            x = y
            y = x + 4
            prev_out_b = self.__raw_tx[x:y]
            prev_out = int.from_bytes(prev_out_b, 'little')

            script_start = y

            script_length = int.from_bytes(self.__raw_tx[y:y+1], 'little')
            script_end = script_start + script_length + 1

            x = y + 5 # skip to r length
            y = x + 1
            r_length = int.from_bytes(self.__raw_tx[x:y], 'big')
            # there is a case where r_length is 33 instead of 32 with an initial byte 00
            # so check if it's 33 and skip initial 00
            if r_length == 33:
                x = y + 1
                y = x + r_length - 1
            else:
                x = y
                y = x + r_length


            r = self.__raw_tx[x:y].hex()

            x = y + 1 # skip s value marker
            y = x + 1
            l_length = int.from_bytes(self.__raw_tx[x:y], 'big')

            x = y
            y = x + l_length
            l = self.__raw_tx[x:y].hex()

            signature = bytes.fromhex(r + l)

            x = y + 1 # skip sig hash flag
            y = x + 1
            pubkey_length = int.from_bytes(self.__raw_tx[x:y], 'big')
            x = y
            y = x + pubkey_length
            pubkey = self.__raw_tx[x:y].hex()

            x = y + 4 # reset x for next iteration

            input_object = input.Input(prev_txid, prev_out, pubkey, signature, start, x, script_start, script_end)

            input_list.append(input_object)
        
        return input_list
