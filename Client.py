#2018-08-17  Nam Vu  <npv14@cs16079ho>
from socket import *
import select
import sys
def dtRequest(dateOrTime):
    """This function is using for create the Request Packet that pack the number require into byte array"""
    pack = bytearray();
    pack += int(0x497e).to_bytes(2, byteorder='big')
    pack += int(0x0001).to_bytes(2, byteorder='big')
    if dateOrTime == "date":
        pack += int(0x0001).to_bytes(2, byteorder='big')
    if dateOrTime == "time":
        pack += int(0x0002).to_bytes(2, byteorder='big')
    print("Successful pack data request")
    return pack
def checkRecivedPacket(data):
    """This function is using for check if the Packet recived is Valid or not as the require"""
    valid = 0
    if len(data) >= 13:
        valid += 1
    if data[0:2].hex() == '497e':
        valid += 1
    if data[2:4].hex() == '0002':
        valid += 1
    if data[4:6].hex() == '0001' or data[4:6].hex() == '0002' or data[4:6].hex() == '0003' :
        valid += 1
    if data[6:8].hex() != '0002':
        valid += 1
    if int.from_bytes(data[6:8], 'big') < 2100:
        valid += 1
    if 1 <= int.from_bytes(data[8:9], 'big') <= 12:
        valid += 1
    if 1 <= int.from_bytes(data[9:10], 'big') <= 31:
        valid += 1
    if 0 <= int.from_bytes(data[10:11], 'big') <= 23:
        valid += 1
    if 0 <= int.from_bytes(data[11:12], 'big') <= 59:
        valid += 1
    if len(data) == 13 + int.from_bytes(data[12:13], 'big'):
        valid += 1
    if valid == 11:
        print("Packet is valid")
    else:
        print("Packet is invalid")
    return valid == 11


def main(dateOrTime, ipORDomain, portNo):
    #creat Client UDP socket
    print("Start main")
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #Packed the data request
    packRequest = dtRequest(dateOrTime)
    try:
        clientSocket.sendto(packRequest, (ipORDomain, portNo))
        print("Sent request packet")
    except:
        print("Did not find the Server")
    found = False
    #Send the request packet and waiting for response in 1 second
    reader,_, _ = select.select([clientSocket], [], [], 1)
    for i in reader:
            if i is clientSocket:
                 found = True
                 data = i.recvfrom(1024)
                 print("Recived data response")
                 packetRecived  = bytearray(data[0])
                 if checkRecivedPacket(packetRecived):
                     #Print the Text field of the packet response. It will look like:
                     """
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     >>>>>>>>>> Today’s date is August 17, 2018 <<<<<<<<<<<
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     """
                     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                     print('>>>>>>>>>>',packetRecived[13:].decode('utf8'), '<<<<<<<<<<<')
                     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    clientSocket.close()
    if not found:

        print("Packet loss")
        print("Please check IP and port number of Server")
    print("Program's closed")




def start():
    """This function is using for start the program if all arguments are valid then start the main funtion"""
    valid = True
    try:
        dateOrTime = sys.argv[1]
        if dateOrTime != "date" and dateOrTime != "time":
            valid = False
            print("Invalid input")
    except:
        print("Invalid input")

    if valid:
        try:
            ipORDomain = sys.argv[2]
            check = ipORDomain.split(".")
            if len(check) == 4:
                for i in check:
                    if int(i) >= 256 or int(i) < 0:
                        valid = False
                        break;
                if not valid:
                    print("Invalid IP")
            else:
                try:
                    #Conver the hostname to IP then check the hostname is valid or not
                    ip = getaddrinfo(ipORDomain, 'www')
                    print("ip: ", ip)
                    ipORDomain = ip[0][4][0]
                except:
                    print("Invalid Hostname")
                    valid = False
        except:
            print("Invalid input")
    if valid:
        try:
            portNo= int(sys.argv[3])
            if not (1024 < portNo < 64000):
                print("Invalid port number")
                valid = False
        except:
            print("Invalid input")


    if valid:
        main(dateOrTime, ipORDomain, portNo)

start()
"""
Command codes for testing the program:
    // Date:
    python3 Client.py date 127.0.1.1 63999
    python3 Client.py date 127.0.1.1 63998
    python3 Client.py date 127.0.1.1 63997
    // Time:
    python3 Client.py time 127.0.1.1 63999
    python3 Client.py time 127.0.1.1 63998
    python3 Client.py time 127.0.1.1 63997
"""
