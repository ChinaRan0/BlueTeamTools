# -*- coding:utf-8 -*-
from UiShow.CryptoToolGUI import CryptoToolGUI
from Code.CryptoEnCode import *

class MaKaBaKaTools:
    def __init__(self):
        CryptoToolGUI('玛卡巴卡加密工具箱', MaKaBaKaEncode, MaKaBaKaDecode)
class Base64Tools:
    def __init__(self):
        CryptoToolGUI('Base64加密工具箱', Base64EnCode, Base64Decode)
class Urlcode:
    def __init__(self):
        CryptoToolGUI("URL编码解码工具",UrlcodeEncode, UrlcodeDecode)
