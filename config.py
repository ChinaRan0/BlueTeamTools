import subprocess
import webbrowser
import os
def Autoruns():
    # Autoruns(查启动项服务等)
    subprocess.Popen("Tools\BT-Response\Autoruns\Autoruns64.exe",shell=True)
def AutorunsBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\Autoruns & explorer .\\",shell=True)

def BrowsingHistoryView():
    # BrowsingHistoryView浏览器记录查看工具
    subprocess.Popen("Tools\BT-Log\BrowsingHistoryView\BrowsingHistoryView.exe",shell=True)
def BrowsingHistoryViewBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\BrowsingHistoryView & explorer .\\",shell=True)
def Ddun():
    # D盾
    subprocess.Popen("Tools\BT-Response\Ddun\D_Safe_Manage.exe",shell=True)
def DdunBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\Ddun & explorer .\\",shell=True)

def DaoMuBiJi():
    subprocess.Popen('cd Tools\moyu\ & explorer .\\',shell=True)
def DaoMubijiBrowser(event=None):
    subprocess.Popen("cd Tools\moyu & explorer .\\",shell=True)

def Everything():
    # Everything文件搜索
    subprocess.Popen("Tools\BT-Tools\Everything\Everything.exe",shell=True)
def EverythingBrowser(event=None):  
    # Everything文件搜索
    subprocess.Popen("cd Tools\BT-Tools\Everything & explorer .\\",shell=True)

def exp_Everything(event):
    subprocess.Popen("cd Tools\BT-Tools\Everything\ & explorer .\\",shell=True)
def evtxLogparse1():
    # evtxLogparse1日志分析
    subprocess.Popen("cd Tools\BT-Log\evtxLogparse1.1\ & start.bat",shell=True)
def evtxLogparse1Browser(event=None):
    subprocess.Popen("cd Tools\BT-Log\evtxLogparse1.1 & explorer .\\",shell=True)

def javaMemshellScan():
    # Java内存马扫描
    subprocess.Popen('cd Tools\BT-Response\java-memshell-scanner-master\java-memshell-scanner-master & explorer .\\',shell=True)
def javaMemshellScanBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\java-memshell-scanner-master & explorer .\\",shell=True)

def LastActivityView():
    #LastActivityView (查看最近访问文件)
    subprocess.Popen("Tools\BT-Response\LastActivityView\LastActivityView\LastActivityView.exe",shell=True)
def LastActivityViewBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\LastActivityView & explorer .\\",shell=True)

def ProcessHacker():
    # ProcessHacker查看网络连接
    subprocess.Popen(r"Tools\BT-Tools\ProcessHacker\x64\ProcessHacker.exe",shell=True)
def ProcessHackerBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\ProcessHacker & explorer .\\",shell=True)


def Wscan():
    # wscan(web查杀)深信服
    subprocess.Popen("Tools\BT-Response\wscan\wscan.exe",shell=True)
def WscanBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\wscan & explorer .\\",shell=True)

def Sysmon():
    # Sysmon监控系统日志
    subprocess.Popen("cd Tools\BT-Log\Sysmon & start.bat",shell=True)
def SysmonBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\Sysmon & explorer .\\",shell=True)    

def GetInfo():
    # GetInfo获取系统基本信息
    subprocess.Popen("Tools\BT-Tools\win_GetInfo\GetInfo.exe",shell=True)
def GetInfoBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\win_GetInfo & explorer .\\",shell=True)

def YDArk():
    # YDArk系统驱动查看
    subprocess.Popen("Tools\BT-Response\YDArk_v1.0.2.5_Signed\YDArk_v1.0.2.5_Signed.exe",shell=True)
def YDArkBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\YDArk_v1.0.2.5_Signed & explorer .\\",shell=True)

def huorongjian():
    # 火绒剑
    subprocess.Popen("Tools\BT-Response\HRSword\HRSword.exe",shell=True)
def huorongjianBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\HRSword & explorer .\\",shell=True)

