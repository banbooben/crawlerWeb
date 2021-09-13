from Crypto.Cipher import AES
import base64
import json
import hashlib


class JiaduAes:
    def __init__(self, key="syzn@123", iv="0908070605040302"):
        self.key = self.add_to_16(key)
        self.iv = iv

    # 16位填充
    def pad(self, data):
        length = 16 - (len(data) % 16)
        return data.encode(encoding='utf-8') + (chr(length) * length).encode(encoding='utf-8')

    # 截取填充
    def unpad(self, data):
        print(-(data[-1] if type(data[-1]) == int else ord(data[-1])))
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

    # 补足字符串长度为16的倍数
    def add_to_16(self, s):
        while len(s) % 16 != 0:
            s += '\0'
        return str.encode(s)

    # 加密
    def AED_Encrypt(self, data):
        data = json.dumps(data)
        data = data.replace(" ", "")
        data = self.pad(data)

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv.encode('utf8'))
        encryptedbytes = cipher.encrypt(data)
        # 加密后得到的是bytes类型的数据
        encodestrs = base64.b64encode(encryptedbytes)
        # 使用Base64进行编码,返回byte字符串
        enctext = encodestrs.decode('utf8')
        # 对byte字符串按utf-8进行解码
        return enctext

    def AED_Decrypt(self, data):
        encodebytes = base64.b64decode(data.encode('UTF-8'))
        # encodebytes = base64.decodebytes(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv.encode('utf8'))
        text = cipher.decrypt(encodebytes)
        text = self.unpad(text)
        text = json.loads(text)
        return text

    # md5加密
    def md5_encrypt(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode())
        a_md5 = md5.hexdigest()
        return a_md5.upper()


if __name__ == '__main__':
    # data = {'nowTime': '2020-06-28 14:26:25', 'isOpenTcp': 1, 'tcpPort': 8083, 'token': 'qwertyuiop0123456789'}
    # data1 = {"nowTime":  '2020-06-28 14:26:25', "isActivation": 0, "lstFaceUpdateId": 1, "lstBlackIdCardUpdateId": 1,
    #         "lstWhiteIdCardUpdateId": 1, "lstNoticeInfoUpdateId": 1, "lstGuardTimeRuleUpdateId": 1}
    #
    # new_data = JiaduAes().AED_Encrypt(data=aaa)
    # print(new_data)
    endata = "aJFTHxa3RuX9UtarMlkGdA2efIO0/9r9R3Vm0BqABgovgHFzIw1MXM789uOknQhKWraBPdPEZEUsZ6chVOJFs5+zG5sXCs0NuUsrtnYfSJFASqw6UX4lPrKls74mUCf/dJBthrxSbduG339zLcxk8aBqIwMxSjPOtyco1sAGIDVwN0oUlaciD01GIBIIlhNxhv9vz8S92ijg4X/WuOI4U3UDg1RRsfEzS8uVuZeFFENeQZiAk5NVMfE2dhAQI14l"
    # endata1 = "fAJHUyVT1cpp2rEJdAOR/Qzv4zXOI2BZcuC4YWfnvKt5tiE0tXmfoGCKOzVYLmk94yAqVoyTyzZrwvQz7up8f2nafoEFFS55mIHqLaXgoYuLoDu7X7FPhLfUi5v7gZbQYt8GQsFrft5tbhAgdrnA8fxxKTtwjN4gombERc8y4wz6qhlFH7kQb/tbzGnoz0wizE7FobMf1RAY5usaYeW/8efCig+2HFRtXIEwMZCO7fM6p9hfOdna41CIxyOWz4tMDF3bfdxeXJ5HL8329w+MOA=="
    # print(JiaduAes().AED_Decrypt(endata),"end1")

    content = {"isClear": 0, "dataList": [
        {"updateId": 1, "updateStatus": 0, "personId": "0001", "name": "陈帅涛", "personNo": "0001",
         "personCoverImg": "http://192.168.10.100:9092/static/0024.jpg", "identifyCardNumber": "",
         "certificateType": -1, "certificateNumber": "", "effectiveBegin": "2020-06-29 09:50:57",
         "effectiveEnd": "2021-06-29 09:50:57", "personInfoMd5": "", "faceGroupId": 1, "guardTimeRuleIds": [],
         "dataType": 1, "dataInfo": {"dataId": "0001"}},
        {"updateId": 2, "updateStatus": 0, "personId": "0002", "name": "葛猛", "personNo": "0002",
         "personCoverImg": "http://192.168.10.100:9092/static/0006.jpg", "identifyCardNumber": "",
         "certificateType": -1, "certificateNumber": "", "effectiveBegin": "2020-06-29 09:50:57",
         "effectiveEnd": "2021-06-29 09:50:57", "personInfoMd5": "", "faceGroupId": 1, "guardTimeRuleIds": [],
         "dataType": 1, "dataInfo": {"dataId": "0002"}}]}
    # print(JiaduAes().AED_Encrypt(data=content))

    content = {"isClear": 0,
               "dataList": [
                   {"updateId": 1,
                    "updateStatus": 0,
                    "personId": "0001",
                    "name": "陈帅涛",
                    "personNo": "0001",
                    "personCoverImg": "http://192.168.10.100:9092/static/0024.jpg",
                    "identifyCardNumber": "",
                    "certificateType": 0,
                    "certificateNumber": "",
                    "effectiveBegin": "2020-06-29 09:50:57",
                    "effectiveEnd": "2021-06-29 09:50:57",
                    "personInfoMd5": "",
                    "faceGroupId": 1,
                    "guardTimeRuleIds": [],
                    "dataType": 1,
                    "dataInfo": {
                        "dataId": "0001",
                        "faceImg": "http://192.168.10.100:9092/static/0006.jpg",
                        "faceImgMd5": "BDAF6C3CC80F84C12C87FA814004E1DF",
                        "cardNumber": "",
                        "cardPassword": "",
                        "algorithmVersion": "",
                        "feaData": "",
                    }
                    }
               ]
               }
    # print(AED_Decrypt(endata))
    # print(AED_Decrypt(new_data),"new_data")
    print(JiaduAes().AED_Encrypt(content))
    # print(JiaduAes().md5_encrypt("http://192.168.10.100:9092/static/0006.jpg"))
