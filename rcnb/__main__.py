import sys,getopt,os
from . import encode,decode

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'deu')
        #print(opts,args)
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(f"""使用方法: {sys.argv[0]} [-d|-e|-u] [text|file|-] [encoding]
        -d, -u: 解码
        -e: 编码 (默认)
        encoding 默认为 utf-8""")
        sys.exit(2)

    func = encode
    for o, _ in opts:
        if o == '-e': func = encode
        if o == '-d': func = decode
        if o == '-u': func = decode
    encoding='utf-8'
    if args and args[0]!='-':
        if len(args)>1:
            encoding=args[-1]
        print(f'encoding:{encoding}')
        if os.path.isfile(args[0]):
            with open(args[0],'r',encoding=encoding) as f:
                text=f.read()
        else:
            text=args[0]
    else:
        text=sys.stdin.read()
    print(func(text,encoding=encoding))

main()
    