def portexpert():
    # 端口专家
    subprocess.Popen("Tools\BT-Response\portexpert\portexpert.exe",shell=True)
def portexpertBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\portexpert & explorer .\\",shell=True)

def HeMaWebShellChaSha():
    # 河马webshell查杀
    subprocess.Popen("Tools\BT-Response\HeMawebShell\qhm.exe",shell=True)
def HeMaWebShellChaShaBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\HeMawebShell & explorer .\\",shell=True)

def JieMi():
    # 超级解密工具
    subprocess.Popen("cd Tools\BT-Analysis\JiaMi & CTF-Tools.exe",shell=True)
def JieMiBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Analysis\JiaMi & explorer .\\",shell=True)

def DangerPort():
    # 端口分析大师
    subprocess.Popen("Tools\BT-Response\DangerPort\DangerPort.exe",shell=True)
def DangerPortBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\DangerPort & explorer .\\",shell=True)

def hash():
    # 哈希计算器
    subprocess.Popen("Tools\BT-Tools\hash\Hash.exe",shell=True)
def hashBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\hash & explorer .\\",shell=True)

def dumpClass():
    # DumpClass
    subprocess.Popen('cd Tools\BT-Log\dumpclass & explorer .\\',shell=True)
def dumpClassBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\dumpclass & explorer .\\",shell=True)


def Csnas():
    # Csnas科来网络分析系统
    subprocess.Popen("Tools\BT-Analysis\csnas_tech\科来网络分析.exe",shell=True)
def CsnasBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Analysis\csnas_tech & explorer .\\",shell=True)

def cmd():
    # Name
    subprocess.Popen("start cmd.exe",shell=True)
def BTTools2():
    # BTTools2蓝队工具箱2
    subprocess.Popen(r"cd Tools\BT-Analysis\BTtools2 && ..\..\..\Java_path\Java_8_win\bin\java.exe -jar BlueTeamTools0.85.jar",shell=True)
def BTTools2Browser(event=None):
    subprocess.Popen("cd Tools\BT-Analysis\BTtools2 & explorer .\\",shell=True)

def winhex():
    # WinHex
    subprocess.Popen("Tools\BT-Tools\winhex\WinHex.exe",shell=True)
def winhexBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\winhex & explorer .\\",shell=True)
def windows1check():
    # Windows日志一件分析
    subprocess.Popen("cd Tools\BT-Log\windows1check && windowslog.exe",shell=True)
def windows1checkBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\windows1check & explorer .\\",shell=True)

def wakuang():
    # annamineWanncry挖矿专杀
    subprocess.Popen(r"cd Tools\BT-Response\wannamineWanncryPowershell & start.bat",shell=True)
def wakuangBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\wannamineWanncryPowershell & explorer .\\",shell=True)

def silu():
    # 蓝队思路图
    subprocess.Popen(r"cd Tools\BT-Tools\silu & start.bat",shell=True)
def Wireshark():
    # Wireshark
    subprocess.Popen(r"cd Tools\BT-Analysis\Wireshark && WiresharkPortable64.exe",shell=True)
def WiresharkBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Analysis\Wireshark & explorer .\\",shell=True)

def silu2():
    # Lin/Win排查指令
    subprocess.Popen(r"cd Tools\BT-Tools\silu & start2.bat",shell=True)
def Baolumian():
    subprocess.Popen(r"cd Tools\BT-Tools\baolu & start.bat",shell=True)
def Seay():
    # Seay代码审计
    subprocess.Popen("Tools\BT-Tools\Seay\Seay.exe",shell=True)
def SeayBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\Seay & explorer .\\",shell=True)

def notapad():
    # NotePad++
    subprocess.Popen(r"Tools\BT-Tools\notepad++\notepad++.exe",shell=True)
def notepadBrower(event=None):
    subprocess.Popen("cd Tools\BT-Tools\notepad++ & explorer .\\",shell=True)

def Fiddler():
    # Fiddler抓包
    subprocess.Popen(r"Tools\BT-Analysis\fiddler\Fiddler.exe",shell=True)
def FiddlerBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Analysis\fiddler & explorer .\\",shell=True)

def Burp():
    # Burp精简版
    subprocess.Popen(r"Java_path\Java_8_win\bin\java.exe -jar Tools\BT-Log\BurpSuitev\BurpLoader.jar ",shell=True)
def BurpBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\BurpSuitev & explorer .\\",shell=True)

def ASCII():
    # Ascll及进制转换工具
    subprocess.Popen(r"Tools\BT-Tools\Ascll\turns4.exe",shell=True)
def ASCIIBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\Ascll & explorer .\\",shell=True)

def erweima():
    # 二维码解析工具
    subprocess.Popen("Tools\BT-Tools\erweima\erweima.exe",shell=True)
def erweimaBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\erweima & explorer .\\",shell=True)

def yuancheng():
    # MobaXterm万能远程连接工具
    subprocess.Popen(r"Tools\BT-Tools\yuancheng\MobaXterm1_CHS1.exe",shell=True)
def yuanchengBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\yuancheng & explorer .\\",shell=True)
def ApkIDE():
    # ApkIDE逆向工具
    subprocess.Popen(r"Tools\BT-Reverse\ApkIDE\ApkIDE.exe",shell=True)
def ApkIDEBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\ApkIDE & explorer .\\",shell=True)

def java_re():
    # java反编译工具
    subprocess.Popen("Tools\BT-Reverse\java_re\XJad.exe",shell=True)
def java_reBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\java_re & explorer .\\",shell=True)
def ILSPY():
    # ILSPY反编译工具
    subprocess.Popen("Tools\BT-Reverse\IL Spy_2.3.0.0_CHS_MOD\ILSpy.exe",shell=True)
def ILSPYBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\IL Spy_2.3.0.0_CHS_MOD & explorer .\\",shell=True)
def jd_gui():
    # jd-gui工具
    subprocess.Popen("Tools\BT-Reverse\jd-gui-0.3.3.windows\jd-gui.exe",shell=True)
def jd_guiBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\jd-gui-0.3.3.windows & explorer .\\",shell=True)

def PEiD():
    # PEiD查壳脱壳工具
    subprocess.Popen("Tools\BT-Reverse\PEiD 0.94\PEiD_原始.exe",shell=True)
def PEiDBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\PEiD 0.94 & explorer .\\",shell=True)

def OD():
    # OD
    subprocess.Popen(r"Tools\BT-Reverse\Ollydbg\吾爱破解[LCG].exe",shell=True)
def ODBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Reverse\Ollydbg & explorer .\\",shell=True)

def UPdumpclass():
    # dumpclass
    subprocess.Popen('cd Tools\BT-upload\dumpclass\ & explorer .\\',shell=True)
def UPdumpclassBrower(event=None):
    subprocess.Popen("cd Tools\BT-upload\dumpclass & explorer .\\",shell=True)

def UPhuorongjian():
    # 火绒剑安装包
    subprocess.Popen('cd Tools\BT-upload\huorong\ & explorer .\\',shell=True)

def UPLinuxCheck():
    # Linux应急小脚本
    subprocess.Popen('cd Tools\BT-upload\LinuxCheckScript\ & explorer .\\',shell=True)
def UPshellanalyzer():
    # shell-analyzer内存马查杀工具
    subprocess.Popen('cd Tools\BT-upload\shell-analyzer\ & explorer .\\',shell=True)
def UPSysmon():
    # Sysmon日志查看工具
    subprocess.Popen('cd Tools\BT-upload\Sysmon\ & explorer .\\',shell=True)
def UPtomcat():
    # tomcat-Java内存马扫描工具
    subprocess.Popen('cd Tools\BT-upload\omcat\ & explorer .\\',shell=True)
def UPwhohk():
    # whohkLinux应急脚本
    subprocess.Popen('cd Tools\BT-upload\whohk\ & explorer .\\',shell=True)
def UPWireshark():
    # Wireshark
    subprocess.Popen('cd Tools\BT-upload\wi\ & explorer .\\',shell=True)
