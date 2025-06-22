import os
import subprocess
import customtkinter as ctk
from tkinter import Menu, TclError, StringVar, filedialog, Tk
import shutil
import json
from tkinter import messagebox
import sys
import webbrowser
import threading
import functools
import time
import requests

# Add system tray and hotkey support
try:
    import pystray
    from PIL import Image
    HAS_TRAY_SUPPORT = True
except ImportError:
    HAS_TRAY_SUPPORT = False
    
try:
    import keyboard
    HAS_KEYBOARD_SUPPORT = True
except ImportError:
    HAS_KEYBOARD_SUPPORT = False

# --- Configuration moved to tools_data.json and app_settings.json ---
# Define paths for configuration files
TOOLS_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_data.json")
APP_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.json")
TOOLS_ROOT_DIR = "tools" # Base directory for all tool categories

# Default tools configuration if tools_data.json is not found
# This defines the initial structure and example tools
DEFAULT_TOOLS_CONFIG = {
  "密码学工具": {
    "directory": "cryptography_tools",
    "tools": {
      "AES加解密": {
        "path": f"{TOOLS_ROOT_DIR}/cryptography_tools/aes/aes.exe",
        "desc": "AES加解密工具，支持多种模式和填充方式。"
      },
      "RSA加解密": {
        "path": f"{TOOLS_ROOT_DIR}/cryptography_tools/rsa/rsa.exe",
        "desc": "RSA加解密工具，支持大素数生成和签名验证。"
      }
    }
  },
  "编码解码工具": {
    "directory": "encoding_decoding_tools",
    "tools": {
      "Base64编解码": {
        "path": f"{TOOLS_ROOT_DIR}/encoding_decoding_tools/base64/base64.py",
        "desc": "Base64编码解码工具，支持文件和文本操作。"
      },
      "URL编解码": {
        "path": f"{TOOLS_ROOT_DIR}/encoding_decoding_tools/url/url_codec.html",
        "desc": "URL编码解码在线工具。"
      }
    }
  },
  "流量分析工具": {
    "directory": "traffic_analysis_tools",
    "tools": {
      "Wireshark": {
        "path": f"{TOOLS_ROOT_DIR}/traffic_analysis_tools/wireshark/Wireshark.exe",
        "desc": "著名的网络协议分析器。"
      }
    }
  },
  "逆向工程工具": {
    "directory": "reverse_engineering_tools",
    "tools": {
      "IDA Pro": {
        "path": f"{TOOLS_ROOT_DIR}/reverse_engineering_tools/ida_pro/idag.exe",
        "desc": "交互式反汇编器和调试器。"
      }
    }
  },
  "漏洞利用工具": {
    "directory": "exploit_tools",
    "tools": {
      "Metasploit": {
        "path": f"{TOOLS_ROOT_DIR}/exploit_tools/metasploit/msfconsole.bat",
        "desc": "流行的渗透测试框架。"
      }
    }
  },
  "杂项工具": {
    "directory": "misc_tools",
    "tools": {
      "Hash计算器": {
        "path": f"{TOOLS_ROOT_DIR}/misc_tools/hash_calculator/hash.py",
        "desc": "各种哈希算法计算工具。"
      }
    }
  }
}

# Ensure tools_data.json exists or create it with default config
# Also ensures initial tool directories and dummy files exist
if not os.path.exists(TOOLS_DATA_FILE):
    try:
        os.makedirs(TOOLS_ROOT_DIR, exist_ok=True)
        for category_name, category_info in DEFAULT_TOOLS_CONFIG.items():
            category_path_full = os.path.join(os.path.dirname(os.path.abspath(__file__)), TOOLS_ROOT_DIR, category_info["directory"])
            os.makedirs(category_path_full, exist_ok=True)
            for tool_name, tool_info in category_info["tools"].items():
                tool_dir_full = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)), tool_info["path"]))
                os.makedirs(tool_dir_full, exist_ok=True)
                # Create dummy files for demonstration if they don't exist
                dummy_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), tool_info["path"])
                if not os.path.exists(dummy_file_path):
                    with open(dummy_file_path, 'w', encoding='utf-8') as f:
                        f.write(f"This is a dummy file for '{tool_name}' in '{category_name}' category.\n")
                        f.write(f"Executable type: {os.path.splitext(tool_info['path'])[1]}\n")
                        f.write(f"Description: {tool_info['desc']}")
        
        with open(TOOLS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_TOOLS_CONFIG, f, indent=2, ensure_ascii=False)
        print("Default tools_data.json created with initial structure and dummy files.")
    except Exception as e:
        print(f"Error creating default tools_data.json or directories/dummy files: {e}")
# --- End of Configuration handling ---


