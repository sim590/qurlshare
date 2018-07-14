# #!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Simon Désaulniers <sim.desaulniers@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import argparse

# DHT, serialization modules
import opendht
import msgpack

# Crypto modules
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Util import Padding
from Cryptodome.Protocol import KDF

########################
#  USER CONFIGURATION  #
########################

USER = "49d248e8b300550"
PWD  = "99a2b38a6216c1c"

#######################
#  PROGRAM VARIABLES  #
#######################

PRGNAME = "qurlshare"

# OpenDHT
DEFAULT_DHT_BOOTSTRAP_HOST = "bootstrap.ring.cx"
DEFAULT_DHT_BOOTSTRAP_PORT = "4222"

# Cryptodome
KEYLEN = 32 # bytes = 256bit

dht = None

# Debug prints

def print_debug(string_):
    print(PRGNAME+":", "debug:", string_, file=sys.stderr)

def print_error(string_):
    print(PRGNAME+":", "error:", string_, file=sys.stderr)

# Crypto

def encrypt(plaintext, key, keylen=KEYLEN):
    """Encrypt bytes using AES-CBC with keys of length `keylen` (defaults to
    KEYLEN: 256 bits).

    Key is passed in KDF `PBKDF2` in order to protect weak keys against brute
    force attacks.

    @param plaintext:  Data to be encrypted.
    @type  plaintext:  bytes

    @param key:  Encryption passphrase.
    @type  key:  str, bytes

    @param keylen:  Length of the key to use in bytes. Can be either 16, 24 or
                    32.
    @type  keylen:  str, bytes

    @return:  The produced ciphertext.
    @rtype :  bytes

    @raise ValueError: Incorrect padding. Happens if passphrase is incorrect.
    """
    salt      = Random.new().read(AES.block_size)
    iv        = Random.new().read(AES.block_size)
    key       = KDF.PBKDF2(key, salt, dkLen=keylen)
    plaintext = Padding.pad(plaintext, AES.block_size)
    cipher    = AES.new(key, AES.MODE_CBC, iv=iv)
    return base64.b64encode(salt + iv + cipher.encrypt(plaintext))

def decrypt(ciphertext, key, keylen=KEYLEN):
    """Decrypt bytes using AES-CBC with keys of length `keylen` (defaults to
    KEYLEN: 256 bits).

    @param ciphertext:  Data to be decrypted.
    @type  ciphertext:  bytes

    @param key:  Encryption passphrase.
    @type  key:  str, bytes

    @param keylen:  Length of the key to use in bytes. Can be either 16, 24 or
                    32.
    @type  keylen:  str, bytes

    @return:  The decrypted ciphertext.
    @rtype :  bytes

    @raise ValueError: Incorrect padding. Happens if passphrase is incorrect.
    """
    ciphertext = base64.b64decode(ciphertext)
    salt       = ciphertext[:AES.block_size]
    iv         = ciphertext[AES.block_size:2*AES.block_size]
    key        = KDF.PBKDF2(key, salt, dkLen=keylen)
    cipher     = AES.new(key, AES.MODE_CBC, iv=iv)
    return Padding.unpad(cipher.decrypt(ciphertext[2*AES.block_size:]), AES.block_size)

# Deserialization

def unpack_decrypt_dht_value(data_, pwd=''):
    """Unpack (and decrypts) a DHT value content.

    @param data_:  A DHT value.
    @type  data_:  opendht.Value

    @return: The deserialized data. A map of (key, values) pairs. A complete
             data should look like the following
             {
                b"id" : data_id
                b"data" : the_data
             }
    @rtype : dict

    @raise ValueError:  See encrypt function.
    """
    ud = None
    try:
        ud = msgpack.unpackb(data_.data)
    except Exception:
        pdata = decrypt(data_.data, pwd.encode())
        ud = msgpack.unpackb(pdata)
    return ud

def get_last_value(pvalues, pwd=''):
    """Find the last stored value on the DHT storage given a list of values
    previously recovered from the DHT.

    @param pvalues: The list of DHT values (type: opendht.Value).
    @type  pvalues: list

    @return:  Unpacked value which was the last stored on DHT.
    @rtype :  dict

    @raise ValueError:  See decrypt.
    """
    if not pvalues:
        return None
    return unpack_decrypt_dht_value(max(pvalues, key=lambda pv: unpack_decrypt_dht_value(pv, pwd)[b"id"]), pwd)

# Qutebrowser

def qute_cmd(cmd_string_):
    """Send a command to qutebrowser.

    @param cmd_string_: The command to send.
    @type  cmd_string_: str
    """
    try:
        print_debug(cmd_string_)
        k = 'QUTE_FIFO'
        cmd_fifo = os.environ[k] if k in os.environ else ''
        with open(cmd_fifo, 'w') as f:
            f.write(cmd_string_+'\n')
    except FileNotFoundError as e:
        pass

def qute_print(string_):
    """Send a message to qutebrowser user.

    @param string_: The message to send
    @type  string_: str
    """
    qute_cmd(":message-info '%s: %s'" % (PRGNAME, string_))

#####################
#  Main userscript  #
#####################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to share.", nargs='?')
    parser.add_argument("-g", "--get", help="Get shared URL.", action='store_true')
    pa = parser.parse_args()

    h = opendht.InfoHash.get(USER+PWD)
    print_debug("InfoHash: %s" % h.toString())

    dht = opendht.DhtRunner()
    dht.bootstrap(DEFAULT_DHT_BOOTSTRAP_HOST, DEFAULT_DHT_BOOTSTRAP_PORT)
    dht.run()
    print_debug("is running? %s" % dht.isRunning())

    if pa.get:
        lv = get_last_value(dht.get(h), PWD)
        if not lv:
            qute_print("No url found")
            return 1
        url = lv[b"data"].decode()
        qute_cmd(":open -t %s" % url)
        qute_print("URL found: %s" % url)
    else:
        if not pa.url:
            return
        lv = get_last_value(dht.get(h), PWD)
        last_id = lv[b"id"] if lv else -1
        pv = msgpack.packb({
            "id" : last_id+1,
            "data" : pa.url
        })
        v = opendht.Value(encrypt(pv, PWD))
        print_debug(v)
        dht.put(h, v)
        qute_print("URL shared")

if __name__ == "__main__":
    main()

#  vim: set ts=4 sw=4 tw=120 et :

