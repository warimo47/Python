import socket 
import struct
import random

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('192.168.0.63', 4211)) 

while True :
    message = input('Enter command : ') # 명령어 입력
    
    if message == '4': # 4를 입력하면 IF-SC400 패킷 송신
        data_IP = '192.168.0.70'
        data_time = '2020-11-17 11:46:53.054978'  # 시간 문자열은 예제와 같은 (yyyy-MM-dd HH:mm:ss.ffffff) 포맷으로 해주시면 됩니다.
        data_objNum = random.randrange(1, 41) # 리스트 최대 길이는 40입니다.

        print(data_IP + ' ' + data_time + ' ' + str(data_objNum))

        IF_SC400_header = struct.pack('B', 4) # IF-SC400
        while len(data_IP) < 15 :
            data_IP += ' '
        IF_SC400_IP = bytes(data_IP, encoding='UTF-16')
        IF_SC400_time = bytes(data_time, encoding='UTF-16')
        IF_SC400_objNum = struct.pack('B', data_objNum) # 0 - 40

        sendBuffer = IF_SC400_header + IF_SC400_IP + IF_SC400_time + IF_SC400_objNum

        for i in range(data_objNum) :
            data_objType = random.randrange(0, 3) # 0=사람, 1=차량, 2=트럭
            data_XAxis = random.uniform(1, 10)
            data_ZAxis = random.uniform(1, 10)
            randObjX = random.randrange(100, 1820)
            randObjY = random.randrange(100, 980)
            data_percent = random.uniform(0, 100)
            data_action = random.randrange(0, 5) # 0=정상상태, 1=쓰러짐, 2=월담, 3=싸움, 4=밀수
            data_color = random.randrange(0, 15) # 0=빨강, 1=주황, 2=노랑, 3=연두, 4=초록, 5=청록, 6=파랑, 7=남색, 8=보라, 9=자주, 10=분홍, 11=갈색, 12=하양, 13=회색, 14=검정
            data_red = random.randrange(0, 256)
            data_green = random.randrange(0, 256)
            data_blue = random.randrange(0, 256)

            log = str(i) + ' : ' + str(data_objType) + ' ' + str(data_XAxis) + ' ' + str(data_ZAxis) + ' '
            log += str(randObjX - 100) + ' ' + str(randObjY - 100) + ' ' + str(randObjX + 100) + ' ' + str(randObjY + 100) + ' ' + str(data_percent) + ' '
            log += str(data_action) + ' ' + str(data_color) + ' ' + str(data_red) + ' ' + str(data_green) + ' ' + str(data_blue)
            print(log)

            IF_SC400_objType = struct.pack('B', data_objType)
            IF_SC400_XAxis = struct.pack('f', data_XAxis)
            IF_SC400_ZAxis = struct.pack('f', data_ZAxis)
            IF_SC400_objX1 = struct.pack('i', randObjX - 100)
            IF_SC400_objY1 = struct.pack('i', randObjY - 100)
            IF_SC400_objX2 = struct.pack('i', randObjX + 100)
            IF_SC400_objY2 = struct.pack('i', randObjY + 100)
            IF_SC400_percent = struct.pack('f', data_percent)
            IF_SC400_action = struct.pack('B', data_action)
            IF_SC400_color = struct.pack('B', data_color)
            IF_SC400_red = struct.pack('B', data_red)
            IF_SC400_green = struct.pack('B', data_green)
            IF_SC400_blue = struct.pack('B', data_blue)

            sendBuffer += IF_SC400_objType + IF_SC400_XAxis + IF_SC400_ZAxis
            sendBuffer += IF_SC400_objX1 + IF_SC400_objY1 + IF_SC400_objX2 + IF_SC400_objY2 + IF_SC400_percent
            sendBuffer += IF_SC400_action + IF_SC400_color + IF_SC400_red + IF_SC400_green + IF_SC400_blue
        
        client_socket.send(sendBuffer)
        
    elif message == 'quit': # quit 입력하면 통신 종료
    	break

    # data = client_socket.recv(1024) 
    # print('Received from the server :',repr(data.decode())) 

client_socket.close() 
