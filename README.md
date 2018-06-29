# qurlshare

A Qutebrowser userscript enabling *secure* sharing of an URL between qutebrowser
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


## Dependencies

- Python version 3
- [libopendht][]
- [python3-opendht][libopendht]
- [msgpack][]
- [PyCryptodome][]


[libopendht]: https://github.com/savoirfairelinux/opendht
[msgpack]: https://pypi.org/project/msgpack/
[PyCryptodome]: https://www.pycryptodome.org/en/latest/src/introduction.html
[PBKDF2]: https://www.pycryptodome.org/en/latest/src/protocol/kdf.html#Crypto.Protocol.KDF.PBKDF2
[sim590]: https://github.com/sim590

<!-- vim: set ts=4 sw=4 tw=80 et :-->

