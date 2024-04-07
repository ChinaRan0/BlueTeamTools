# -*- coding:utf-8 -*-
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image,ImageTk
import config
from tkinter import messagebox
import webbrowser
import threading  # 预防卡住
from PIL.ImageTk import PhotoImage
import atexit
import os
import requests
import time
from Code.CryptoEnCode import *
from UiShow.main import *
from ShowCode.main import *

def show_popup(event):
    popup = tk.Toplevel(root)
    popup.title("输入密码")
    
    entry_label = tk.Label(popup, text="emhpZ29uZ3NoYW5mYW5n")
    entry_label.pack()
    
    entry = tk.Entry(popup, show="*")
    entry.pack()
    
    def check_password():
        password = entry.get()
        
        # 在这里添加密码验证逻辑
        if password == "zhigongshanfang":
            
            print("密码正确")
            config.DaoMuBiJi()
            pass
        else:
            # 密码错误的提示
            pass
    
    confirm_button = tk.Button(popup, text="确认", command=check_password)
    confirm_button.pack()

def show_splash_screen(root, duration):
    # 创建启动动画窗口
    splash_root = tk.Toplevel(root)
    splash_root.overrideredirect(True)  # 窗口无边框

    # 启动窗口设计参数
    splash_screen_width = 300  # 启动窗口的宽度
    splash_screen_height = 200  # 启动窗口的高度
    position_right = int((screen_width - splash_screen_width) / 2)
    position_down = int((screen_height - splash_screen_height) / 2)

    # 设置窗口位置和大小
    splash_root.geometry(f"{splash_screen_width}x{splash_screen_height}+{position_right}+{position_down}")

    # 设定背景和前景颜色
    bg_color = '#0D1B2A'  # 深蓝色背景
    fg_color = '#1B9AAA'  # 科技感青色前景
    splash_root.configure(background=bg_color)

    # 在启动窗口中显示文本
    splash_label = tk.Label(splash_root, text="Attack&Defend", font=("Consolas", 20, "bold"), bg=bg_color, fg=fg_color)
    splash_label.pack(expand=True)
    
    # 添加一个进度条
    progress = ttk.Progressbar(splash_root, orient='horizontal', length=splash_screen_width, mode='determinate')
    progress.pack(side='bottom')
    
    # 用于模拟加载进度的简单动画效果
    def simulate_loading():
        for value in range(0, 101, 10):  # 从0%加载到100%
            progress['value'] = value
            splash_root.update_idletasks()  # 更新UI
            time.sleep(0.1)  # 等待一小段时间

    splash_root.after(0, simulate_loading)
    
    # 经过duration时间后销毁启动窗口并显示主窗口
    root.after(duration, splash_root.destroy)


def on_close():
    response=messagebox.askyesno('Exit','关闭前请确认临时笔记是否还有未处理内容')
    if response:
        root.destroy()
