# qurlshare

A [Qutebrowser][] userscript enabling *secure* sharing of an URL between qutebrowser
instances without need of any centralized service.

More precisely, it is a URL sharing script running over a distributed hash
table. Everytime you paste a new URL, the last pasted URL is recovered.

## How to use

Place the script somewhere on your system. Let's say it's installed at
`~/bin/qurlshare.py`. Then, you can do as follows in qutebrowser in order to
share an URL:

```
:spawn --userscript /usr/bin/python3 ~/bin/qurlshare.py {url}
```

In order to recover the URL, simply do:

```
:spawn --userscript /usr/bin/python3 ~/bin/qurlshare.py -g
```

This will open a tab in the Qutebrowser window with the recovered URL.

## Security

User configuration protects his data. The script can be configured directly by
editing variables at the top of the script:

```python
########################
#  USER CONFIGURATION  #
########################

USER = "49d248e8b300550"
PWD  = "99a2b38a6216c1c"
```

Username and password can be of any length. The username and password are used
to derive a storage location on the DHT so make sure to pick something that is
unique if you don't want to end up with someone else (encrypted) data.

The key used to encrypt is the result of passing `PWD` into some *Key Derivation
Function* which has the effect of increasing the computationnal effort of
bruteforcing your password. The *KDF* used is [PBKDF2][] from [PyCryptodome][]
python module.

## Dependencies

- Python version 3
- [libopendht][] (tested with version 1.6.0)
- [python3-opendht][libopendht]
- [msgpack][]
- [PyCryptodome][]

## Roadmap

1. Configure username and password outside of the script.

## Author

[Simon Désaulniers][sim590] (<sim.desaulniers@gmail.com>)

[Qutebrowser]: http://qutebrowser.org/
[libopendht]: https://github.com/savoirfairelinux/opendht
[msgpack]: https://pypi.org/project/msgpack/
[PyCryptodome]: https://www.pycryptodome.org/en/latest/src/introduction.html
[PBKDF2]: https://www.pycryptodome.org/en/latest/src/protocol/kdf.html#Crypto.Protocol.KDF.PBKDF2
[sim590]: https://github.com/sim590

<!-- vim: set ts=4 sw=4 tw=80 et :-->

