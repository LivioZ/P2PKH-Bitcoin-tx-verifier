class Input:
    __prev_txid = None
    __prev_out = None
    __pubkey = None
    __sig = None
    __start = None
    __end = None
    __script_start = None # with script length
    __script_end = None

    def __init__(self, prev_txid, prev_out, pubkey, sig, start, end, script_start, script_end):
        self.__prev_txid = prev_txid
        self.__prev_out = prev_out
        self.__pubkey = pubkey
        self.__sig = sig
        self.__start = start
        self.__end = end
        self.__script_start = script_start
        self.__script_end = script_end


    def get_prev_txid(self):
        return self.__prev_txid

    def get_prev_out(self):
        return self.__prev_out

    def get_pubkey(self):
        return self.__pubkey

    def get_sig(self):
        return self.__sig

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_script_start(self):
        return self.__script_start

    def get_script_end(self):
        return self.__script_end
