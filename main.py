import socket , base64 , binascii

PORT = 53
IP = "127.0.0.1"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # defining UDP socket with IPv4 Addressing
sock.bind((IP,PORT))                                    # Binding the socket with an IP and PORT

def display(info: str,data):
    print(f"{info} - {data} and Type - {type(data)}")

def get_flags(flag_data: bytes):
    byte1 = flag_data[:1]
    byte2 = flag_data[1:2]

    # testing purpose(int -> byte)
    # byte1 = (255).to_bytes(1, byteorder='big') 
    
    rflags = ''

    # Byte - 1
    QR = '1'        # QUERY\RESPONSE
    OPCODE = ''     # OPERATION CODE
    # retrieving 4 bits from the bit position of 1-4th
    for bit in range(4,0,-1):
        if( ord(byte1) & (1<<bit) ):    # ord() - (bytes -> int) , & - BITWISE AND (1<<bit) - BIT SHIFTING
            OPCODE += '1'
        else:
            OPCODE += '0'
    #display("OPCODE",OPCODE)
    AA = '1'        # AUTHORITATIVE ANSWER
    TC = '0'        # TRUNCATION
    RD = '0'        # RECURSION DESIRED

    # Byte - 2
    RA = '0'        # RECURSION AVAILABLE
    Z  = '000'      # Reserved for future use
    RCODE = '0000'  # RESPONSE CODE

    rflags = int(QR+OPCODE+AA+TC+RD,2).to_bytes(1, byteorder='big') + int(RA+Z+RCODE).to_bytes(1, byteorder='big')

    return rflags

def get_domain_name(data: bytes):
    
    display("data",data)
    domain = []
    length = 0
    byte_pos = 0
    portion = ''

    for byte in data:
        if(byte_pos < length):
            each = (byte.to_bytes(1,'big')).decode()
            portion += each
            byte_pos += 1
        else:
            if(byte_pos > 0):
                domain.append(portion)
            byte_pos += 1
            if(byte == 0):
                break
            portion = ''
            length = byte_pos + byte

    display("Domain",domain)
    question_type = data[byte_pos:byte_pos+2]   # A Record
    display("Q",question_type)

    return (domain,question_type)

def get_record(data):

    # Domain name & question_type
    domain , question_type = get_domain_name(data)
    if question_type == b'\x00\x01':
        


def buildresponse(received_data: bytes):

    # TransactionID - 'string 0f bytes' &
    TransactionID = received_data[:2]
    TID = "0x" + binascii.hexlify(TransactionID).decode()       # 2 Bytes
    print(f"TransactionID - {TID} and type - {type(TID)}")

    # Flags
    Flags = get_flags(received_data[2:4])                       # 2 Bytes
    print(display("ResponseFlags",Flags))

    # Question Count
    QCOUNT = b'\x00\x01'

    # retrieving Records
    get_records(received_data[12:])

    return 1

print("Listening on a UDP Socket with IPv4 Addressing ...")
sock.setblocking(0) # 0 - Non-Blocking
while True:
    try:
        data , addr = sock.recvfrom(512)                    # Listening for DNS requests and IP of the sender
        response = buildresponse(data)
        # sock.sendto(response,addr)                          # Sending the response
    except BlockingIOError:
        #print("Waiting to receive requests ...")           # prints infinitely
        continue
    except Exception as e:
        print(f"En Error occured {e}")
        break

# sock.settimeout(5.0)
# while True:
#     try:
#         data , addr = sock.recvfrom(512)
#         print(data)
#         print(addr)
#     except socket.timeout:
#         print("Listening for DNS requests ...")
#     except Exception as e:
#         print(f"The error is {e}")
#         break

sock.close()
