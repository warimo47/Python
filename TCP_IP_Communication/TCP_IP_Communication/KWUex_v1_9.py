import socket 
import struct
import random

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('192.168.0.63', 4211)) # IP 주소를 알맞게 변경하세요.

while True :
    message = input('Enter command : ') # 명령어 입력
    
    if message == '5': # 5를 입력하면 IF-SC500 패킷 송신
        data_IP = '192.168.0.80'
        data_time = '2020-12-15 13:05:04.012345'  # 시간 문자열은 예제와 같은 (yyyy-MM-dd HH:mm:ss.ffffff) 포맷으로 해주시면 됩니다.
        data_objNum = random.randrange(1, 41) # 리스트 최대 길이는 40입니다.

        print(data_IP + ' ' + data_time + ' ' + str(data_objNum))

        IF_SC500_header = struct.pack('B', 5) # IF-SC500
        while len(data_IP) < 15 :
            data_IP += ' '
        IF_SC500_IP = bytes(data_IP, encoding='UTF-16')
        IF_SC500_time = bytes(data_time, encoding='UTF-16')
        IF_SC500_objNum = struct.pack('B', data_objNum) # 0 - 40

        sendBuffer = IF_SC500_header + IF_SC500_IP + IF_SC500_time + IF_SC500_objNum

        for i in range(data_objNum) :
            data_objType = random.randrange(0, 15) # 0=미확인 객체, 1=타워 크레인, 2=갠트리 크레인, 3=스프레더, 4=선박, 5=리치스태커, 6=지게차, 7=야드 섀시, 8=야드 트럭, 9=기타 트럭, 10=차량, 11=조명 타워, 12=컨테이너, 13=컨테이너 홀더, 14=컨테이너 콘
            data_XAxis = random.uniform(1, 10)
            data_ZAxis = random.uniform(1, 10)
            randObjX = random.randrange(100, 1820)
            randObjY = random.randrange(100, 980)
            data_percent = random.uniform(0, 100)

            log = str(i) + ' : ' + str(data_objType) + ' ' + str(data_XAxis) + ' ' + str(data_ZAxis) + ' '
            log += str(randObjX - 100) + ' ' + str(randObjY - 100) + ' ' + str(randObjX + 100) + ' ' + str(randObjY + 100) + ' ' + str(data_percent)
            print(log)

            IF_SC500_objType = struct.pack('B', data_objType)
            IF_SC500_XAxis = struct.pack('f', data_XAxis)
            IF_SC500_ZAxis = struct.pack('f', data_ZAxis)
            IF_SC500_objX1 = struct.pack('i', randObjX - 100)
            IF_SC500_objY1 = struct.pack('i', randObjY - 100)
            IF_SC500_objX2 = struct.pack('i', randObjX + 100)
            IF_SC500_objY2 = struct.pack('i', randObjY + 100)
            IF_SC500_percent = struct.pack('f', data_percent)

            sendBuffer += IF_SC500_objType + IF_SC500_XAxis + IF_SC500_ZAxis
            sendBuffer += IF_SC500_objX1 + IF_SC500_objY1 + IF_SC500_objX2 + IF_SC500_objY2 + IF_SC500_percent
        
        client_socket.send(sendBuffer)
        
    elif message == 'quit': # quit 입력하면 통신 종료
    	break

    # data = client_socket.recv(1024) 
    # print('Received from the server :',repr(data.decode())) 

client_socket.close() 
