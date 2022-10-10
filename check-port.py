import socket as sk
import logging as lg

sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

lg.basicConfig(filename="check-port.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = lg.getLogger(__name__)
logger.setLevel(lg.INFO)

print("Bắt đầu!!")
for x in range(65535):
    try:
        result = sock.connect_ex(('ts.qq.com', x))
        if result == 0:
            result_text = str(x) + ": Port is open"
            print (result_text)
            logger.info (result_text)
            sock.close()
        else:
            result_text = str(x) + ": Port is closed"
            print (result_text)
            logger.info (result_text)
            sock.close()
    except Exception as e:
        logger.error (e)
        sock.close()