class interface:
    def update(self):
        print("开始检查更新")
        try:
            res  = requests.get("https://gitee.com/China6618NetworkTeam/blue-team-tools/raw/master/update",timeout=5)
            if int(res.text) == 11:
                messagebox.showinfo("信息",f"您已是最新版本!\nversion : v{res.text}")
            else:
                messagebox.showinfo("信息",f"您的工具箱不是最新版本,最新版本为v{res.text},您的版本v11,即将打开发布页面.")
                webbrowser.open('https://github.com/ChinaRan0/BlueTeamTools')

        except:
            messagebox.showinfo("信息",f"未知错误，请联系微信Admin_Ran")
    # 打开浏览器
    def threading_browser(self):
        # 默认浏览器打开指定地址
        webbrowser.open('http://www.zhigongshanfang.top')
    def YijianWeiXing(self):
        # 默认浏览器打开指定地址
        messagebox.showinfo("提示",f"卫星连接成功！！")


    def HVVinfo(self):
        # 默认浏览器打开指定地址
        webbrowser.open('http://hvv.zhigongshanfang.top')
    def RTtools(self):
        # 获取当前工作目录
        current_directory = os.getcwd()

        # 要检查的文件夹名称
        folder_name = "onefox"

        # 构建文件夹的完整路径
        folder_path = os.path.join(current_directory, folder_name)

        # 检查文件夹是否存在
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print(f"目录 '{folder_name}' 存在.")
            config.onefox()
        else:
            messagebox.showinfo("提示", "未获取到联动文件，请关注公众号'知攻善防实验室'回复'蓝队工具箱'获取教程。")
            print(f"目录 '{folder_name}' 不存在.")
    def Open_browser(self):
        current_path = os.getcwd()
        if os.name == 'nt':
            os.startfile(current_path)
    def browser(self):
        # 定义线程 预防卡
        t = threading.Thread(target=self.threading_browser)
        # 启动线程
        t.start()

        # 公众号
    def threading_gzh(self):
        img = Image.open('images\gongzhonghao.png')
        img.show()

    def Gzh(self):
        # 定义线程 预防卡
        t = threading.Thread(target=self.threading_gzh)
        # 启动线程
        t.start()

    def Invoke_Output(self):
        self.whois_top = tk.Tk()
        self.whois_top.geometry('600x600')
        # 给主窗口起一个名字，也就是窗口的名字
        self.whois_top.title('免责声明')
        # whois_top.config(background="#2F4F4F")

        # 创建一个滚动条控件，默认为垂直方向
        self.whois_sbar = tk.Scrollbar(self.whois_top,
                                  background="#00FA9A",
                                  activebackground="#00FA9A",
                                  troughcolor="#363636",
                                  borderwidth=-2,
                                  activerelief='groove')
        # 将滚动条放置在右侧，并设置当窗口大小改变时滚动条会沿着垂直方向延展
        self.whois_sbar.pack(side=tk.RIGHT,
                        fill=tk.Y)

        # 设置文本框控件
        self.whois_result = ttk.Text(self.whois_top,
                                yscrollcommand=self.whois_sbar.set,  # 调用滚动条
                                undo=True,)  # 开启删除内容
        # 在主窗口内显示
        self.whois_result.place(relwidth=0.988,
                           relheight=1.0)

        #font1 = tk.font.Font(family='微软雅黑',size=24) # 设置字体
        font = tk.font.Font(family='微软雅黑',size=60)# 设置字体
        self.whois_result.config(font=font, foreground='#68afc3')  # 颜色

        self.whois_sbar.config(command=self.whois_result.yview)  # 设置鼠标可以

        self.whois_result.insert(tk.END,"""尊敬的用户：
感谢您使用我们开发的安全工具。
以下是关于本工具的相关免责声明，请您仔细阅读：
风险提示：
  本产品涉及的内容较为敏感，可能存在一定的法律风险和安全风险。
  请您在使用本产品时，严格遵守相关法律法规，并确保您的行为符合相关规定。
病毒风险：
  由于互联网环境的复杂性和不确定性，且集成工具大都来源于互联网，我们无法确保本产品来源的安全性。
  若您在使用本产品时发现任何可疑行为或病毒，请您立即停止使用，并及时联系我们进行处理。
使用风险：
  使用本产品需要具备一定的技术水平和专业知识。
  若您在使用本产品时因操作不当或误操作导致的问题，我们无法承担任何责任。
数据风险：
  在使用本安全工具时，可能会涉及到用户的个人信息、商业机密等敏感数据。
  请您在使用本产品时，严格遵守相关隐私保护法规，并确保您的行为符合相关规定。
声明有效期：
  本免责声明自您使用本工具之日起生效，至您停止使用本工具之日止。
  若您在使用期间有任何疑问或需要帮助，请随时与我们联系。
再次感谢您对本团队产品的关注和支持。我们将竭诚为您提供专业、可靠的服务，祝您使用愉快！""")
    def ChangYongWangZhan(self):
        self.whois_top = tk.Tk()
        self.whois_top.geometry('600x300')
        # 给主窗口起一个名字，也就是窗口的名字
        self.whois_top.title('RT')
        # whois_top.config(background="#2F4F4F")

        # 创建一个滚动条控件，默认为垂直方向
        self.whois_sbar = tk.Scrollbar(self.whois_top,
                                  background="#00FA9A",
                                  activebackground="#00FA9A",
                                  troughcolor="#363636",
                                  borderwidth=-2,
                                  activerelief='groove')
        # 将滚动条放置在右侧，并设置当窗口大小改变时滚动条会沿着垂直方向延展
        self.whois_sbar.pack(side=tk.RIGHT,
                        fill=tk.Y)

        # 设置文本框控件
        self.whois_result = ttk.Text(self.whois_top,
                                yscrollcommand=self.whois_sbar.set,  # 调用滚动条
                                undo=True)  # 开启删除内容
        # 在主窗口内显示
        self.whois_result.place(relwidth=0.988,
                           relheight=1.0)

        #font1 = tk.font.Font(family='微软雅黑',size=24) # 设置字体
        font = tk.font.Font(family='微软雅黑',size=60)# 设置字体
        self.whois_result.config(font=font, foreground='#68afc3')  # 颜色

        self.whois_sbar.config(command=self.whois_result.yview)  # 设置鼠标可以

        self.whois_result.insert(tk.END,"""工具名称        在线网址
微步社区        https://x.threatbook.com/
奇安信威胁情报  https://ti.qianxin.com/
360威胁情报     https://ti.360.net/
安天威胁情报    https://www.antiycloud.com/
深信服威胁情报  https://wiki.sec.sangfor.com.cn/index/abroad
VirScan         https://www.virscan.org/
腾讯哈勃        https://habo.qq.com/
Jotti扫描       https://virusscan.jotti.org/
ScanVir         http://www.scanvir.com/
IP138           https://www.ip138.com/
IP反查域名      https://dns.aizhan.com/
VirusTotal      https://www.virustotal.com/gui/
网站注册查询     https://www.reg007.com/
SSL公钥解析     http://www.hiencode.com/pub_asys.html
站长工具        https://www.chinaz.com/
""")
    def XiangMu(self):
        self.whois_top = tk.Tk()
        self.whois_top.geometry('600x150')
        # 给主窗口起一个名字，也就是窗口的名字
        self.whois_top.title('项目内推')
        # whois_top.config(background="#2F4F4F")

        # 创建一个滚动条控件，默认为垂直方向
        self.whois_sbar = tk.Scrollbar(self.whois_top,
                                  background="#00FA9A",
                                  activebackground="#00FA9A",
                                  troughcolor="#363636",
                                  borderwidth=-2,
                                  activerelief='groove')
        # 将滚动条放置在右侧，并设置当窗口大小改变时滚动条会沿着垂直方向延展
        self.whois_sbar.pack(side=tk.RIGHT,
                        fill=tk.Y)

        # 设置文本框控件
        self.whois_result = ttk.Text(self.whois_top,
                                yscrollcommand=self.whois_sbar.set,  # 调用滚动条
                                undo=True)  # 开启删除内容
        # 在主窗口内显示
        self.whois_result.place(relwidth=0.988,
                           relheight=1.0)

        #font1 = tk.font.Font(family='微软雅黑',size=24) # 设置字体
        font = tk.font.Font(family='微软雅黑',size=60)# 设置字体
        self.whois_result.config(font=font, foreground='#68afc3')  # 颜色

        self.whois_sbar.config(command=self.whois_result.yview)  # 设置鼠标可以

        self.whois_result.insert(tk.END,"""尊敬的用户：
我是知攻善防实验室的ChinaRan404
如果你也因手头无项目或现有项目薪资过低
可加入我们团队交流群，群内不定时推送项目
包括但不限于:
网络攻防、CTF代打、CTF培训、驻场工程师等等。
可关注公众号“知攻善防实验室”发送“交流群”获取进群链接
""")

    def markdown(self):
        tools = ttk.LabelFrame(self.frame_markdown,text="安装文档",
                                            bootstyle="dark")

        tools.place(relx = 0,  # 左边
                        rely=0,# 上边
                        relwidth=1, # 右边
                        relheight=1) # 下边
        button = tk.Button(tools, text='Docker安装文档(在线)',command=config.docker, width=40, height=2)
        button.grid(row=1,column=1,padx=20,pady=20) # 位置UP
        
        button = tk.Button(tools, text='Nessus漏扫',command=config.nessus, width=40, height=2)
        button.grid(row=1,column=2,padx=20,pady=20) # 位置UP
        
        button = tk.Button(tools, text='AWVS漏扫',command=config.awvs, width=40, height=2)
        button.grid(row=1,column=3,padx=20,pady=20) # 位置UP
        
        button = tk.Button(tools, text='NextScan漏扫',command=config.nextscan, width=40, height=2)
        button.grid(row=1,column=4,padx=20,pady=20) # 位置UP
        
        button = tk.Button(tools, text='Goby资产识别(不建议漏扫)',command=config.goby, width=40, height=2)
        button.grid(row=2,column=1,padx=20,pady=20) # 位置UP

        button = tk.Button(tools,text='Hfish(蜜罐搭建)',width=40,height=2)
        button.config(command=config.Hfish)
        button.bind("<Button-3>", show_popup)  # 绑定鼠标右键单击事件
        button.grid(row=2,column=2,padx=20,pady=20)

        button = tk.Button(tools, text='Invicti (漏洞扫描)',command=config.goby, width=40, height=2)
        button.grid(row=2,column=3,padx=20,pady=20) # 位置UP

    def main(self):

        self.frame_in_common_use = ttk.Frame()
        self.frame_flow_analysis = ttk.Frame()
        self.frame_Response = ttk.Frame()
        self.frame_Log_analysis = ttk.Frame()
        self.frame_about = ttk.Frame()
        # self.frame_about2 = ttk.Frame()
        self.frame_Text = ttk.Frame()
        self.frame_reverse = ttk.Frame()
        self.frame_upload = ttk.Frame()
        self.frame_IdeaMap = ttk.Frame()
        self.frame_markdown = ttk.Frame()

        notebook.add(self.frame_in_common_use, text='       常用工具       ',compound='left')
        notebook.add(self.frame_flow_analysis, text='       流量分析       ',compound='left')
        notebook.add(self.frame_Response, text='       应急响应       ',compound='left')
        notebook.add(self.frame_Log_analysis, text='       日志分析       ',compound='left')
        notebook.add(self.frame_reverse, text='       逆向分析       ',compound='left')
        notebook.add(self.frame_upload, text='       上传应急       ',compound='left')
        notebook.add(self.frame_IdeaMap, text='       蓝队思路图       ',compound='left')
        notebook.add(self.frame_markdown, text='       安装文档       ',compound='left')
        # notebook.add(self.frame_about2, text='在线工具',image=frame_img,compound='left')
        notebook.add(self.frame_about, text='工具关于',compound='left')
        notebook.add(self.frame_Text, text='临时笔记',compound='left')
        
        
        

        notebook.pack(padx=2, pady=0, fill=ttk.BOTH, expand=True)

        # 设置默认选项卡为第一个选项卡
        notebook.select(self.frame_in_common_use)
        in_common_use(self)
        flow_analysis(self)
        Response(self)
        Log_analysis(self)
        reverse(self)
        about(self)
        upload(self)
        Text(self)
        IdeaMap(self)
        self.markdown()
        main_menu = ttk.Menu(root)

        Switch = ttk.Menu(main_menu)

        # 在主目录菜单上新增"文件"选项，并通过menu参数与下拉菜单绑定
        main_menu.add_cascade(label="公众号官网",command=self.browser)

        # 在主目录菜单上新增"文件"选项，并通过menu参数与下拉菜单绑定
        main_menu.add_command(label="团队公众号",command=self.Gzh)
        main_menu.add_command(label="免责声明",command=self.Invoke_Output)
        main_menu.add_command(label="项目内推",command=self.XiangMu)
        main_menu.add_command(label="蓝队常用网站",command=self.ChangYongWangZhan)
        main_menu.add_command(label="HVV情报",command=self.HVVinfo)
        main_menu.add_command(label="一键日卫星",command=self.YijianWeiXing)
        crypto_tools_menu = tk.Menu(main_menu, tearoff=0)  # 设置tearoff=0以防止菜单被分离
        crypto_tools_menu.add_command(label="玛卡巴卡", command=MaKaBaKaTools)
        crypto_tools_menu.add_command(label="Base64", command=Base64Tools)
        crypto_tools_menu.add_command(label="URL", command=Urlcode)
        crypto_tools_menu.add_command(label="持续更新中", command=MaKaBaKaTools)

        main_menu.add_cascade(label="编码工具", menu=crypto_tools_menu)

        main_menu.add_command(label="检查更新",command=self.update)


        main_menu.add_command(label="工具箱目录",command=self.Open_browser)
        main_menu.add_command(label="     OneFox红队工具箱     ",command=self.RTtools)


        # 显示菜单
        root.config(menu=main_menu)


