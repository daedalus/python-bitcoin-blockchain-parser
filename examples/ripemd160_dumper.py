# Copyright (C) 2015-2016 The bitcoin-blockchain-parser developers
#
# This file is part of bitcoin-blockchain-parser.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of bitcoin-blockchain-parser, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

import sys
from blockchain_parser.blockchain import Blockchain
import binascii 
import bitcoin
import hashlib

from fastBloomFilter import bloom

def hash160(s):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(s)
    rip.update(sha.digest())
    #print ( "key_hash = \t" + rip.hexdigest() )
    return rip.digest()  # .hexdigest() is hex ASCII

Gigs = 8
bf = bloom.BloomFilter(array_size=Gigs*(1024**3),do_bkp=False,do_hashing=False,fast=False)

blockchain = Blockchain(sys.argv[1],blkfilestart=0)
for block in blockchain.get_unordered_blocks():
    for transaction in block.transactions:
        for output in transaction.outputs:
            sh = output._script_hex
            if sh != None:
                addr = None
                if sh[0] == 0x41 and sh[1] == 0x04:
                    pub = sh[1:-1]
                    #print(binascii.hexlify(pub))
                    addr = hash160(pub)
                if sh[0] == 0x21 and sh[1] == 0x03:
                    pub = sh[1:-1]
                    #print(binascii.hexlify(pub))
                    addr = hash160(pub)
                if sh[0:3] == b'v\xa9\x14' and sh[-2::] == b'\x88\xac':
                    addr = sh[3:-2]
                    #print(binascii.hexlify(addr))
                if sh[0:2] == b'xa9\x14' and sh[-1] == b'\xac':
                    addr = sh[2:-1]
                    #print(binascii.hexlify(addr))
                if addr != None:
                    if bf.update(addr) == False:
                        print(addr.hex())
