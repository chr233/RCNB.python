from rcnb import RCNB

a = RCNB()

b = a.encode('1234')
c = a.decode(b)

print(b, c)
