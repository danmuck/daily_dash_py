
import json, hashlib, datetime, os
from random import randint

REC_OPTS = [
    "dog", "cat", "bird", "mouse", "leopard", "jaguar", "panther", "cheetah", "bobcat",
    "tomcat", "lion", "tiger", "liger", "bengal", "tabby", "fox", "fenix", "bear", "polarbear",
    "grizzly", "panda", "koala", "klondike", "scarecrow", "tinman", "dorothy", "munchkin",
    "todo", "emerald", "ruby", "diamond", "sapphire", "topaz", "amethyst", "malachite",
    "parrot", "songbird", "cardinal", "bluejay", "jay", "hawk", "eagle", "robyn", "snake",
    "boa", "constrictor", "python", "rattlesnake", "kingsnake", "viper", "canine", "retriever",
    "sloth", "oppossum", "raccoon", "squirrel", "groundhog", "beaver", "dirtpig", "pig",
    "cow", "horse", "hen", "chicken", "chick", "rooster", "llama", "camel", "alpaca", "farm",
    "city", "state", "country", "usa", "canada", "england", "spain", "germany", "france", 
    "sweden", "norway", "iceland", "greenland", "mexico", "argentina", "panama", "japan",
    "korea", "china", "ukraine", "russia", "australia", "newzealand", "malasia", "egypt",
    "madagascar", "africa", "israel", "turkey", "mono", "di", "tri", "tetra", "penta", "hexa", 
    "hepta", "octo", "ennea", "deca", "monkey", "gorilla", "baboon", "book", "page", "leather"

]

class Wallet_:
    address_:str
    root_b:str
    balance:float
    txn_hist:list
    inv_data:dict

    recover_hash:str
    signer_hash:str
    wallet_:dict

    f_curr:dict

    def __init__(self,
        root_b:str,
        balance:float,
        init_txn:dict={},
        inv_data={},
        address=None,
        rec_hash=None,
        sign_hash=None,
        txn_hist=[],
        new_=True,
    ) -> None:
        if new_ is not True:
            self.address_ = address
            self.recover_hash = rec_hash
            self.signer_hash = sign_hash
            self.txn_hist = txn_hist
            self.root_b = root_b[:-5]
            self.balance = balance
            self.inv_data = inv_data
        else:
            self.recover_hash = None
            self.signer_hash = None
            self.txn_hist = []
            self.root_b = root_b[:-5]
            self.balance = balance
            self.inv_data = inv_data
            self.address_ = self.init_wallet()
        self.txn_hist.append(init_txn)

        self.wallet_ = dict

    def init_wallet(self):
        hash_r, list_ = self.gen_recovery()
        hash_p, pass_ = self.set_signer()
        encoded_addr = json.dumps('_'.join([hash_r, hash_p, self.root_b])).encode()
        hash_ = ''.join(('0x', hashlib.sha256(encoded_addr).hexdigest()))
        self.address_ = hash_
        print(f"""
           [ Ready to show password and passphrase for new wallet address:  ]

        !!   {hash_}

           [ This is the last time that you will see these so write them    ] 
           [     down in an appropriate place for safe keeping!!            ]
            
        """)
        u_input = input("Ready? (Y/n) \n: ").casefold()
        if u_input in ['y', 'yes', '']:
            print("Signer Password:", pass_)
            i = 1
            for word in list_:
                print('  ', i, word)
                i+=1

        return hash_

    def gen_wallet(self):
        wallet_ = {
            self.address_: {
                "root_b": self.root_b,
                "balance": self.balance,
                "txn_hist": self.txn_hist,
                "inv_data": self.inv_data,
                "rec_hash": self.recover_hash,
                "sign_hash": self.signer_hash
            }
        }
        self.wallet_ = wallet_
        return wallet_

    def new_txn(self):
        pass

    def gen_recovery(self):
        REC_OPTS
        your_opts = []
        i = 1
        while len(your_opts) < 12:
            new_opt = REC_OPTS[randint(0, len(REC_OPTS) - 1)]
            if new_opt not in your_opts:
                your_opts.append(new_opt)
                print(i, new_opt)
                i+=1
        encoded_opts = json.dumps(your_opts).encode()
        hash_ = ''.join(('0x', hashlib.sha512(encoded_opts).hexdigest()))
        if self.recover_hash is None:
            self.recover_hash = hash_
        print(self.recover_hash, your_opts)
        return hash_, tuple(your_opts)

    def set_signer(self):
        password = input("Enter a Signer-password: ")
        encoded_pass = json.dumps(password).encode()
        hash_ = ''.join(('0x', hashlib.sha512(encoded_pass).hexdigest()))
        if self.signer_hash is None:
            self.signer_hash = hash_
        print(password, hash_)
        return hash_, password

    def print_wallet(self):
        pass

    def store_wallet(self):
        try:
            os.mkdir(f"{os.getcwd()}/user_data/")
        except FileExistsError:
            pass
        with open(f"{os.getcwd()}/user_data/wallet.json", "x") as file:
            wallet_data =  json.dumps(self.gen_wallet(), indent=2)
            file.write(wallet_data)        

# w = Wallet_("0xlaksjd", 23.0, {})


    
class Txn_:
    to_addr:str
    from_addr:str
    txn_data:dict
    amount:float
    miner_fee:float
    timestamp:str
    type_:str

    txn_hash:str
    final_txn:dict

    def __init__(self,
        to_addr,
        from_addr,
        txn_data,
        amount,
        miner_fee,
        type_

    ) -> None:
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.txn_data = txn_data
        self.amount = amount
        self.miner_fee = miner_fee
        self.type_ = type_
        self.timestamp = str(datetime.datetime.now())

        self.raw_txn = {
            "to": self.to_addr,
            "from": self.from_addr,
            "data": self.txn_data,
            "amt": self.amount,
            "fee": self.miner_fee,
            "type": self.type_,
            "time": self.timestamp,
            }
        self.txn_finalize()
        
    def txn_in_validator(self):
        pass

    def txn_out_validator(self):
        pass

    def txn_finalize(self):
        self.txn_hash = self.hash_txn_(self.raw_txn)
        self.final_txn = {self.txn_hash: self.raw_txn}
        return self.final_txn

    def txn_compression(self):
        pass


    def hash_txn_(self, raw_txn:dict) -> str:
        '''
            Hash a txn and return the cryptographic hash value of the txn
                convert a string -> bytes and return encrypted hash
        '''    
        encoded_txn = json.dumps(raw_txn).encode()
        return ''.join(('0x', hashlib.sha256(encoded_txn).hexdigest()))