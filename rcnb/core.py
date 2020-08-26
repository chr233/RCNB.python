
'''
# @Author       : Chr_
# @Date         : 2020-08-25 18:55:16
# @LastEditors  : Chr_
# @LastEditTime : 2020-08-26 22:59:51
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
    __src = __sr * __sc
    __snb = __sn * __sb
    __scnb = __sc * __snb

    def __init__(self):
        '''
        初始化RCNB类
        '''
        super().__init__()

    def __encodeByte(self, i: int) -> str:
        '''
        单字节编码
        '''
        if (i > 0xFF):
            raise ValueError('rc/nb overflow')
        if (i > 0x7F):
            i &= 0x7F
            r = f'{self.__cn[i // self.__sb]}{self.__cb[i % self.__sb]}'
        else:
            r = f'{self.__cr[i // self.__sc]}{self.__cc[i % self.__sc]}'
        return(r)

    def __encodeShort(self, i: int) -> str:
        '''
        双字节编码
        '''
        if (i > 0xFFFF):
            raise ValueError('rc/nb overflow')
        reverse = False
        if(i > 0x7FFF):
            reverse = True
            i &= 0x7FFF
        if(not reverse):
            r = [self.__cr[i // self.__scnb], self.__cc[i % self.__scnb // self.__snb],
                 self.__cn[i % self.__snb // self.__sb], self.__cb[i % self.__sb]]
        else:
            r = [self.__cn[i % self.__snb // self.__sb], self.__cb[i % self.__sb],
                 self.__cr[i // self.__scnb], self.__cc[i % self.__scnb // self.__snb]]
        return(''.join(r))

    def __decodeByte(self, s: str) -> int:
        '''
        解码成单字节
        '''
        try:
            id1 = self.__cr.index(s[0])
            id2 = self.__cc.index(s[1])
            nb = False
        except ValueError:
            try:
                id1 = self.__cn.index(s[0])
                id2 = self.__cb.index(s[1])
                nb = True
            except ValueError:
                raise ValueError('not rc/nb')
        r = (id1 * self.__sb + id2) if nb else (id1 * self.__sc + id2)
        if(r > 0x7F):
            raise ValueError('rc/nb overflow')
        r |= 0x80 if nb else 0
        return(r)

    def __decodeShort(self, s: str) -> int:
        '''
        解码成双字节
        '''
        reverse = s[0] not in self.__cr
        try:
            if(not reverse):
                idx = [self.__cr.index(s[0]), self.__cc.index(s[1]),
                       self.__cn.index(s[2]), self.__cb.index(s[3])]
            else:
                idx = [self.__cr.index(s[2]), self.__cc.index(s[3]),
                       self.__cn.index(s[0]), self.__cb.index(s[1])]
        except ValueError:
            raise ValueError('not rcnb')
        r = idx[0] * self.__scnb + idx[1] * \
            self.__snb + idx[2] * self.__sb + idx[3]
        if (r > 0x7FFF):
            raise ValueError('rcnb overflow')
        r |= 0x8000 if reverse else 0
        return(r)

    def encodeBytes(self, bs: bytes) -> str:
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
            r.append(self.__encodeShort((bs[i * 2] << 8) | bs[i * 2 + 1]))
        if(len(bs) & 1 == 1):
            r.append(self.__encodeByte(bs[-1]))
        return(''.join(r))

    def encode(self, s: str, encoding: str = 'utf-8') -> str:
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
        r = self.encodeBytes(bs)
        return(r)

    def decodeBytes(self, s: str) -> bytes:
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
            value = self.__decodeShort(s[i * 4: i * 4 + 4])
            r.append(bytes([value >> 8]))
            r.append(bytes([value & 0xFF]))
        if((len(s) & 2) == 2):
            r.append(bytes([self.__decodeByte(s[-2:])]))
        return (b''.join(r))

    def decode(self, s: str, encoding: str = 'utf-8') -> str:
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
            r = self.decodeBytes(s).decode(encoding)
        except UnicodeDecodeError:
            raise ValueError('decode error')
        return (r)
