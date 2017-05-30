# import io
# import random
from clint.textui import colored,puts
from sys import stdin

if __name__ == '__main__':
    print('Welcome to NanoSQL')
    print(colored.green('> '),end='',flush=True)
    input=stdin.readline()
    print(input)

    # print(colored.red('red text'))

# with open('test.txt','w') as f:
#     for i in range(1,1000000):
#         f.write(str(i)+'\n')

# with open('test.txt','rb') as f:
#     for i in range(1,10000):
#         position=random.randint(0,1000000)
#         f.seek(100,io.SEEK_CUR)
#         a=f.read(10)
#         print(a)
#