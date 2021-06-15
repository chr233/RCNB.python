
'''
# @Author       : liggest
# @Date         : 2021-06-15 15:43:00
# @LastEditors  : Chr_
# @LastEditTime : 2021-06-15 23:30:13
# @Description  : 
'''

import os
import sys
import getopt
from . import encode, decode

usage = f"""
使用方法: {sys.argv[0]} [-d|-e] [-f] [-u encoding] text
    -d: 解码
    -e: 编码 (默认)
    -f: 把text当做文件路径而不是待加密/解密的字符串
    -u encoding: 指定编码方式(默认为 utf-8)"""


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'deu:f')
        # print(opts,args)
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(usage)
        sys.exit(2)

    func = encode
    encoding = 'utf-8'
    filemode = False

    for opt, arg in opts:
        if opt == '-e':
            func = encode
        elif opt == '-d':
            func = decode
        elif opt == '-u':
            encoding = arg
        elif opt == '-f':
            filemode = True

    if not sys.stdin.isatty():
        sys.stdin.reconfigure(encoding=encoding)
        text = sys.stdin.read()
    elif args:
        if filemode:
            try:
                with open(args[0], 'r', encoding=encoding) as f:
                    text = f.read()
            except FileNotFoundError:
                print('错误: 文件不存在')
                print(usage)
                sys.exit(2)
        else:
            text = ' '.join(args)
    else:
        print('错误: 缺少参数')
        print(usage)
        sys.exit(2)

    result = func(text, encoding=encoding)

    if sys.stdout.isatty():
        print(result)
    else:
        sys.stdout.reconfigure(encoding=encoding)
        sys.stdout.write(result)


main()
