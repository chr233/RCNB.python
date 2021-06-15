
'''
# @Author       : Chr_
# @Date         : 2020-08-26 15:28:58
# @LastEditors  : Chr_
# @LastEditTime : 2020-08-26 23:06:04
# @Description  : RCNB
'''

from .core import RCNB

encode=RCNB.encode
encodeBytes=RCNB.encodeBytes
decode=RCNB.decode
decodeBytes=RCNB.decodeBytes

__all__ = ['core','encode','encodeBytes','decode','decodeBytes']
