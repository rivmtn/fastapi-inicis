import os

from dotenv import load_dotenv

load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
SERVER_URL = os.getenv("SERVER_URL")
MID = os.getenv("MID")
SIGN_KEY = os.getenv("SIGN_KEY")
INI_API_KEY = "Sd4f65QL89=="
INI_API_IV = "Sd4f65QL89=="

'''
[테스트 계정 정보]
테스트 MID : INIpayTest
용도 : 일반결제
signkey    : SU5JTElURV9UUklQTEVERVNfS0VZU1RS
INIAPI key : ItEQKi3rY7uvDS8l
INIAPI iv   : HYb3yQ4f65QL89==
모바일 hashkey : 3CB8183A4BE283555ACC8363C0360223
'''