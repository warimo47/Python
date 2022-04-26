import requests


def GetPTZ(_cctv_ip):
    url = f"http://{_cctv_ip}/cgi-bin/param.cgi?action=list&group=PTZPOS&channel=0"
    headers = {"Authorization": "Basic YWRtaW46YWRtaW4="}
    res = requests.get(url, headers=headers)

    print(res.text)


def SetPTZ(_cctv_ip):
    pan = "0"
    tilt = "9000"
    zoom = "0"
    url = f"http://{_cctv_ip}/cgi-bin/param.cgi?action=update&group=PTZPOS&channel=0&" \
          f"PTZPOS.panpos={pan}&PTZPOS.tiltpos={tilt}&PTZPOS.zoopos={zoom}"
    headers = {"Authorization": "Basic YWRtaW46YWRtaW4="}
    res = requests.get(url, headers=headers)


def CalibNow(_cctv_ip):
    url = f"http://{_cctv_ip}/cgi-bin/param.cgi?action=update&" \
          f"group=PTZCALIBRATION&PTZCALIBRATION.enable=1&PTZCALIBRATION.calibnow=1"
    headers = {"Authorization": "Basic YWRtaW46YWRtaW4="}
    res = requests.get(url, headers=headers)


if __name__ == "__main__":
    # SetPTZ("192.168.0.60")

    # time.sleep(1.0)

    # GetPTZ("192.168.0.60")

    CalibNow("192.168.0.60")
