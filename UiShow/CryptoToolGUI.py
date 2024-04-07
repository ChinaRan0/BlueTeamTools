import tkinter as tk
import ttkbootstrap as ttk

class CryptoToolGUI:
    def __init__(self, title, encode_func, decode_func):
        self.encode_func = encode_func
        self.decode_func = decode_func

        window = tk.Tk()
        window.title(title)
        window.geometry('900x400')
        window.configure(bg='#333333')

        label = tk.Label(window, text="请输入明文或密文，点击按钮即可加密或解密",
                         font=('Helvetica', 12), bg='#333333', fg='white')
        label.pack(pady=20)

        self.e = tk.Text(window, height=2, font=('Helvetica', 12), bd=2, relief='groove')
        self.e.pack(pady=5)

        self.t = tk.Text(window, height=2, font=('Helvetica', 12), bd=2, relief='groove')
        self.t.pack(pady=5)

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), background='#4F4F4F', foreground='white')

        b1 = ttk.Button(window, text="加密", width=15, command=self.insert_point)
        b1.pack(pady=5)

        b2 = ttk.Button(window, text="解密", width=15, command=self.insert_end)
        b2.pack(pady=5)

        window.mainloop()

    def insert_point(self):
        text = self.e.get("1.0", "end").strip()
        encoded_text = self.encode_func(text)
        self.t.delete(1.0, "end")
        self.t.insert('insert', encoded_text)

    def insert_end(self):
        text = self.e.get("1.0", "end").strip()
        decoded_text = self.decode_func(text)
        self.t.delete(1.0, "end")
        self.t.insert('end', decoded_text)