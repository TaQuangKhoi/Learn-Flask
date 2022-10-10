import socket as sk
import logging as lg
from threading import Thread

lg.basicConfig(filename="check-port.log",
                format='%(asctime)s %(message)s',
                filemode='w')
logger = lg.getLogger(__name__)
logger.setLevel(lg.INFO)

sock1 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
sock2 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)


def check(x, sock=sock1):
    result = sock.connect_ex(('ts.qq.com', x))
    if result == 0:
        result_text = str(x) + ": Port is open"
        print (result_text)
        logger.info (result_text)
    else:
        result_text = str(x) + ": Port is closed"
        print (result_text)
        logger.info (result_text)

def one():
    print("Bắt đầu!!")
    x = 1
    while x <= 32767:
        check(x, sock1)
        x += 1
    sock1.close()

def two():
    print("Bắt đầu!!")
    x = 32768
    while x <= 65535:
        check(x, sock2)
        x += 1
    sock2.close()

def main():
    print("Bắt đầu!!")

    thread1 = Thread(target=one)
    thread1.start()

    thread2 = Thread(target=two)
    thread2.start()

    


main()