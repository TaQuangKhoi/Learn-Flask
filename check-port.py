import socket as sk
import logging as lg

lg.basicConfig(filename="check-port.log",
                format='%(asctime)s %(message)s',
                filemode='w')
logger = lg.getLogger(__name__)
logger.setLevel(lg.INFO)
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

def check(x):
    result = sock.connect_ex(('ts.qq.com', x))
    if result == 0:
        result_text = str(x) + ": Port is open"
        print (result_text)
        logger.info (result_text)
    else:
        result_text = str(x) + ": Port is closed"
        print (result_text)
        logger.info (result_text)

def main():
    print("Bắt đầu!!")
    x = 1
    while x <= 65535:
        check(x)
        x += 1
    sock.close()

main()