class ToolBox(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Store tool configuration (will be loaded from JSON)
        self.tools_config = {}
        
        # Current page category (None means all/search, etc. non-specific category interface)
        self.current_category: str | None = None
        
        # Theme mode (light/dark)
        self.theme_mode = "light"
        
        # Current theme color (user-selected accent color)
        self.theme_color = "蓝色" # Default accent color
        
        # Tray icon object
        self.tray_icon = None
        
        # Global hotkey
        self.hotkey = "ctrl+alt+t"  # Default hotkey
        # Track the hotkey currently registered with the 'keyboard' library
        self._current_registered_hotkey = None
        
        # Run in background setting
        self.background_run = False
        
        # Store python and java paths from settings
        self._python_path = None
        self._java_path = None
        self._java_path_cached = None # Cache for Java path check
        
        # Load settings and tool data
        self._load_app_settings()
        self.load_tools_config() # This also updates category buttons
        
        # Configure window
        self.title("蓝队应急响应工具箱 - 公众号：知攻善防实验室")
        self.geometry("1200x800")
        self.minsize(800, 600) # Set a minimum size
        
        # Set custom icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
            else:
                print(f"Icon file not found: {icon_path}")
        except Exception as e:
            print(f"Error setting icon: {str(e)}")
        
        # Set CustomTkinter theme mode (default color theme is applied later via _apply_saved_color)
        ctk.set_appearance_mode(self.theme_mode)
        
        # Create main layout (grid for sidebar and main content)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=10, fg_color=("gray92", "gray15")) # Lighter/darker background for sidebar
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_rowconfigure(99, weight=1) # Pushes bottom buttons down

        # Create Logo label
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="蓝队应急响应工具箱",
            font=ctk.CTkFont(size=24, weight="bold", family="Microsoft YaHei UI") # More impactful font
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create search box
        self.search_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="🔍 搜索工具...", # Add a search icon
            height=35,
            corner_radius=8
        )
        self.search_entry.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")
        self.search_entry.bind('<Return>', self.search_tools)
        
        # Create "All Tools" button
        self.all_tools_btn = ctk.CTkButton( # Store reference to update color
            self.sidebar,
            text="🏠 全部工具", # Home icon
            command=self.show_all_tools,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.all_tools_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Category buttons will be created/updated by _update_category_buttons()
        self.category_buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.category_buttons_frame.grid(row=3, column=0, padx=0, pady=0, sticky="nsew")
        self.category_buttons_frame.grid_columnconfigure(0, weight=1)
        # This frame holds category buttons, allowing flexible re-creation
        
        self.category_buttons = [] # List to hold references to category buttons
        self._update_category_buttons() # Initial creation of category buttons

        # Spacer to push bottom buttons
        self.sidebar.grid_rowconfigure(99, weight=1)
        
        # Add bottom buttons in a frame for better alignment
        bottom_buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_buttons_frame.grid(row=100, column=0, padx=20, pady=20, sticky="ew")
        bottom_buttons_frame.grid_columnconfigure((0,1,2), weight=1) # Distribute space evenly

        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            bottom_buttons_frame,
            text="🌙" if self.theme_mode == "light" else "☀️",
            command=self.toggle_theme,
            width=40,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.theme_button.grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        # Add tool button
        self.add_tool_button = ctk.CTkButton(
            bottom_buttons_frame,
            text="➕", # Plus icon
            command=self.add_tool,
            width=40,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.add_tool_button.grid(row=0, column=1, padx=(5, 5), sticky="nsew")
        
        # Settings button
        self.settings_button = ctk.CTkButton(
            bottom_buttons_frame,
            text="⚙️", # Gear icon
            command=self.open_settings,
            width=40,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.settings_button.grid(row=0, column=2, padx=(5, 0), sticky="e")
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        try:
            print("正在获取公告")
            res = requests.get(r'https://gitee.com/China6618NetworkTeam/blue-team-tools/raw/master/%E5%85%AC%E5%91%8A.txt',verify=False)
            text = res.text
        except:
            text="""
            离线公告:欢迎使用蓝队应急响应工具箱
            
            请从左侧选择工具类别，或使用搜索功能
            
            您也可以点击左下角的 ➕ 添加新工具
            
            联系我们
            微信 Admin_Ran
            公众号 知攻善防实验室
            交流群：公众号后台回复“交流群”
            欢迎推荐好用的工具给我们！""",
            pass
        # Create welcome page
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text=text,
            font=ctk.CTkFont(size=24, weight="bold", family="Microsoft YaHei UI"),
            wraplength=700,
            justify="center",
            text_color=("gray20", "gray80") # Adjust text color for contrast
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Apply saved color theme after UI initialization
        self._apply_saved_color()

    def _load_app_settings(self):
        """Loads application settings from app_settings.json."""
        try:
            if os.path.exists(APP_SETTINGS_FILE):
                with open(APP_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                if "background_run" in settings:
                    self.background_run = settings["background_run"]
                if "hotkey" in settings:
                    self.hotkey = settings["hotkey"].lower()
                if "theme_mode" in settings: # Load theme mode
                    self.theme_mode = settings["theme_mode"]
                if "theme_color" in settings:
                    self.theme_color = settings["theme_color"]
                if "python_path" in settings:
                    self._python_path = settings["python_path"]
                if "java_path" in settings:
                    self._java_path = settings["java_path"]
        except Exception as e:
            print(f"Error loading app settings: {e}")

    def save_app_settings(self):
        """Saves current application settings to app_settings.json."""
        settings = {
            "background_run": self.background_run,
            "hotkey": self.hotkey,
            "theme_mode": self.theme_mode, # Save theme mode
            "theme_color": self.theme_color,
            "python_path": self._python_path,
            "java_path": self._java_path
        }
        try:
            with open(APP_SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving app settings: {e}")

    def load_tools_config(self):
        """Loads tool configurations from tools_data.json."""
        try:
            if os.path.exists(TOOLS_DATA_FILE):
                with open(TOOLS_DATA_FILE, 'r', encoding='utf-8') as f:
                    self.tools_config = json.load(f)
            else:
                self.tools_config = DEFAULT_TOOLS_CONFIG
                self.save_tools_config() # Create the file with default content
            
            # Re-create category buttons after loading config
            if hasattr(self, 'category_buttons_frame'): # Ensure UI is initialized
                self._update_category_buttons()

        except json.JSONDecodeError as e:
            messagebox.showerror("配置错误", f"工具配置文件 (tools_data.json) 损坏，请检查或删除后重启应用。\n错误: {e}")
            self.tools_config = DEFAULT_TOOLS_CONFIG # Fallback to default
        except Exception as e:
            messagebox.showerror("加载错误", f"加载工具配置时出错: {e}")
            self.tools_config = DEFAULT_TOOLS_CONFIG # Fallback to default
        
        # Ensure 'tools' base directory exists
        os.makedirs(TOOLS_ROOT_DIR, exist_ok=True)
        # Ensure category directories exist for current config
        for category_name, category_info in self.tools_config.items():
            category_path = os.path.join(TOOLS_ROOT_DIR, category_info["directory"])
            os.makedirs(category_path, exist_ok=True)


    def save_tools_config(self):
        """Saves current tool configuration to tools_data.json."""
        try:
            with open(TOOLS_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.tools_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("保存错误", f"保存工具配置时出错: {e}")

    def _update_category_buttons(self):
        """Recreates category buttons based on current tools_config."""
        # Destroy existing buttons in the category_buttons_frame
        for widget in self.category_buttons_frame.winfo_children():
            widget.destroy()
        self.category_buttons = []

        # Create new category buttons
        row_idx = 0
        for category_name in self.tools_config.keys():
            button = ctk.CTkButton(
                self.category_buttons_frame, # Parent to the new frame
                text=f"📂 {category_name}",
                command=lambda cat=category_name: self.show_category(cat),
                height=40,
                corner_radius=8,
                font=ctk.CTkFont(size=14)
            )
            button.grid(row=row_idx, column=0, padx=20, pady=3, sticky="ew")
            self.category_buttons.append(button)
            self.create_context_menu(button, self.tools_config[category_name]["directory"])
            row_idx += 1
        
        # Reapply colors after creating new buttons
        self._apply_saved_color()

    def apply_settings(self, settings):
        """Applies settings received from the settings window."""
        print("Applying settings:", settings)
        
        # Update internal state
        if "background_run" in settings:
            self.background_run = settings["background_run"]
            
        if "hotkey" in settings:
            old_hotkey = self.hotkey
            self.hotkey = settings["hotkey"].lower()
            if self.hotkey != old_hotkey:
                self.register_hotkey() # Re-register hotkey if it changed
            
        if "theme_mode" in settings: # Allow settings to change theme_mode too
            self.theme_mode = settings["theme_mode"]
            ctk.set_appearance_mode(self.theme_mode)
            self.theme_button.configure(text="🌙" if self.theme_mode == "light" else "☀️")
            
        if "theme_color" in settings:
            self.theme_color = settings["theme_color"]
            self._apply_custom_color(self._get_color_hex(self.theme_color)) # Apply the accent color
            
        if "python_path" in settings:
            self._python_path = settings["python_path"]
            
        if "java_path" in settings:
            self._java_path = settings["java_path"]
            self._java_path_cached = None # Invalidate cached Java path, force re-check
        
        self.save_app_settings() # Save all applied settings

    def _get_color_hex(self, color_name):
        """Returns the hex code for a given color name."""
        colors = {
            "蓝色": "#3498DB", # A vibrant blue
            "红色": "#E74C3C", # A strong red
            "绿色": "#2ECC71", # A fresh green
            "紫色": "#9B59B6"  # A rich purple
        }
        return colors.get(color_name, "#3498DB") # Default to blue

    def _apply_saved_color(self):
        """Applies the saved accent color to UI elements."""
        color_hex = self._get_color_hex(self.theme_color)
        self._apply_custom_color(color_hex)

    def _apply_custom_color(self, color_hex):
        """Applies a custom color to specific UI elements."""
        try:
            hover_color = self._adjust_color(color_hex, -20) # Darken for hover

            # Apply to sidebar "All Tools" button
            self.all_tools_btn.configure(fg_color=color_hex, hover_color=hover_color)

            # Apply to category buttons
            for btn in self.category_buttons:
                btn.configure(fg_color=color_hex, hover_color=hover_color)
            
            # Apply to specific buttons (theme, add, settings)
            self.add_tool_button.configure(fg_color=color_hex, hover_color=hover_color)
            self.settings_button.configure(fg_color=color_hex, hover_color=hover_color)
            self.theme_button.configure(fg_color=color_hex, hover_color=hover_color)
            
            # Apply to tool cards' launch buttons if they exist
            # This requires iterating through currently displayed tool cards
            if hasattr(self, 'main_frame') and self.main_frame.winfo_children():
                for widget in self.main_frame.winfo_children():
                    if isinstance(widget, ctk.CTkScrollableFrame):
                        for tool_card in widget.winfo_children():
                            if isinstance(tool_card, ctk.CTkFrame):
                                for card_child in tool_card.winfo_children():
                                    if isinstance(card_child, ctk.CTkButton) and card_child.cget("text").startswith("🚀"): # Check for rocket icon
                                        card_child.configure(fg_color=color_hex, hover_color=hover_color)
                                        break

            # Apply to dialog buttons if open (best handled within dialog's own creation, but a fallback)
            for window in self.winfo_children():
                if isinstance(window, ctk.CTkToplevel):
                    for child in window.winfo_children():
                        if isinstance(child, ctk.CTkFrame):
                            for grand_child in child.winfo_children():
                                if isinstance(grand_child, ctk.CTkButton):
                                    if grand_child.cget("text") in ["确认", "取消", "确定", "保存并应用", "确认添加", "确认修改"]:
                                        grand_child.configure(fg_color=color_hex, hover_color=hover_color)
        except Exception as e:
            print(f"Error applying custom color: {e}")

    def _adjust_color(self, hex_color, amount):
        """Adjusts the brightness of a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_tray_icon(self):
        """Creates system tray icon."""
        if not HAS_TRAY_SUPPORT:
            return
        
        try:
            menu = pystray.Menu(
                pystray.MenuItem("显示主窗口", self.show_window),
                pystray.MenuItem("全部工具", self.show_all_tools),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("设置", self.open_settings),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("退出", self.quit_app)
            )
            
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.ico")
            if not os.path.exists(icon_path):
                # Fallback to a simple blue square icon if bg.ico is missing
                icon_image = Image.new('RGB', (64, 64), color = (52, 152, 219)) # Use a color from the theme
            else:
                icon_image = Image.open(icon_path)
            
            self.tray_icon = pystray.Icon("CTF工具箱", icon_image, "CTF工具箱", menu)
            
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            print("Tray icon created.")
        except Exception as e:
            print(f"Error creating tray icon: {e}")

    def register_hotkey(self):
        """Registers global hotkey."""
        if not HAS_KEYBOARD_SUPPORT:
            print("Keyboard support not available. Skipping hotkey registration.")
            return
        
        try:
            # If a hotkey was previously registered and it's different from the new one, remove it.
            if self._current_registered_hotkey and self._current_registered_hotkey != self.hotkey:
                try:
                    keyboard.remove_hotkey(self._current_registered_hotkey)
                    print(f"Removed previous hotkey: {self._current_registered_hotkey}")
                except KeyError: # Hotkey might have been removed by other means or never properly registered
                    print(f"Previous hotkey '{self._current_registered_hotkey}' not found or already removed.")
                except Exception as e:
                    print(f"Error removing previous hotkey '{self._current_registered_hotkey}': {e}")
            
            # Register the new hotkey if it's not already registered
            # keyboard.add_hotkey implicitly handles if the same hotkey is added multiple times with the same callback
            keyboard.add_hotkey(self.hotkey, self.show_window)
            self._current_registered_hotkey = self.hotkey # Store the newly registered hotkey
            print(f"Global hotkey registered: {self.hotkey}")
        except Exception as e:
            print(f"Error registering global hotkey: {e}")
            messagebox.showerror("快捷键注册失败", f"无法注册全局快捷键 '{self.hotkey}'。\n可能已被其他程序占用或权限不足。\n错误: {e}")

    def show_window(self):
        """Shows the main window."""
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        """Hides the main window."""
        self.withdraw()

    def quit_app(self):
        """Quits the application."""
        if self.tray_icon:
            self.tray_icon.stop()
        if HAS_KEYBOARD_SUPPORT and self._current_registered_hotkey: # Unhook only the hotkey we registered
            try:
                keyboard.remove_hotkey(self._current_registered_hotkey)
                print(f"Unhooked hotkey: {self._current_registered_hotkey} before exit.")
            except Exception as e:
                print(f"Error unhooking hotkey on exit: {e}")
        self.destroy()

    def on_closing(self):
        """Handles window closing event."""
        if self.tray_icon and self.background_run:
            self.hide_window()
        else:
            self.quit_app()

    def show_add_tool_dialog(self, file_path, category_hint=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("添加工具")
        dialog.geometry("550x550") # Slightly larger for better spacing
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False) # Prevent resizing

        # Apply custom colors to dialog elements
        dialog_fg_color = self.main_frame.cget("fg_color")
        dialog.configure(fg_color=dialog_fg_color)

        # File path display
        path_label = ctk.CTkLabel(dialog, text="文件路径:", font=ctk.CTkFont(weight="bold"))
        path_label.pack(padx=20, pady=(20, 5), anchor="w")
        path_display = ctk.CTkLabel(dialog, text=file_path, wraplength=490, font=ctk.CTkFont(size=12, family="Consolas"))
        path_display.pack(padx=20, pady=(0, 10), anchor="w")

        # Tool name input
        name_label = ctk.CTkLabel(dialog, text="工具名称:", font=ctk.CTkFont(weight="bold"))
        name_label.pack(padx=20, pady=(10, 5), anchor="w")
        name_entry = ctk.CTkEntry(dialog, width=490, height=35, corner_radius=8)
        name_entry.pack(padx=20, pady=(0, 10))
        name_entry.insert(0, os.path.splitext(os.path.basename(file_path))[0])

        # Tool description input
        desc_label = ctk.CTkLabel(dialog, text="工具描述:", font=ctk.CTkFont(weight="bold"))
        desc_label.pack(padx=20, pady=(10, 5), anchor="w")
        desc_entry = ctk.CTkTextbox(dialog, width=490, height=120, corner_radius=8)
        desc_entry.pack(padx=20, pady=(0, 10))
        
        # Category selection
        category_label = ctk.CTkLabel(dialog, text="选择类别:", font=ctk.CTkFont(weight="bold"))
        category_label.pack(padx=20, pady=(10, 5), anchor="w")
        
        # Get category names for the dropdown, add an option to create new
        category_names = list(self.tools_config.keys())
        category_names.sort() # Sort alphabetically
        category_names.insert(0, "新建类别...") # Option to create new category

        initial_category_value = "新建类别..."
        if category_hint and category_hint in self.tools_config:
            initial_category_value = category_hint
        elif len(self.tools_config) > 0:
            initial_category_value = list(self.tools_config.keys())[0] # Default to first existing category
            
        category_var = ctk.StringVar(value=initial_category_value)
        
        category_menu = ctk.CTkOptionMenu(
            dialog, 
            values=category_names, 
            variable=category_var,
            width=490,
            height=35,
            corner_radius=8,
            dropdown_hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20),
            button_color=self._get_color_hex(self.theme_color),
            button_hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20),
            command=lambda choice: self.prompt_new_category_name(category_var) if choice == "新建类别..." else None
        )
        category_menu.pack(padx=20, pady=(0, 20))

        def add_tool_confirmed():
            try:
                tool_name = name_entry.get().strip()
                tool_desc = desc_entry.get("1.0", "end-1c").strip()
                category = category_var.get()
                
                if not tool_name:
                    messagebox.showerror("错误", "请输入工具名称")
                    return
                if not tool_desc:
                    messagebox.showerror("错误", "请输入工具描述")
                    return
                if category == "新建类别...":
                    messagebox.showerror("错误", "请为新类别输入名称或选择一个现有类别。")
                    return

                # Ensure the category exists in the tools_config dictionary
                if category not in self.tools_config:
                    # This case should ideally be handled by prompt_new_category_name,
                    # but as a fallback, define a default directory.
                    sanitized_cat_name = category.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
                    self.tools_config[category] = {
                        "directory": os.path.join(TOOLS_ROOT_DIR, sanitized_cat_name),
                        "tools": {}
                    }
                    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.tools_config[category]["directory"]), exist_ok=True)
                    print(f"Created new category directory on the fly: {self.tools_config[category]['directory']}")


                # Create target directory for the tool
                category_dir = self.tools_config[category]["directory"]
                tool_folder_name = tool_name.lower().replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_") # Sanitize folder name
                tool_destination_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), category_dir, tool_folder_name)
                os.makedirs(tool_destination_dir, exist_ok=True)
                
                # Copy file
                target_file_name = os.path.basename(file_path)
                target_file_full_path = os.path.join(tool_destination_dir, target_file_name)
                
                if os.path.exists(target_file_full_path):
                     overwrite_response = messagebox.askyesno("文件已存在", f"文件 '{target_file_name}' 已存在于目标目录。是否覆盖？")
                     if not overwrite_response:
                         messagebox.showinfo("取消", "已取消文件复制。")
                         return

                shutil.copy2(file_path, target_file_full_path)
                print(f"File copied to: {target_file_full_path}")

                # Calculate relative path for config
                base_path_for_rel = os.path.dirname(os.path.abspath(__file__))
                relative_path = os.path.relpath(target_file_full_path, base_path_for_rel).replace('\\', '/')

                # Add to tools_config in memory
                if tool_name in self.tools_config[category]["tools"]:
                    response = messagebox.askyesno("警告", f"工具 '{tool_name}' 已存在于 '{category}' 类别中，是否覆盖其信息？")
                    if not response:
                        return
                
                self.tools_config[category]["tools"][tool_name] = {
                    "path": relative_path,
                    "desc": tool_desc
                }
                
                # Save updated config
                self.save_tools_config()
                
                messagebox.showinfo("成功", f"工具 '{tool_name}' 添加成功！")
                dialog.destroy()
                
                # Refresh UI (category buttons and tool display)
                self.after(100, lambda: self._force_refresh_after_add(category))
                
            except Exception as e:
                error_msg = f"添加工具时出错: {str(e)}"
                print(error_msg)
                import traceback
                traceback.print_exc()
                messagebox.showerror("错误", error_msg)

        # Create button container frame
        button_container = ctk.CTkFrame(dialog, fg_color="transparent")
        button_container.pack(side="bottom", fill="x", padx=20, pady=20)
        button_container.grid_columnconfigure((0, 1), weight=1)

        cancel_btn = ctk.CTkButton(
            button_container, 
            text="取消", 
            command=dialog.destroy,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=("gray70", "gray30"), # Muted color for cancel
            hover_color=("gray60", "gray40")
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        confirm_btn = ctk.CTkButton(
            button_container, 
            text="确认添加", 
            command=add_tool_confirmed,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=self._get_color_hex(self.theme_color),
            hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20)
        )
        confirm_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def prompt_new_category_name(self, category_var):
        """Prompts user for a new category name."""
        dialog = ctk.CTkInputDialog(text="请输入新类别名称:", title="新建类别")
        new_category_name = dialog.get_input()
        
        if new_category_name:
            new_category_name = new_category_name.strip()
            if not new_category_name:
                messagebox.showwarning("无效名称", "类别名称不能为空。")
                category_var.set(list(self.tools_config.keys())[0] if self.tools_config else "新建类别...")
                return
            
            if new_category_name in self.tools_config:
                messagebox.showwarning("名称重复", f"类别 '{new_category_name}' 已存在。")
                category_var.set(new_category_name) # Set to existing
                return

            # Add the new category to tools_config with a default directory
            sanitized_cat_name = new_category_name.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
            self.tools_config[new_category_name] = {
                "directory": os.path.join(TOOLS_ROOT_DIR, sanitized_cat_name),
                "tools": {}
            }
            # Create the physical directory for the new category
            category_path_full = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.tools_config[new_category_name]["directory"])
            os.makedirs(category_path_full, exist_ok=True)
            print(f"Created directory for new category: {category_path_full}")
            
            self.save_tools_config() # Save the updated config
            self.load_tools_config() # Reload to update category buttons
            category_var.set(new_category_name) # Set dropdown to new category
        else:
            # If user cancels or enters empty, revert to the first existing category or "新建类别..."
            category_var.set(list(self.tools_config.keys())[0] if self.tools_config else "新建类别...")


    def search_tools(self, event=None):
        search_text = self.search_entry.get().lower().strip()
        
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for results
        results_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        found_tools = []
        for category, category_info in self.tools_config.items():
            for tool_name, tool_info in category_info["tools"].items():
                if (search_text in tool_name.lower() or 
                    search_text in tool_info["desc"].lower() or
                    search_text in category.lower()): # Search category name too
                    found_tools.append((category, tool_name, tool_info))
        
        if not found_tools:
            no_results_label = ctk.CTkLabel(
                results_frame,
                text="😢 未找到匹配的工具，请尝试其他关键词。",
                font=ctk.CTkFont(size=18, weight="bold", family="Microsoft YaHei UI"),
                text_color=("gray30", "gray70")
            )
            no_results_label.pack(pady=50, padx=20)
            return
        
        # Display search results
        for category, tool_name, tool_info in found_tools:
            self.create_tool_card(results_frame, tool_name, tool_info, category)

    def show_all_tools(self):
        self.current_category = None
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for all tools
        all_tools_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        all_tools_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for category, category_info in sorted(self.tools_config.items()): # Sort categories for consistent display
            if not category_info["tools"]: # Skip empty categories
                continue
            
            category_label = ctk.CTkLabel(
                all_tools_frame,
                text=f"📂 {category}", # Added folder icon
                font=ctk.CTkFont(size=18, weight="bold", family="Microsoft YaHei UI"),
                text_color=self._get_color_hex(self.theme_color) # Use accent color for category headers
            )
            category_label.pack(fill="x", padx=15, pady=(20, 10)) # More padding for headers
            
            for tool_name, tool_info in sorted(category_info["tools"].items()): # Sort tools within category
                self.create_tool_card(all_tools_frame, tool_name, tool_info, category)

    def create_tool_card(self, parent_frame, tool_name, tool_info, category=None):
        tool_frame = ctk.CTkFrame(parent_frame, corner_radius=10, border_width=1, border_color=("gray80", "gray20"))
        tool_frame.pack(fill="x", padx=10, pady=6) # Increased padding
        
        tool_frame.grid_columnconfigure(0, weight=1) # Tool details take most space
        tool_frame.grid_columnconfigure(1, weight=0) # Button takes fixed space

        # Tool name and description
        name_label = ctk.CTkLabel(
            tool_frame,
            text=tool_name,
            font=ctk.CTkFont(size=16, weight="bold", family="Microsoft YaHei UI"),
            wraplength=700,
            anchor="w" # Align left
        )
        name_label.grid(row=0, column=0, padx=15, pady=(10, 2), sticky="w")
        
        desc_label = ctk.CTkLabel(
            tool_frame,
            text=tool_info["desc"],
            font=ctk.CTkFont(size=12),
            wraplength=700,
            anchor="w", # Align left
            text_color=("gray40", "gray60")
        )
        desc_label.grid(row=1, column=0, padx=15, pady=(2, 10), sticky="w")
        
        # Launch button
        launch_btn = ctk.CTkButton(
            tool_frame,
            text="🚀 启动", # Rocket icon
            width=100,
            height=35,
            corner_radius=8,
            command=functools.partial(self.launch_tool, tool_info["path"], tool_name, category),
            fg_color=self._get_color_hex(self.theme_color),
            hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        launch_btn.grid(row=0, column=1, rowspan=2, padx=15, pady=10) # Centered vertically
        
        # Add right-click menu for the tool card
        self.create_tool_context_menu(tool_frame, tool_info["path"], tool_name, category)

    def check_java(self):
        """Checks for Java environment and caches the result."""
        if self._java_path_cached is not None:
            return self._java_path_cached
        
        # 1. Check user-configured Java path first
        if self._java_path and os.path.exists(self._java_path) and ("java.exe" in self._java_path.lower() or "java" in self._java_path.lower()):
            self._java_path_cached = self._java_path
            return self._java_path_cached
        
        # 2. Check JAVA_HOME environment variable
        java_home = os.environ.get('JAVA_HOME')
        if java_home:
            java_exe_path = os.path.join(java_home, 'bin', 'java.exe') # Windows
            if sys.platform != 'win32':
                java_exe_path = os.path.join(java_home, 'bin', 'java') # Linux/macOS
            if os.path.exists(java_exe_path):
                self._java_path_cached = java_exe_path
                return self._java_path_cached
            
        # 3. Check system PATH
        java_path_from_shutil = shutil.which('java')
        if java_path_from_shutil:
            self._java_path_cached = java_path_from_shutil
            return self._java_path_cached
        
        # 4. Try running 'java' command directly (will fail if not in PATH)
        try:
            subprocess.run(['java', '-version'], capture_output=True, check=True, timeout=5) # Add timeout
            self._java_path_cached = 'java' # Means it's in PATH
            return self._java_path_cached
            
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self._java_path_cached = None
            return None
        except Exception as e:
            print(f"Error during Java check: {e}")
            self._java_path_cached = None
            return None

    def show_java_error(self):
        """Displays Java environment missing prompt."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Java环境缺失")
        dialog.geometry("450x200")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        label = ctk.CTkLabel(
            dialog,
            text="未检测到 Java 运行环境，请安装 Java 后再试。\n\n您可以从以下地址下载 Java：",
            wraplength=400,
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=(20, 10))
        
        link_label = ctk.CTkLabel(
            dialog,
            text="https://www.java.com/download/",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14, underline=True)
        )
        link_label.pack(pady=(0, 20))
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.java.com/download/"))
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="确定",
            command=dialog.destroy,
            width=100,
            height=35,
            corner_radius=8,
            fg_color=self._get_color_hex(self.theme_color),
            hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20)
        )
        ok_btn.pack(pady=10)
        self.wait_window(dialog)
    
    def create_context_menu(self, widget, directory):
        menu = Menu(self, tearoff=0, 
                    bg=self._get_menu_bg_color(), 
                    fg=self._get_menu_fg_color(), 
                    activebackground=self._get_color_hex(self.theme_color),
                    activeforeground="white", 
                    font=("Microsoft YaHei UI", 10), 
                    relief="flat", bd=1)
        
        open_dir_cmd = functools.partial(self.open_directory, directory)
        menu.add_command(label="📁 打开目录", command=open_dir_cmd)
        
        widget._context_menu = menu # Store menu reference
        
        widget.bind("<Button-3>", lambda e: self._show_context_menu(e, menu), add="+")
        widget.bind("<Shift-F10>", lambda e: self._show_context_menu(e, menu), add="+")

    def create_tool_context_menu(self, widget, tool_path, tool_name, category=None):
        menu = Menu(self, tearoff=0, 
                    bg=self._get_menu_bg_color(), 
                    fg=self._get_menu_fg_color(), 
                    activebackground=self._get_color_hex(self.theme_color),
                    activeforeground="white", 
                    font=("Microsoft YaHei UI", 10), 
                    relief="flat", bd=1)
        
        open_tool_dir_cmd = functools.partial(self.open_tool_directory, tool_path)
        rename_tool_cmd = functools.partial(self.rename_tool, tool_name, tool_path, category)
        delete_tool_cmd = functools.partial(self.delete_tool, tool_name, tool_path, category) # Add delete option
        
        menu.add_command(label="📂 打开程序目录", command=open_tool_dir_cmd)
        menu.add_separator()
        menu.add_command(label="✏️ 编辑工具信息", command=rename_tool_cmd) # Changed text to be more general
        menu.add_command(label="🗑️ 删除工具", command=delete_tool_cmd)
        
        widget._context_menu = menu # Store menu reference
        
        widget.bind("<Button-3>", lambda e: self._show_context_menu(e, menu), add="+")
        widget.bind("<Shift-F10>", lambda e: self._show_context_menu(e, menu), add="+")

    def _get_menu_bg_color(self):
        """Returns background color for context menus based on theme."""
        return "gray20" if self.theme_mode == "dark" else "gray90"

    def _get_menu_fg_color(self):
        """Returns foreground (text) color for context menus based on theme."""
        return "gray80" if self.theme_mode == "dark" else "gray30"

    def _show_context_menu(self, event, menu):
        """Displays the context menu."""
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
            
    def open_directory(self, directory):
        base_path = os.path.dirname(os.path.abspath(__file__))
        directory_path = os.path.join(base_path, directory)
        
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True) # Ensure it's created if missing
        
        try:
            # Use os.startfile on Windows, xdg-open on Linux, open on macOS
            if sys.platform == "win32":
                os.startfile(directory_path)
            elif sys.platform == "darwin":
                subprocess.Popen(['open', directory_path])
            else: # Linux
                subprocess.Popen(['xdg-open', directory_path])
        except FileNotFoundError:
            self.show_message(f"无法打开目录，请手动打开:\n{directory_path}")
        except Exception as e:
            self.show_message(f"打开目录时出错:\n{str(e)}")
    
    def open_tool_directory(self, tool_path):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_path, tool_path)
            
            if not os.path.exists(full_path):
                self.show_message(f"工具文件不存在：{full_path}")
                return
            
            tool_dir = os.path.dirname(full_path)
            
            # Ensure directory exists before opening (should usually exist if tool_path is valid)
            if not os.path.exists(tool_dir):
                os.makedirs(tool_dir, exist_ok=True)
                
            print(f"Opening directory: {tool_dir}")
            # Use os.startfile on Windows, xdg-open on Linux, open on macOS
            if sys.platform == "win32":
                os.startfile(tool_dir)
            elif sys.platform == "darwin":
                subprocess.Popen(['open', tool_dir])
            else: # Linux
                subprocess.Popen(['xdg-open', tool_dir])
        except Exception as e:
            self.show_message(f"打开程序目录时出错:\n{str(e)}")
            
    def launch_tool(self, tool_path, tool_name, category):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_path, tool_path)
            
            if not os.path.exists(full_path):
                response = messagebox.askyesno(
                    "工具缺失", 
                    f"工具 '{tool_name}' 未找到。\n路径: '{full_path}'\n\n是否从列表中删除此工具？"
                )
                if response:
                    self.delete_tool(tool_name, tool_path, category, silent=True)
                return
            
            working_dir = os.path.dirname(full_path)
            ext = os.path.splitext(tool_path)[1].lower()
            
            def run_tool_threaded():
                try:
                    if ext == '.py':
                        python_exe = self._python_path or sys.executable
                        cmd = [python_exe, full_path]
                        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        subprocess.Popen(cmd, cwd=working_dir, creationflags=creation_flags)
                    elif ext == '.exe':
                        cmd = [full_path]
                        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        subprocess.Popen(cmd, cwd=working_dir, creationflags=creation_flags)
                    elif ext == '.bat':
                        cmd = [full_path]
                        subprocess.Popen(cmd, cwd=working_dir, shell=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
                    elif ext == '.jar':
                        java_path = self._java_path or self.check_java()
                        if not java_path:
                            self.after(0, self.show_java_error) # Show error on main thread
                            return
                        cmd = [java_path, '-jar', full_path]
                        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        subprocess.Popen(cmd, cwd=working_dir, creationflags=creation_flags)
                    elif ext == '.html':
                        webbrowser.open(full_path)
                    else:
                        self.after(0, lambda: self.show_message(f"不支持的文件类型: {ext}"))
                        return
                    
                    print(f"Launched tool: {tool_name} from {full_path}")
                except FileNotFoundError:
                    self.after(0, lambda: self.show_message(f"启动 '{tool_name}' 失败: 命令或文件未找到。"))
                except Exception as e:
                    self.after(0, lambda: self.show_message(f"启动 '{tool_name}' 时出错:\n{str(e)}"))
            
            threading.Thread(target=run_tool_threaded, daemon=True).start()
            
        except Exception as e:
            self.show_message(f"启动工具时发生意外错误:\n{str(e)}")

    def show_message(self, message):
        """Displays a message box."""
        messagebox.showinfo("提示", message)
    
    def show_category(self, category):
        self.current_category = category
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        tools_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        tools_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if category not in self.tools_config or not self.tools_config[category]["tools"]:
            no_tools_label = ctk.CTkLabel(
                tools_frame,
                text=f"此类别 '{category}' 下暂无工具。",
                font=ctk.CTkFont(size=18, weight="bold", family="Microsoft YaHei UI"),
                text_color=("gray30", "gray70")
            )
            no_tools_label.pack(pady=50, padx=20)
            return

        for tool_name, tool_info in sorted(self.tools_config[category]["tools"].items()): # Sort tools
            self.create_tool_card(tools_frame, tool_name, tool_info, category)

    def rename_tool(self, tool_name, tool_path, category=None):
        """Renames a tool or updates its description."""
        if not category:
            for cat_name, cat_info in self.tools_config.items():
                if tool_name in cat_info["tools"]:
                    category = cat_name
                    break
        
        if not category:
            self.show_message("无法确定工具所属类别，无法编辑。")
            return
        
        if tool_name not in self.tools_config[category]["tools"]:
            self.show_message(f"工具 '{tool_name}' 未在类别 '{category}' 中找到。")
            return

        current_tool_info = self.tools_config[category]["tools"][tool_name]
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("编辑工具信息")
        dialog.geometry("550x450")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Apply custom colors
        dialog_fg_color = self.main_frame.cget("fg_color")
        dialog.configure(fg_color=dialog_fg_color)

        # Current name display
        current_name_label = ctk.CTkLabel(dialog, text="当前名称:", font=ctk.CTkFont(weight="bold"))
        current_name_label.pack(padx=20, pady=(20, 5), anchor="w")
        current_name = ctk.CTkLabel(dialog, text=tool_name, font=ctk.CTkFont(size=13, family="Consolas"))
        current_name.pack(padx=20, pady=(0, 10), anchor="w")
        
        # New name input
        new_name_label = ctk.CTkLabel(dialog, text="新名称:", font=ctk.CTkFont(weight="bold"))
        new_name_label.pack(padx=20, pady=(10, 5), anchor="w")
        new_name_entry = ctk.CTkEntry(dialog, width=490, height=35, corner_radius=8)
        new_name_entry.pack(padx=20, pady=(0, 10))
        new_name_entry.insert(0, tool_name) # Pre-fill with current name
        
        # Tool description input
        desc_label = ctk.CTkLabel(dialog, text="工具描述:", font=ctk.CTkFont(weight="bold"))
        desc_label.pack(padx=20, pady=(10, 5), anchor="w")
        desc_entry = ctk.CTkTextbox(dialog, width=490, height=120, corner_radius=8)
        desc_entry.pack(padx=20, pady=(0, 20))
        desc_entry.insert("1.0", current_tool_info["desc"]) # Pre-fill with current description
        
        def apply_changes():
            new_name = new_name_entry.get().strip()
            new_desc = desc_entry.get("1.0", "end-1c").strip()
            
            if not new_name:
                messagebox.showerror("错误", "工具名称不能为空")
                return
            
            if new_name == tool_name and new_desc == current_tool_info["desc"]:
                dialog.destroy() # No changes made
                return
            
            try:
                # Update in-memory config
                if new_name != tool_name:
                    # Check if new name already exists in the same category
                    if new_name in self.tools_config[category]["tools"]:
                        messagebox.showerror("错误", f"新名称 '{new_name}' 已存在于此类别中。")
                        return
                    
                    # Rename the tool entry in the config
                    tool_info_to_move = self.tools_config[category]["tools"].pop(tool_name)
                    self.tools_config[category]["tools"][new_name] = tool_info_to_move
                    
                    # Try to rename the corresponding tool directory on disk
                    old_sanitized_name = tool_name.lower().replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_")
                    new_sanitized_name = new_name.lower().replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_")

                    category_base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.tools_config[category]["directory"])
                    old_tool_dir = os.path.join(category_base_dir, old_sanitized_name)
                    new_tool_dir = os.path.join(category_base_dir, new_sanitized_name)

                    if os.path.exists(old_tool_dir) and old_tool_dir != new_tool_dir:
                        try:
                            os.rename(old_tool_dir, new_tool_dir)
                            print(f"Renamed tool directory from {old_tool_dir} to {new_tool_dir}")
                            # Update the path in the config to reflect the new directory name
                            # This assumes the tool's file is inside a folder named after the tool
                            # Example: tools/category/old_tool_name_folder/file.exe
                            # Changes to: tools/category/new_tool_name_folder/file.exe
                            current_tool_path = self.tools_config[category]["tools"][new_name]["path"]
                            
                            # Replace only the part related to the tool's folder name in its path
                            # This needs careful regex or string manipulation to avoid replacing unrelated parts
                            # A simple replace might work if the folder name is unique enough in the path
                            path_parts = current_tool_path.split('/')
                            # Find if the old_sanitized_name is a directory in the path
                            try:
                                old_folder_index = path_parts.index(old_sanitized_name)
                                path_parts[old_folder_index] = new_sanitized_name
                                self.tools_config[category]["tools"][new_name]["path"] = '/'.join(path_parts)
                                print(f"Updated tool path in config: {self.tools_config[category]['tools'][new_name]['path']}")
                            except ValueError:
                                print(f"Old tool directory name '{old_sanitized_name}' not found in path, skipping path update.")

                        except OSError as e:
                            messagebox.showwarning("警告", f"无法重命名工具目录：{e}\n请手动更改文件夹名称。")
                            print(f"Error renaming directory: {e}")
                
                # Update description (applies whether name changed or not)
                self.tools_config[category]["tools"][new_name if new_name != tool_name else tool_name]["desc"] = new_desc
                
                self.save_tools_config()
                messagebox.showinfo("成功", "工具信息更新成功！")
                dialog.destroy()
                
                # Refresh UI
                self._force_refresh_after_add(category) # This will reload config and refresh view
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("错误", f"更新工具信息失败: {str(e)}")
        
        # Create button container frame
        button_container = ctk.CTkFrame(dialog, fg_color="transparent")
        button_container.pack(side="bottom", fill="x", padx=20, pady=20)
        button_container.grid_columnconfigure((0, 1), weight=1)

        cancel_btn = ctk.CTkButton(
            button_container, 
            text="取消", 
            command=dialog.destroy,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=("gray70", "gray30"), # Muted color for cancel
            hover_color=("gray60", "gray40")
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        confirm_btn = ctk.CTkButton(
            button_container, 
            text="确认修改", 
            command=apply_changes,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=self._get_color_hex(self.theme_color),
            hover_color=self._adjust_color(self._get_color_hex(self.theme_color), -20)
        )
        confirm_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def delete_tool(self, tool_name, tool_path, category, silent=False):
        """Deletes a tool from the configuration and optionally its files."""
        if not category:
            # Find category if not provided (e.g., from "All Tools" view)
            for cat_name, cat_info in self.tools_config.items():
                if tool_name in cat_info["tools"]:
                    category = cat_name
                    break
        
        if not category:
            if not silent:
                self.show_message("无法确定工具所属类别，无法删除。")
            return
        
        if tool_name not in self.tools_config[category]["tools"]:
            if not silent:
                self.show_message(f"工具 '{tool_name}' 未在类别 '{category}' 中找到。")
            return

        if not silent:
            response = messagebox.askyesno(
                "确认删除", 
                f"确定要从 '{category}' 类别中删除工具 '{tool_name}' 吗？"
            )
        else: # For silent deletion (e.g., after launching a missing tool)
            response = True # Assume yes for silent deletion

        if response:
            try:
                # Remove from in-memory config
                del self.tools_config[category]["tools"][tool_name]
                
                # Check if the category is now empty
                if not self.tools_config[category]["tools"]:
                    if not silent:
                        remove_category_response = messagebox.askyesno(
                            "类别为空",
                            f"类别 '{category}' 现在已空。是否删除此类别？\n\n注意：删除类别将同时删除其对应的工具文件夹！"
                        )
                    else:
                        remove_category_response = False # Don't silently delete category

                    if remove_category_response:
                        category_directory_to_delete = self.tools_config[category]["directory"]
                        del self.tools_config[category]
                        try:
                            full_category_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), category_directory_to_delete)
                            if os.path.exists(full_category_path):
                                shutil.rmtree(full_category_path)
                                print(f"Removed empty category directory: {full_category_path}")
                        except OSError as e:
                            messagebox.showwarning("警告", f"无法删除类别目录 '{full_category_path}'：{e}\n请手动删除。")
                        except Exception as e:
                            messagebox.showwarning("警告", f"删除类别目录时发生错误：{e}")

                # Save updated config
                self.save_tools_config()

                # Prompt to delete physical files, unless silent
                if not silent:
                    delete_files_response = messagebox.askyesno(
                        "删除文件",
                        f"您是否也要删除与工具 '{tool_name}' 相关的文件和其所在的文件夹？\n\n这会删除：'{os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)), tool_path))}'"
                    )
                else:
                    delete_files_response = True # Silently delete files if the tool was missing

                if delete_files_response:
                    full_tool_dir = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)), tool_path))
                    try:
                        if os.path.exists(full_tool_dir):
                            shutil.rmtree(full_tool_dir)
                            print(f"Removed tool directory: {full_tool_dir}")
                            if not silent:
                                self.show_message(f"工具 '{tool_name}' 及其文件已成功删除。")
                        else:
                            if not silent:
                                self.show_message(f"工具 '{tool_name}' 已从列表中删除，但其文件目录不存在，无需删除。")
                    except OSError as e:
                        if not silent:
                            messagebox.showwarning("警告", f"无法删除工具目录 '{full_tool_dir}'：{e}\n请手动删除。")
                    except Exception as e:
                        if not silent:
                            messagebox.showwarning("警告", f"删除工具文件时发生错误：{e}")
                else:
                    if not silent:
                        self.show_message(f"工具 '{tool_name}' 已从列表中删除。")
                
                # Refresh UI
                self._force_refresh_after_add(category) # This will reload config and refresh view
            except Exception as e:
                import traceback
                traceback.print_exc()
                if not silent:
                    messagebox.showerror("错误", f"删除工具失败: {str(e)}")
        elif not silent:
            messagebox.showinfo("取消", "已取消删除操作。")

    def toggle_theme(self):
        """Toggles theme mode (light/dark)."""
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️")
        else:
            self.theme_mode = "light"
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙")
        self.save_app_settings() # Save theme preference
        # Reapply colors to reflect theme change on context menus etc.
        self._apply_saved_color()


    def add_tool(self):
        """Handles add tool button click."""
        file_path = filedialog.askopenfilename(
            title="选择工具文件",
            filetypes=[
                ("所有支持的文件", "*.exe *.py *.bat *.jar *.html"),
                ("可执行文件", "*.exe"),
                ("Python脚本", "*.py"),
                ("批处理文件", "*.bat"),
                ("Java应用", "*.jar"),
                ("HTML文件", "*.html"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.show_add_tool_dialog(file_path, category_hint=self.current_category)

    def open_settings(self):
        """Opens the settings interface."""
        try:
            # Dynamically import settings to avoid circular dependencies and ensure it's reloaded if modified
            import importlib
            # Ensure settings module can access app properties
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            try:
                import settings_module
                importlib.reload(settings_module)
            except ImportError:
                messagebox.showwarning("警告", "settings_module.py 文件不存在或已损坏。")
                return
            
            # Pass current settings to the settings dialog
            current_settings = {
                "theme_mode": self.theme_mode,
                "theme_color": self.theme_color,
                "background_run": self.background_run,
                "hotkey": self.hotkey,
                "python_path": self._python_path,
                "java_path": self._java_path
            }
            
            # Open settings window, passing a callback for applying settings
            settings_module.open_settings(self, current_settings, self.apply_settings)
            
        except Exception as e:
            self.show_message(f"打开设置时出错:\n{str(e)}")

    def _force_refresh_after_add(self, category_to_show=None):
        """Forces UI refresh after adding/renaming/deleting a tool."""
        print(f"Forcing UI refresh, target category: {category_to_show}")
        
        # Reload tools configuration from JSON
        self.load_tools_config()
        
        # Determine which view to show
        if category_to_show and category_to_show in self.tools_config:
            self.show_category(category_to_show)
        else:
            self.show_all_tools()
            
        self.update_idletasks() # Ensure UI updates are processed

if __name__ == "__main__":
    # Ensure the settings_module.py file exists for the settings dialog to work
    # This block will create/update settings_module.py if it's missing or outdated
    settings_content = """
import customtkinter as ctk
import json
import os
from tkinter import filedialog, messagebox

# Assuming APP_SETTINGS_FILE path is relative to the script's directory
APP_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.json")

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, master, current_settings, apply_callback):
        super().__init__(master)
        self.master = master
        self.apply_callback = apply_callback
        
        self.title("设置")
        self.geometry("600x550")
        self.transient(master)  # Make it modal
        self.grab_set()         # Grab focus
        self.resizable(False, False)

        # Apply custom colors from the main app's theme
        dialog_fg_color = master.main_frame.cget("fg_color")
        self.configure(fg_color=dialog_fg_color)
        
        # Variables to hold settings
        self.theme_mode_var = ctk.StringVar(value=current_settings.get("theme_mode", "light"))
        self.theme_color_var = ctk.StringVar(value=current_settings.get("theme_color", "蓝色"))
        self.background_run_var = ctk.BooleanVar(value=current_settings.get("background_run", False))
        self.hotkey_var = ctk.StringVar(value=current_settings.get("hotkey", "ctrl+alt+t"))
        self.python_path_var = ctk.StringVar(value=current_settings.get("python_path", ""))
        self.java_path_var = ctk.StringVar(value=current_settings.get("java_path", ""))

        # Create settings frames
        self.create_theme_settings()
        self.create_general_settings()
        self.create_path_settings()
        
        # Buttons at the bottom
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="取消", 
            command=self.destroy,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        save_btn = ctk.CTkButton(
            button_frame, 
            text="保存并应用", 
            command=self.save_settings,
            width=220,
            height=40,
            corner_radius=8,
            fg_color=master._get_color_hex(master.theme_color), # Use main app's theme color
            hover_color=master._adjust_color(master._get_color_hex(master.theme_color), -20) # Use main app's color adjust
        )
        save_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def create_theme_settings(self):
        frame = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color=("gray80", "gray20"))
        frame.pack(padx=20, pady=(20, 10), fill="x", expand=False)
        frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="主题设置", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        
        ctk.CTkLabel(frame, text="界面模式:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        mode_optionmenu = ctk.CTkOptionMenu(frame, values=["light", "dark"], variable=self.theme_mode_var, 
                                            width=150, corner_radius=8)
        mode_optionmenu.grid(row=1, column=1, padx=15, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="主题颜色:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        color_optionmenu = ctk.CTkOptionMenu(frame, values=["蓝色", "红色", "绿色", "紫色"], variable=self.theme_color_var,
                                             width=150, corner_radius=8)
        color_optionmenu.grid(row=2, column=1, padx=15, pady=5, sticky="ew")

    def create_general_settings(self):
        frame = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color=("gray80", "gray20"))
        frame.pack(padx=20, pady=10, fill="x", expand=False)
        frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="通用设置", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        ctk.CTkLabel(frame, text="后台运行 (最小化到托盘):").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        bg_run_checkbox = ctk.CTkCheckBox(frame, text="", variable=self.background_run_var)
        bg_run_checkbox.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="显示/隐藏主窗口快捷键:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        hotkey_entry = ctk.CTkEntry(frame, textvariable=self.hotkey_var, width=150, corner_radius=8)
        hotkey_entry.grid(row=2, column=1, padx=15, pady=5, sticky="ew")
        
    def create_path_settings(self):
        frame = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color=("gray80", "gray20"))
        frame.pack(padx=20, pady=(10, 20), fill="x", expand=False)
        frame.columnconfigure(1, weight=1) # Entry column
        frame.columnconfigure(2, weight=0) # Button column

        ctk.CTkLabel(frame, text="解释器/运行时路径 (可选)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=3, padx=15, pady=10, sticky="w")

        # Python Path
        ctk.CTkLabel(frame, text="Python 解释器路径:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        python_entry = ctk.CTkEntry(frame, textvariable=self.python_path_var, width=250, corner_radius=8)
        python_entry.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="ew")
        python_browse_btn = ctk.CTkButton(frame, text="浏览...", command=lambda: self.browse_path(self.python_path_var, "exe"), width=80, height=30, corner_radius=8)
        python_browse_btn.grid(row=1, column=2, padx=(5, 15), pady=5, sticky="e")

        # Java Path
        ctk.CTkLabel(frame, text="Java (JDK/JRE) 路径:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        java_entry = ctk.CTkEntry(frame, textvariable=self.java_path_var, width=250, corner_radius=8)
        java_entry.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="ew")
        java_browse_btn = ctk.CTkButton(frame, text="浏览...", command=lambda: self.browse_path(self.java_path_var, "exe"), width=80, height=30, corner_radius=8)
        java_browse_btn.grid(row=2, column=2, padx=(5, 15), pady=5, sticky="e")

    def browse_path(self, var_to_set, file_type):
        if file_type == "exe":
            path = filedialog.askopenfilename(title="选择可执行文件", filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])
        elif file_type == "dir":
            path = filedialog.askdirectory(title="选择目录")
        else:
            path = None 

        if path:
            var_to_set.set(path)

    def save_settings(self):
        settings_to_apply = {
            "theme_mode": self.theme_mode_var.get(),
            "theme_color": self.theme_color_var.get(),
            "background_run": self.background_run_var.get(),
            "hotkey": self.hotkey_var.get(),
            "python_path": self.python_path_var.get(),
            "java_path": self.java_path_var.get()
        }
        self.apply_callback(settings_to_apply)
        self.destroy()

def open_settings(master_app, current_settings, apply_callback):
    # This function is called from the main app to open the settings dialog
    SettingsDialog(master_app, current_settings, apply_callback)
"""
    settings_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings_module.py")
    try:
        with open(settings_file_path, 'w', encoding='utf-8') as f:
            f.write(settings_content)
    except IOError as e:
        print(f"Error writing settings_module.py: {e}")
        messagebox.showerror("文件写入错误", f"无法创建或更新 settings_module.py 文件。\n请检查文件权限或磁盘空间。\n错误: {e}")
        sys.exit(1) # Exit if essential file can't be created

    try:
        app = ToolBox()
        
        if HAS_TRAY_SUPPORT:
            app.create_tray_icon()
            
        if HAS_KEYBOARD_SUPPORT:
            app.register_hotkey()
            
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Hide window on startup if background run is enabled and tray icon exists
        if app.background_run and HAS_TRAY_SUPPORT:
            app.withdraw()
            
        app.mainloop()
    except Exception as e:
        print(f"Startup error: {str(e)}")
        messagebox.showerror("启动错误", f"应用程序启动失败: {str(e)}\n请检查控制台输出获取更多信息。")
        # For a production application, you might want to log this to a file.