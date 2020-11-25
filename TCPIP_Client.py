import socket 
import struct

# header
magicCode = 1234
pType = 12
pVer = 1

# IF-SC400
IF_SC400_PACKET_TYPE = 4
IF_SC400_IP = bytes('192.168.0.101', encoding='UTF-8')
OBJECT_TYPE = 2 # 0=사람, 1=차량, 2=트럭
IF_SC400_TIME = bytes('2020-11-17 11:46:53.054978', encoding='UTF-8') # 시간 문자열은 예제와 같은 (yyyy-MM-dd HH:mm:ss.ffffff) 포맷으로 해주시면 됩니다. 
OBJ_X1 : float = 11.112345
OBJ_Y1 : float = 22.222222
OBJ_WIDTH : float = -23.25
OBJ_HEIGHT : float = 20.42
PERSENT : float = 50.54
IF_SC400_Struct = (IF_SC400_PACKET_TYPE, IF_SC400_IP, OBJECT_TYPE, IF_SC400_TIME, OBJ_X1, OBJ_Y1, OBJ_WIDTH, OBJ_HEIGHT, PERSENT)
IF_SC400_Format = '<B 15s B 30s f f f f f'
IF_SC400_Packer = struct.Struct(IF_SC400_Format)
IF_SC400_Packet = IF_SC400_Packer.pack(*IF_SC400_Struct)

# IF-SC500
IF_SC500_PACKET_TYPE = 5
IF_SC500_IP = bytes('192.168.0.101', encoding='UTF-8')
IF_SC500_TIME = bytes('2020-11-17 14:10:53.123456', encoding='UTF-8') # 시간 문자열은 예제와 같은 (yyyy-MM-dd HH:mm:ss.ffffff) 포맷으로 해주시면 됩니다. 
ACTION = 2 # 0=정상상태, 1=쓰러짐, 2=월담, 3=싸움, 4=밀수
COLOR = 0 # 0=빨강, 1=주황, 2=노랑, 3=연두, 4=초록, 5=청록, 6=파랑, 7=남색, 8=보라, 9=자주, 10=분홍, 11=갈색, 12=하양, 13=회색, 14=검정
IF_SC500_Struct = (IF_SC500_PACKET_TYPE, IF_SC500_IP, IF_SC500_TIME, ACTION, COLOR)
IF_SC500_Format = '<B 15s 30s B B'
IF_SC500_Packer = struct.Struct(IF_SC500_Format)
IF_SC500_Packet = IF_SC500_Packer.pack(*IF_SC500_Struct)

HOST = '192.168.0.58' # Server IP
PORT = 4211

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 

# 키보드로 입력한 문자열을 서버로 전송하고 
# quit를 입력할 때 까지 반복합니다.

while True: 

    message = input('Enter command : ')
    
    if message == '4':
        client_socket.send(IF_SC400_Packet)

    elif message == '5':
        client_socket.send(IF_SC500_Packet)
        
    elif message == 'quit':
    	break

    # data = client_socket.recv(1024) 
    # print('Received from the server :',repr(data.decode())) 

client_socket.close() 
