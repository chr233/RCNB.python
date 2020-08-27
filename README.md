# RCNB.Python [![Codacy Badge][codacy_b]][codacy] [![PyPI][pypi_v_b]][pypi] [![License][license_b]][License]

The world is based on RC. Thus, *everything* can be encoded into RCNB.

RCNB is available in various languages: **Python** [JavaScript](https://github.com/rcnbapp/RCNB.js) [C](https://github.com/rcnbapp/librcnb) [PHP](https://github.com/rcnbapp/RCNB.php) [Pascal](https://github.com/rcnbapp/RCNB.pas) ([more..](https://github.com/rcnbapp/))

## Why RCNB?

### RCNB vs Base64

|           | Base64       | RCNB                                                          |
| --------- | ------------ | ------------------------------------------------------------- |
| Speed     | ❌ Fast       | ✔️ Slow, motivate Intel to improve their CPU                   |
| Printable | ❌ On all OS  | ✔️ Only on newer OS, motivate users to upgrade their legacy OS |
| Niubility | ❌ Not at all | ✔️ RCNB!                                                       |
| Example   | QmFzZTY0Lg== | ȐĉņþƦȻƝƃŔć                                                    |

## Install

```bash
>$ pip install rcnb
```

## Usage

```python
from rcnb import RCNB

encoder = RCNB()

print(encoder.encode("Who NB?"))
# ȐȼŃƅȓčƞÞƦȻƝƃŖć

print(encoder.decode("ȐĉņþƦȻƝƃŔć"))
# RCNB!
```

  [codacy_b]: https://app.codacy.com/project/badge/Grade/e69b178927b74f5983ba22d403b39551
  [codacy]: https://www.codacy.com/manual/chr233/RCNB.python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chr233/RCNB.python&amp;utm_campaign=Badge_Grade
  [pypi_v_b]: https://img.shields.io/pypi/v/rcnb
  [pypi]: https://pypi.org/project/rcnb/
  [license]: https://github.com/chr233/RCNB.python/blob/master/license
  [license_b]: https://img.shields.io/github/license/chr233/RCNB.python
