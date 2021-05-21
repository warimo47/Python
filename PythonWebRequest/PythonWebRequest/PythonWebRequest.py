import requests as rq

cctvIP = '192.168.0.60'
URL = 'http://' + cctvIP + '/cgi-bin/param.cgi?action=list&group=PTZPOS&channel=0'

headers = {'Authorization': 'Basic YWRtaW46YWRtaW4='}

res = rq.get(URL, headers=headers)

print(res.text)

ptzStr = res.text.split('\n')

print(ptzStr[1][19:])
print(ptzStr[2][20:])
print(ptzStr[3][20:])