def NWT():
    # 内网通
    subprocess.Popen('cd Tools\BT-Tools\wt & explorer .\\',shell=True)

def ShuaXin():
    # 自动刷新脚本
    subprocess.Popen('cd Tools\BT-Tools\shuaxin & explorer .\\',shell=True)

def IPaddersINFO():
    # ip地址批量查询
    import webbrowser
    webbrowser.open('http://www.ab173.com/gongju/ip/ipbatch.php')
def onefox():
    print("正在启动onefox")
    subprocess.Popen('cd onefox & Python38\python3.exe GUI_Tools.py',shell=True)
def SimulateFishing():
    # 模拟钓鱼工具
    subprocess.Popen(r"cd Tools\BT-Tools\Simulate-fishing & start.bat",shell=True)
def SimulateFishingBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\Simulate-fishing & explorer .\\",shell=True)
def FastTest():
    # 红队服务器探测
    subprocess.Popen(r"cd Tools\BT-Tools\fasttest & start.bat",shell=True)
def FastTestBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Tools\fasttest & explorer .\\",shell=True)

def UPhema():
    # 河马WebShell查杀
    subprocess.Popen('cd Tools\BT-Response\HeMawebShell & explorer .\\',shell=True)


def UPAutoruns():
    subprocess.Popen('cd Tools\BT-Response\Autoruns & explorer .\\',shell=True)

def UPDDun():
    subprocess.Popen('cd Tools\BT-Response\Ddun & explorer .\\',shell=True)

def UPSysmon():
    subprocess.Popen('cd Tools\BT-Log\Sysmon & explorer .\\',shell=True)
def UPod():
    subprocess.Popen('cd Tools\BT-Reverse\Ollydbg\ & explorer .\\',shell=True)
    
def docker():
    webbrowser.open('https://docs.docker.com/')
def nessus():
    webbrowser.open('https://github.com/elliot-bia/nessus/blob/main/README-cn.md')
def awvs():
    webbrowser.open('https://mp.weixin.qq.com/s/X_i-ZQcw_s910E33KdOEHA')
def nextscan():
    webbrowser.open('https://next-scan.ly.com/install/binary/')
def goby():
    webbrowser.open('https://gobysec.net/faq')
def yingjibiji():
    webbrowser.open('https://github.com/Bypass007/Emergency-Response-Notes')
def huoqilin():
    subprocess.Popen('cd Tools\BT-Response\huoqilin & explorer .\\',shell=True)
def DEyes():
    subprocess.Popen('cd Tools\BT-Response\D-Eyes & explorer .\\',shell=True)
def Hfish():
    webbrowser.open('https://hfish.net/#/2-3-windows')
def Invicti():
    webbrowser.open('https://mp.weixin.qq.com/s/o9OTPnNWYdNoO7Xrhz0aoA')
def Emergenc():
    subprocess.Popen('Tools\BT-Log\Emergency_response_tools\Emergency_response_tools.exe',shell=True)
def EmergencBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Log\Emergency_response_tools & explorer .\\",shell=True)
  
def Sandboxie():
    subprocess.Popen("Tools/BT-Response/SandBox/Sandboxie.exe",shell=True)
def SandboxieBrowser(event=None):
    subprocess.Popen("cd Tools\BT-Response\SandBox & explorer .\\",shell=True)
def LinuxCheck():
    subprocess.Popen('cd Tools\BT-Response\LinuxCheck & explorer .\\',shell=True)

def Self360():
    subprocess.Popen('cd Tools\BT-Response\Self360 & explorer .\\',shell=True)
def LinuxCheck2():
    subprocess.Popen('cd Tools\BT-Response\LinuxCheck2 & explorer .\\',shell=True)
def pythonDev():
    subprocess.Popen('cd Python38 & explorer .\\',shell=True)

def pyinstallerRE():
    # pyinstaller逆向
    
    subprocess.Popen('cd Tools\BT-Reverse\PyinstallRE & explorer .\\',shell=True)