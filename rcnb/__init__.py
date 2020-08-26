
'''
# @Author       : Chr_
# @Date         : 2020-08-26 15:28:58
# @LastEditors  : Chr_
# @LastEditTime : 2020-08-26 23:05:37
# @Description  : RCNB
'''

'''
USAGE:
from rcnb import RCNB

encoder = RCNB()

print(encoder.encode("Who NB?"))
# ȐȼŃƅȓčƞÞƦȻƝƃŖć

print(encoder.decode("ȐĉņþƦȻƝƃŔć"))
# RCNB!
'''

from .core import RCNB

__all__ = ['core']
