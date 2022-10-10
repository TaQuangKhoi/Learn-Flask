import socket as sk

sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

result = sock.connect_ex(('ts.qq.com', 33446))
if result == 0:
    result_text = "Port is open"
    print (result_text)
    sock.close()
else:
    result_text = "Port is closed"
    print (result_text)
    sock.close()