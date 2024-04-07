import tkinter as tk
import ttkbootstrap as ttk
import config

def Text(self):
    tools = ttk.LabelFrame(self.frame_Text,text="用作临时记录笔记",
                                        bootstyle="journal")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边

    # 创建一个滚动条控件，默认为垂直方向
    whois_sbar = tk.Scrollbar(tools,
                                    background="#00FA9A",
                                    activebackground="#00FA9A",
                                    troughcolor="#363636",
                                    borderwidth=-2,
                                    activerelief='groove')
    # 将滚动条放置在右侧，并设置当窗口大小改变时滚动条会沿着垂直方向延展
    whois_sbar.pack(side=tk.RIGHT,
                            fill=tk.Y)
    # 设置文本框控件
    whois_result = ttk.Text(tools,
                                    yscrollcommand=whois_sbar.set,  # 调用滚动条
                                    undo=True)  # 开启删除内容
    # 在主窗口内显示
    whois_result.place(relwidth=0.988,
                            relheight=1.0)

    font = tk.font.Font(size=14)  # 设置字体
    whois_result.config(font=font, foreground='#68afc3')  # 颜色

    whois_sbar.config(command=whois_result.yview)  # 设置鼠标可以

    whois_result.insert(tk.END,"""笔记:
""")
# 上传应急    
def upload(self):
    tools = ttk.LabelFrame(self.frame_upload,text="将文件上传至服务器进行操作",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边
    button = tk.Button(tools, text='dumpclass工具',command=config.UPdumpclass, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    

    button = tk.Button(tools, text='火绒剑',command=config.UPhuorongjian, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置


    button = tk.Button(tools, text='Linux日志查看脚本',command=config.UPLinuxCheck, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置
    
    button = tk.Button(tools, text='shell-analyzer内存马查杀',command=config.UPshellanalyzer, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='tomcat内存马查杀工具',command=config.UPtomcat, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='whohk-Linux应急脚本',command=config.UPwhohk, width=40, height=2)
    button.grid(row=2,column=2,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='Wireshark',command=config.UPWireshark, width=40, height=2)
    button.grid(row=2,column=3,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='河马WebShell查杀工具',command=config.UPhema, width=40, height=2)
    button.grid(row=2,column=4,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='Autoruns(检查启动项服务等)',command=config.UPAutoruns, width=40, height=2)
    button.grid(row=3,column=1,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='D盾',command=config.UPDDun, width=40, height=2)
    button.grid(row=3,column=2,padx=20,pady=20) # 位置UP

    button = tk.Button(tools, text='Sysmon(监控系统日志)',command=config.UPSysmon, width=40, height=2)
    button.grid(row=3,column=3,padx=20,pady=20) # 位置UP
    
    button = tk.Button(tools, text='吾爱专用OD',command=config.UPod, width=40, height=2)
    button.grid(row=3,column=4,padx=20,pady=20) # 位置UP
    
    button = tk.Button(tools, text='火麒麟',command=config.huoqilin, width=40, height=2)
    button.grid(row=4,column=1,padx=20,pady=20) # 位置UP

    button = tk.Button(tools, text='D-Eyes 绿盟科技应急响应工具',command=config.DEyes, width=40, height=2)
    button.grid(row=4,column=2,padx=20,pady=20) # 位置UP

    button = tk.Button(tools, text='360急救箱',command=config.Self360, width=40, height=2)
    button.grid(row=4,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.Self360)

    button = tk.Button(tools, text='Linux日志检查脚本',command=config.LinuxCheck2, width=40, height=2)
    button.grid(row=4,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.LinuxCheck2)

# 工具关于
def about(self):

    tools = ttk.LabelFrame(self.frame_about,text="工具关于",
                                        bootstyle="journal")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边


    # 创建一个滚动条控件，默认为垂直方向
    whois_sbar = tk.Scrollbar(tools,
                                    background="#00FA9A",
                                    activebackground="#00FA9A",
                                    troughcolor="#363636",
                                    borderwidth=-2,
                                    activerelief='groove')
    # 将滚动条放置在右侧，并设置当窗口大小改变时滚动条会沿着垂直方向延展
    whois_sbar.pack(side=tk.RIGHT,
                            fill=tk.Y)

    # 设置文本框控件
    whois_result = ttk.Text(tools,
                                    yscrollcommand=whois_sbar.set,  # 调用滚动条
                                    undo=True)  # 开启删除内容
    # 在主窗口内显示
    whois_result.place(relwidth=0.988,
                            relheight=1.0)

    # font1 = tk.font.Font(family='微软雅黑',size=24) # 设置字体
    font = tk.font.Font(size=14)  # 设置字体
    whois_result.config(font=font, foreground='#68afc3')  # 颜色

    whois_sbar.config(command=whois_result.yview)  # 设置鼠标可以

    whois_result.insert(tk.END,"""
代码编写成员
########################################################
* ChinaRan404
* W啥都学
* 清辉
* Code_200
########################################################
致谢：
森然、我数挖槽、Song、雪娃娃、成都第一深情
                        
项目地址(持续更新):
https://github.com/ChinaRan0/BlueTeamTools                            

One-Fox工具箱联动（狐狸）
Github:https://github.com/One-Fox-Security-Team/One-Fox-T00ls

工具更新与反馈建议：
关注公众号“知攻善防实验室”回复“交流群”，在群内@群主
""")


 # 逆向工具
def reverse(self):
    tools = ttk.LabelFrame(self.frame_reverse,text="逆向分析",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边
    

    button = tk.Button(tools, text='ApkIDE',command=config.ApkIDE, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ApkIDEBrowser)
    
    button = tk.Button(tools, text='java反编译工具',command=config.java_re, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.java_reBrowser)
    
    button = tk.Button(tools, text='ILSPY',command=config.ILSPY, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ILSPYBrowser)
    
    button = tk.Button(tools, text='jd-gui-0.3.3',command=config.jd_gui, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.jd_guiBrowser)
    
    button = tk.Button(tools, text='PEiD',command=config.PEiD, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.PEiDBrowser)
    
    button = tk.Button(tools, text='ILSPY',command=config.ILSPY, width=40, height=2)
    button.grid(row=2,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ILSPYBrowser)
    
    button = tk.Button(tools, text='吾爱破解专用版Ollydbg',command=config.OD, width=40, height=2)
    button.grid(row=2,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ODBrowser)

    button = tk.Button(tools, text='Pyinstaller逆向工具',command=config.pyinstallerRE, width=40, height=2)
    button.grid(row=2,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.pyinstallerRE)

    
# 日志分析
def Log_analysis(self):

    tools = ttk.LabelFrame(self.frame_Log_analysis,text="日志分析",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边

    button = tk.Button(tools, text='BrowsingHistoryView浏览器记录查看工具',command=config.BrowsingHistoryView, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.BrowsingHistoryViewBrowser)



    button = tk.Button(tools, text='evtxLogparse1日志分析',command=config.evtxLogparse1, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.evtxLogparse1Browser)
    button = tk.Button(tools, text='Sysmon监控系统日志',command=config.Sysmon, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.SysmonBrowser)
    button = tk.Button(tools, text='dumpclass',command=config.dumpClass, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.dumpClassBrowser)
    button = tk.Button(tools, text='Windows日志一键分析',command=config.windows1check, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.windows1checkBrowser)
    button = tk.Button(tools, text='Burp精简版',command=config.Burp, width=40, height=2)
    button.grid(row=2,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.BurpBrowser)
    button = tk.Button(tools, text='EmergencyWindows日志分析工具',command=config.Emergenc, width=40, height=2)
    button.grid(row=2,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.EmergencBrowser)
    
   
# 应急响应
def Response(self):

    tools = ttk.LabelFrame(self.frame_Response,text="应急响应",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边

    button = tk.Button(tools, text='Autoruns(查启动项服务等)',command=config.Autoruns, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.AutorunsBrowser)


    button = tk.Button(tools, text='D盾',command=config.Ddun, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.DdunBrowser)

    button = tk.Button(tools, text='Java内存马扫描工具',command=config.javaMemshellScan, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.javaMemshellScanBrowser)

    button = tk.Button(tools, text='LastActivityView近期访问文件',command=config.LastActivityView, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.LastActivityViewBrowser)

    button = tk.Button(tools, text='YDArk系统驱动查看',command=config.YDArk, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.YDArkBrowser)

    button = tk.Button(tools, text='火绒剑',command=config.huorongjian, width=40, height=2)
    button.grid(row=2,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.huorongjianBrowser)

    button = tk.Button(tools, text='端口专家',command=config.portexpert, width=40, height=2)
    button.grid(row=2,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.portexpertBrowser)

    button = tk.Button(tools, text='河马WebShell查杀',command=config.HeMaWebShellChaSha, width=40, height=2)
    button.grid(row=2,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.HeMaWebShellChaShaBrowser)

    button = tk.Button(tools, text='深信服WebShell查杀工具',command=config.Wscan, width=40, height=2)
    button.grid(row=3,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.WscanBrowser)


    button = tk.Button(tools, text='annamineWanncry挖矿专杀',command=config.wakuang, width=40, height=2)
    button.grid(row=3,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.wakuangBrowser)
    
    button = tk.Button(tools, text='Sandbox沙盒',command=config.Sandboxie, width=40, height=2)
    button.grid(row=3,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.SandboxieBrowser)
    
    button = tk.Button(tools, text='360急救箱',command=config.Self360, width=40, height=2)
    button.grid(row=3,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.Self360)

    button = tk.Button(tools, text='Linux日志检查脚本',command=config.LinuxCheck2, width=40, height=2)
    button.grid(row=4,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.LinuxCheck2)

    
# 常用工具
def in_common_use(self):
    tools = ttk.LabelFrame(self.frame_in_common_use,text="常用工具",
                                        bootstyle="journal")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边


    button = tk.Button(tools, text='cmd',command=config.cmd, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='Everything',command=config.Everything,width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20)
    button.bind('<Double-3>',config.EverythingBrowser)


    button = tk.Button(tools, text='ProcessHacker查看网络连接',command=config.ProcessHacker,width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置\
    button.bind('<Double-3>',config.ProcessHackerBrowser)

    button = tk.Button(tools, text='GetInfo获取系统基本信息',command=config.GetInfo, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.GetInfoBrowser)
    

    button = tk.Button(tools, text='哈希计算器',command=config.hash, width=40, height=2)
    button.grid(row=2,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.hashBrowser)

    button = tk.Button(tools, text='WinHex',command=config.winhex, width=40, height=2)
    button.grid(row=2,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.winhexBrowser)

    button = tk.Button(tools, text='Seay代码审计工具',command=config.Seay, width=40, height=2)
    button.grid(row=3,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.SeayBrowser)

    button = tk.Button(tools, text='Notepad++',command=config.notapad, width=40, height=2)
    button.grid(row=3,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.notepadBrower)

    button = tk.Button(tools, text='Ascll及进制转换工具',command=config.ASCII, width=40, height=2)
    button.grid(row=3,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ASCIIBrowser)
    
    button = tk.Button(tools, text='二维码解析工具',command=config.erweima, width=40, height=2)
    button.grid(row=3,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.erweimaBrowser)
    
    button = tk.Button(tools, text='MobaXterm万能远程连接工具(密码:qaz1230.)',command=config.yuancheng, width=40, height=2)
    button.grid(row=4,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.yuanchengBrowser)

    button = tk.Button(tools, text='内网通安装包(用于内网通信)',command=config.NWT, width=40, height=2)
    button.grid(row=4,column=2,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='自动刷新脚本',command=config.ShuaXin, width=40, height=2)
    button.grid(row=4,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.ShuaXin)

    button = tk.Button(tools, text='IP地址批量查询',command=config.IPaddersINFO, width=40, height=2)
    button.grid(row=4,column=4,padx=20,pady=20) # 位置
    
    
    button = tk.Button(tools, text='模拟exe钓鱼工具',command=config.SimulateFishing, width=40, height=2)
    button.grid(row=5,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.SimulateFishingBrowser)

    button = tk.Button(tools, text='红队服务器探测',command=config.FastTest, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.FastTestBrowser)
    
    button = tk.Button(tools, text='Burp精简版',command=config.Burp, width=40, height=2)
    button.grid(row=2,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.BurpBrowser)
    

# 流量分析
def flow_analysis(self):

    tools = ttk.LabelFrame(self.frame_flow_analysis,text="流量分析",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边

    button = tk.Button(tools, text='超级解密工具',command=config.JieMi, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.JieMiBrowser)
    
    button = tk.Button(tools, text='蓝队分析辅助包',command=config.BTTools2, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.BTTools2Browser)

    button = tk.Button(tools, text='科来网络分析系统(安装包)',command=config.Csnas, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.CsnasBrowser)

    button = tk.Button(tools, text='Fiddler汉化版',command=config.Fiddler, width=40, height=2)
    button.grid(row=2,column=1,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.FiddlerBrowser)

    button = tk.Button(tools, text='Wireshark',command=config.Wireshark, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置
    button.bind('<Double-3>',config.WiresharkBrowser)

def IdeaMap(self):

    tools = ttk.LabelFrame(self.frame_IdeaMap,text="蓝队思路图",
                                        bootstyle="dark")

    tools.place(relx = 0,  # 左边
                    rely=0,# 上边
                    relwidth=1, # 右边
                    relheight=1) # 下边

    button = tk.Button(tools, text='溯源反制思路图',command=config.silu, width=40, height=2)
    button.grid(row=1,column=1,padx=20,pady=20) # 位置
    
    button = tk.Button(tools, text='Win/Lin排查思维导图',command=config.silu2, width=40, height=2)
    button.grid(row=1,column=2,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='互联网暴露面思维导图',command=config.Baolumian, width=40, height=2)
    button.grid(row=1,column=3,padx=20,pady=20) # 位置

    button = tk.Button(tools, text='应急响应笔记',command=config.yingjibiji, width=40, height=2)
    button.grid(row=1,column=4,padx=20,pady=20) # 位置
