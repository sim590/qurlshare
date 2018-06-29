# qurlshare

A Qutebrowser userscript enabling *secure* sharing of an URL between qutebrowser
instances without need of any centralized service.

More precisely, it is a URL sharing script running over a distributed hash
table. Everytime you paste a new URL, the last pasted URL is recovered.


## Dependencies

- [libopendht][];
- [python-opendht][libopendht];
- [PyCrypto][];

[libopendht]: https://github.com/savoirfairelinux/opendht
[PyCrypto]: https://www.dlitz.net/software/pycrypto/

<!-- vim: set ts=4 sw=4 tw=80 et :-->