if __name__ == '__main__':
    # 检测是否第一次打开如果是，跳转使用手册
    f = open("images/config.ini","r")
    ff = f.read().splitlines()
    f.close
    if ff[0] =='0':
        print("第一次打开")
        webbrowser.open("https://www.yuque.com/chinaran404/fxdg0c/exmghg8gb8ysmg66?singleDoc#%20%E3%80%8A%E5%BA%94%E6%80%A5%E5%93%8D%E5%BA%94%E5%B7%A5%E5%85%B7%E7%AE%B1%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B%E3%80%8B")
        f = open("images/config.ini","w")
        f.write("1")
        f.close()
    # 创建主窗口
    root = tk.Tk()
    root.withdraw()  # 先隐藏主窗口

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 显示启动动画，持续2000毫秒即2秒
    show_splash_screen(root, 2000)

    # 启动动画结束后，配置并显示主窗口
    root.after(2000, root.deiconify)  # 在启动动画后显示主窗口

    # 配置主窗口
    window_width = int(screen_width * 0.767)
    window_height = int(screen_height * 0.60)
    position_right = int((screen_width - window_width) / 2)
    position_down = int((screen_height - window_height) / 2)

    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    root.resizable(True, True)
    # 添加程序的ico
    icon = PhotoImage(file=f"images/bg.jpg")
    root.tk.call('wm', 'iconphoto', root._w, icon)

    root.title('知攻善防实验室 - 应急响应工具箱-2024.v4    微信公众号:知攻善防实验室   By:ChinaRan404')
    notebook = ttk.Notebook(root, bootstyle="selectfg")
    
    # 创建对象
    interface = interface()
    photo = Image.open(f"images/bg.jpg")  # 括号里为需要显示在图形化界面里的图片
    photo = photo.resize((34, 34))  # 规定图片大小
    img = ImageTk.PhotoImage(photo)

    interface.main()
    root.protocol('WM_DELETE_WINDOW',on_close)
    root.mainloop()