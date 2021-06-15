
'''
# @Author       : Chr_
# @Date         : 2020-08-25 18:55:16
# @LastEditors  : Chr_
# @LastEditTime : 2021-06-15 23:34:28
# @Description  : RCNB-CORE
'''


class RCNB():
    '''
    RCNB类
    '''
    __cr = ['r', 'R', 'Ŕ', 'ŕ', 'Ŗ', 'ŗ', 'Ř',
            'ř', 'Ʀ', 'Ȑ', 'ȑ', 'Ȓ', 'ȓ', 'Ɍ', 'ɍ']
    __cc = ['c', 'C', 'Ć', 'ć', 'Ĉ', 'ĉ', 'Ċ',
            'ċ', 'Č', 'č', 'Ƈ', 'ƈ', 'Ç', 'Ȼ', 'ȼ']
    __cn = ['n', 'N', 'Ń', 'ń', 'Ņ', 'ņ', 'Ň',
            'ň', 'Ɲ', 'ƞ', 'Ñ', 'Ǹ', 'ǹ', 'Ƞ', 'ȵ']
    __cb = ['b', 'B', 'ƀ', 'Ɓ', 'ƃ', 'Ƅ', 'ƅ', 'ß', 'Þ', 'þ']

    __sr = len(__cr)
    __sc = len(__cc)
    __sn = len(__cn)
    __sb = len(__cb)
    # __src = __sr * __sc
    __snb = __sn * __sb
    __scnb = __sc * __snb

    @classmethod
    def __encodeByte(cls, i: int) -> str:
        '''
        单字节编码
        '''
        if (i > 0xFF):
            raise ValueError('rc/nb overflow')
        if (i > 0x7F):
            i &= 0x7F
            r = f'{cls.__cn[i // cls.__sb]}{cls.__cb[i % cls.__sb]}'
        else:
            r = f'{cls.__cr[i // cls.__sc]}{cls.__cc[i % cls.__sc]}'
        return(r)

    @classmethod
    def __encodeShort(cls, i: int) -> str:
        '''
        双字节编码
        '''
        if (i > 0xFFFF):
            raise ValueError('rc/nb overflow')
        reverse = False
        if (i > 0x7FFF):
            reverse = True
            i &= 0x7FFF
        if (not reverse):
            r = (cls.__cr[i // cls.__scnb], cls.__cc[i % cls.__scnb // cls.__snb],
                 cls.__cn[i % cls.__snb // cls.__sb], cls.__cb[i % cls.__sb])
        else:
            r = (cls.__cn[i % cls.__snb // cls.__sb], cls.__cb[i % cls.__sb],
                 cls.__cr[i // cls.__scnb], cls.__cc[i % cls.__scnb // cls.__snb])
            
        return(''.join(r))

    @classmethod
    def __decodeByte(cls, s: str) -> int:
        '''
        解码成单字节
        '''
        try:
            id1 = cls.__cr.index(s[0])
            id2 = cls.__cc.index(s[1])
            nb = False
        except ValueError:
            try:
                id1 = cls.__cn.index(s[0])
                id2 = cls.__cb.index(s[1])
                nb = True
            except ValueError:
                raise ValueError('not rc/nb')
        r = (id1 * cls.__sb + id2) if nb else (id1 * cls.__sc + id2)
        if (r > 0x7F):
            raise ValueError('rc/nb overflow')
        r |= 0x80 if nb else 0
        return(r)

    @classmethod
    def __decodeShort(cls, s: str) -> int:
        '''
        解码成双字节
        '''
        reverse = s[0] not in cls.__cr
        try:
            if (not reverse):
                idx = (cls.__cr.index(s[0]), cls.__cc.index(s[1]),
                       cls.__cn.index(s[2]), cls.__cb.index(s[3]))
            else:
                idx = (cls.__cr.index(s[2]), cls.__cc.index(s[3]),
                       cls.__cn.index(s[0]), cls.__cb.index(s[1]))
        except ValueError:
            raise ValueError('not rcnb')
        r = idx[0] * cls.__scnb + idx[1] * \
            cls.__snb + idx[2] * cls.__sb + idx[3]
        if (r > 0x7FFF):
            raise ValueError('rcnb overflow')
        r |= 0x8000 if reverse else 0
        return(r)

    @classmethod
    def encodeBytes(cls, bs: bytes) -> str:
        '''
        字节编码

        参数:
            bs: 字节数据
        返回:
            str: 密文
        '''
        r = []
        l = len(bs) >> 1
        for i in range(0, l):
            r.append(cls.__encodeShort((bs[i * 2] << 8) | bs[i * 2 + 1]))
        if (len(bs) & 1 == 1):
            r.append(cls.__encodeByte(bs[-1]))
        return(''.join(r))

    @classmethod
    def encode(cls, s: str, encoding: str = 'utf-8') -> str:
        '''
        文本编码

        参数:
            s: 明文
            encoding: 字符串编码方式
        返回:
            str: 密文
        '''
        assert isinstance(s, str), 's must be str'
        bs = s.encode(encoding)
        r = cls.encodeBytes(bs)
        return(r)

    @classmethod
    def decodeBytes(cls, s: str) -> bytes:
        '''
        解码为字节

        参数:
            s: 密文
        返回:
            bytes: 二进制数据
        '''
        assert isinstance(s, str), 's must be str'
        if (len(s) & 1):
            raise ValueError('invalid length')
        r = []
        l = len(s) >> 2
        for i in range(0, l):
            value = cls.__decodeShort(s[i * 4: i * 4 + 4])
            r.append(bytes([value >> 8]))
            r.append(bytes([value & 0xFF]))
        if ((len(s) & 2) == 2):
            r.append(bytes([cls.__decodeByte(s[-2:])]))
        return (b''.join(r))

    @classmethod
    def decode(cls, s: str, encoding: str = 'utf-8') -> str:
        '''
        解码为文本

        参数:
            s: 密文
            encoding: 字符串编码方式
        返回:
            str: 明文
        '''
        assert isinstance(s, str), 's must be str'
        try:
            r = cls.decodeBytes(s).decode(encoding)
        except UnicodeDecodeError:
            raise ValueError('decode error')
        return(r)
