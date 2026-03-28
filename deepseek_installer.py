#!/usr/bin/env python3
"""
DeepSeek 1.5B模型本地部署工具
内置Ollama安装和管理功能 - 科技感图形界面版
"""

import os
import sys
import platform
import subprocess
import urllib.request
import tempfile
import threading
import time
from tkinter import Tk, Frame, Label, Button, Text, Scrollbar, Entry, messagebox
from tkinter.ttk import Progressbar, Style
import tkinter.font as tkFont

class OllamaDeepSeekInstaller:
    def __init__(self, gui_callback=None):
        self.system = platform.system().lower()
        self.ollama_installed = self.check_ollama_installed()
        self.model_name = "deepseek:1.5b"
        self.gui_callback = gui_callback  # GUI回调函数用于更新进度
        
        # 配置选项
        self.config = {
            "model_path": self.get_default_model_path(),
            "ollama_port": 11434,
            "proxy": ""
        }
    
    def get_default_model_path(self):
        """获取默认模型保存路径"""
        if self.system == "windows":
            return os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Public"), ".ollama", "models")
        elif self.system == "darwin":
            return os.path.join(os.environ.get("HOME", "/Users"), ".ollama", "models")
        elif self.system == "linux":
            return os.path.join(os.environ.get("HOME", "/home"), ".ollama", "models")
        else:
            return os.path.join(os.getcwd(), ".ollama", "models")
    
    def get_ollama_config(self):
        """获取Ollama配置"""
        if not self.ollama_installed:
            return None
        
        try:
            result = subprocess.run(
                ["ollama", "config", "show"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return None
    
    def set_ollama_config(self, config_key, config_value):
        """设置Ollama配置"""
        if not self.ollama_installed:
            return False
        
        try:
            subprocess.run(
                ["ollama", "config", "set", f"{config_key}={config_value}"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def check_ollama_installed(self):
        """检查Ollama是否已安装"""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ollama(self, progress_callback=None):
        """根据不同系统安装Ollama"""
        if progress_callback:
            progress_callback(10, "开始安装Ollama...")
        
        if self.system == "windows":
            success = self._install_ollama_windows(progress_callback)
        elif self.system == "darwin":  # macOS
            success = self._install_ollama_macos(progress_callback)
        elif self.system == "linux":
            success = self._install_ollama_linux(progress_callback)
        else:
            if progress_callback:
                progress_callback(0, f"不支持的操作系统: {self.system}")
            return False
        
        self.ollama_installed = self.check_ollama_installed()
        if success and progress_callback:
            progress_callback(100, "Ollama安装完成！")
        return success
    
    def _install_ollama_windows(self, progress_callback):
        """Windows系统安装Ollama"""
        if progress_callback:
            progress_callback(10, "正在准备Ollama安装...")
        
        # Ollama Windows安装包下载地址
        url = "https://ollama.com/download/OllamaSetup.exe"
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, "OllamaSetup.exe")
        
        try:
            if progress_callback:
                progress_callback(20, "正在验证下载地址...")
            
            # 自定义下载进度回调
            def reporthook(blocknum, blocksize, totalsize):
                if totalsize <= 0:
                    percent = 0
                else:
                    percent = int(min(85, (blocknum * blocksize * 65) / totalsize + 20))  # 20-85%
                if progress_callback:
                    downloaded = blocknum * blocksize
                    total_mb = totalsize / (1024 * 1024)
                    downloaded_mb = downloaded / (1024 * 1024)
                    progress_callback(percent, f"下载Ollama安装包: {int((percent-20)/0.65)}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)")
            
            # 下载安装包
            if progress_callback:
                progress_callback(25, "开始下载Ollama安装包...")
            urllib.request.urlretrieve(url, installer_path, reporthook=reporthook)
            
            if progress_callback:
                progress_callback(85, "下载完成，正在运行安装程序...")
            
            # 运行安装程序 - 使用shell=True确保能正确执行
            subprocess.run(
                installer_path,
                check=True,
                shell=True
            )
            
            if progress_callback:
                progress_callback(95, "安装完成，正在验证...")
            
            # 验证安装是否成功
            time.sleep(2)
            if self.check_ollama_installed():
                return True
            else:
                if progress_callback:
                    progress_callback(0, "安装程序已完成，但Ollama未检测到，请手动验证")
                return False
                
        except urllib.error.URLError as e:
            if progress_callback:
                progress_callback(0, f"网络错误: 无法下载安装包 - {e}")
            return False
        except subprocess.CalledProcessError as e:
            if progress_callback:
                progress_callback(0, f"安装程序执行失败: {e}")
            return False
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"安装失败: {e}")
            return False
    
    def _install_ollama_macos(self, progress_callback):
        """macOS系统安装Ollama"""
        if progress_callback:
            progress_callback(30, "正在通过curl安装Ollama...")
        
        try:
            # 使用curl命令安装
            process = subprocess.Popen(
                ["curl", "-fsSL", "https://ollama.com/install.sh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # 实时读取输出
            install_script = process.communicate()[0]
            
            # 执行安装脚本
            subprocess.run(
                ["sh", "-c", install_script],
                check=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            if progress_callback:
                progress_callback(0, f"安装失败: {e}")
            return False
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"安装失败: {e}")
            return False
    
    def _install_ollama_linux(self, progress_callback):
        """Linux系统安装Ollama"""
        if progress_callback:
            progress_callback(30, "正在通过curl安装Ollama...")
        
        try:
            # 检查是否有sudo权限
            has_sudo = False
            try:
                subprocess.run(
                    ["sudo", "-n", "echo", "test"],
                    capture_output=True,
                    check=True
                )
                has_sudo = True
            except:
                pass
            
            # 使用curl命令安装
            if has_sudo:
                # 有sudo权限，使用sudo安装
                process = subprocess.Popen(
                    ["curl", "-fsSL", "https://ollama.com/install.sh"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            else:
                # 没有sudo权限，尝试普通用户安装
                process = subprocess.Popen(
                    ["curl", "-fsSL", "https://ollama.com/install.sh"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            
            # 实时读取输出
            install_script = process.communicate()[0]
            
            if has_sudo:
                # 有sudo权限，使用sudo执行安装脚本
                subprocess.run(
                    ["sudo", "sh", "-c", install_script],
                    check=True
                )
            else:
                # 没有sudo权限，尝试普通用户执行安装脚本
                subprocess.run(
                    ["sh", "-c", install_script],
                    check=True
                )
            
            return True
        except subprocess.CalledProcessError as e:
            if progress_callback:
                progress_callback(0, f"安装失败: {e}")
            return False
        except PermissionError:
            if progress_callback:
                progress_callback(0, "安装失败: 权限不足，请使用sudo运行或联系系统管理员")
            return False
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"安装失败: {e}")
            return False
    
    def download_model(self, progress_callback=None):
        """下载DeepSeek 1.5B模型"""
        if not self.ollama_installed:
            if progress_callback:
                progress_callback(0, "请先安装Ollama！")
            return False
        
        if progress_callback:
            progress_callback(10, f"正在下载DeepSeek 1.5B模型 ({self.model_name})...")
        
        try:
            # 启动下载进程
            process = subprocess.Popen(
                ["ollama", "pull", self.model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # 实时读取输出并更新进度
            progress = 10
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    if progress_callback:
                        # 直接显示Ollama的输出信息，而不是模拟进度
                        progress = min(95, progress + 1)
                        progress_callback(progress, f"模型下载中: {output.strip()}")
                time.sleep(0.5)
            
            if process.returncode == 0:
                if progress_callback:
                    progress_callback(100, "模型下载完成！")
                return True
            else:
                if progress_callback:
                    error_output = process.stdout.read()
                    progress_callback(0, f"下载失败: {error_output}")
                return False
                
        except subprocess.CalledProcessError as e:
            if progress_callback:
                progress_callback(0, f"下载失败: {e.stderr}")
            return False
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"下载失败: {str(e)}")
            return False
    
    def run_model(self):
        """运行DeepSeek 1.5B模型"""
        if not self.ollama_installed:
            return False
        
        try:
            subprocess.run(
                ["ollama", "run", self.model_name],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def delete_model(self):
        """删除DeepSeek 1.5B模型"""
        if not self.ollama_installed:
            return False
        
        try:
            subprocess.run(
                ["ollama", "rm", self.model_name],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def update_model(self):
        """更新DeepSeek 1.5B模型"""
        if not self.ollama_installed:
            return False
        
        try:
            subprocess.run(
                ["ollama", "pull", self.model_name],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def list_models(self):
        """列出已安装的Ollama模型"""
        if not self.ollama_installed:
            return None
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return None

class DeepSeekGUI:
    def __init__(self, master):
        self.master = master
        self.installer = OllamaDeepSeekInstaller(self)
        
        # 设置窗口属性
        master.title("DeepSeek 1.5B 本地部署工具")
        master.geometry("800x600")
        master.resizable(True, True)
        
        # 科技感主题
        self.setup_theme()
        
        # 创建界面元素
        self.create_widgets()
        
        # 初始化状态
        self.update_status()
    
    def setup_theme(self):
        """设置科技感主题"""
        # 深色科技感配色
        self.bg_color = "#050a14"  # 深蓝黑色背景
        self.fg_color = "#00ffaa"  # 荧光绿主色调
        self.accent_color = "#00ccff"  # 亮蓝强调色
        self.dark_color = "#101828"  # 深色面板
        self.light_color = "#1a2332"  # 浅色面板
        self.error_color = "#ff4444"  # 错误红色
        self.warning_color = "#ffaa00"  # 警告黄色
        
        self.master.configure(bg=self.bg_color)
        
        # 创建样式
        self.style = Style()
        self.style.theme_use("clam")
        
        # 主按钮样式
        self.style.configure("Primary.TButton", 
                           background=self.accent_color, 
                           foreground="#000000",
                           borderwidth=2,
                           relief="flat",
                           padding=12,
                           font=tkFont.Font(family="Consolas", size=11, weight="bold"))
        self.style.map("Primary.TButton", 
                      background=[("active", self.fg_color)],
                      foreground=[("active", "#000000")],
                      bordercolor=[("focus", self.fg_color)])
        
        # 次要按钮样式
        self.style.configure("Secondary.TButton", 
                           background=self.light_color, 
                           foreground=self.fg_color,
                           borderwidth=1,
                           relief="flat",
                           padding=12,
                           font=tkFont.Font(family="Consolas", size=11))
        self.style.map("Secondary.TButton", 
                      background=[("active", self.dark_color)],
                      foreground=[("active", self.accent_color)])
        
        # 进度条样式
        self.style.configure("TProgressbar",
                           troughcolor=self.dark_color,
                           background=self.fg_color,
                           bordercolor=self.accent_color,
                           borderwidth=2,
                           thickness=10)
        
        # 标签样式
        self.style.configure("TLabel",
                           background=self.bg_color,
                           foreground=self.fg_color)
        
        # 创建霓虹效果的标题字体
        self.title_font = tkFont.Font(family="Consolas", size=28, weight="bold")
        self.subtitle_font = tkFont.Font(family="Consolas", size=14, slant="italic")
        self.header_font = tkFont.Font(family="Consolas", size=12, weight="bold")
        self.text_font = tkFont.Font(family="Consolas", size=10)
    
    def create_widgets(self):
        """创建界面元素"""
        # 标题框架
        title_frame = Frame(self.master, bg=self.bg_color, bd=0)
        title_frame.pack(fill="x", padx=30, pady=30)
        
        # 标题 - 霓虹效果
        self.title_label = Label(title_frame, text="DeepSeek 1.5B 本地部署", 
                               font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        self.title_label.pack()
        
        # 副标题
        self.subtitle_label = Label(title_frame, text="内置Ollama支持 | 科技感界面", 
                                  font=self.subtitle_font, bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label.pack(pady=8)
        
        # 系统状态卡片
        status_frame = Frame(self.master, bg=self.dark_color, bd=2, relief="groove", 
                           highlightbackground=self.accent_color, highlightthickness=1)
        status_frame.pack(fill="x", padx=30, pady=10)
        
        # 系统信息行
        sys_info_frame = Frame(status_frame, bg=self.dark_color)
        sys_info_frame.pack(fill="x", padx=15, pady=12)
        
        # 系统信息标签
        sys_label = Label(sys_info_frame, text="系统:", 
                        font=self.header_font, bg=self.dark_color, fg=self.accent_color, width=10)
        sys_label.pack(side="left", anchor="w")
        
        # 系统信息内容
        system_info = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
        self.system_label = Label(sys_info_frame, text=system_info, 
                                font=self.text_font, bg=self.dark_color, fg=self.fg_color, anchor="w")
        self.system_label.pack(side="left", fill="x", expand=True)
        
        # Ollama状态行
        ollama_status_frame = Frame(status_frame, bg=self.dark_color)
        ollama_status_frame.pack(fill="x", padx=15, pady=5, ipady=5)
        
        # Ollama状态标签
        ollama_label = Label(ollama_status_frame, text="Ollama:", 
                           font=self.header_font, bg=self.dark_color, fg=self.accent_color, width=10)
        ollama_label.pack(side="left", anchor="w")
        
        # Ollama状态内容
        self.ollama_status_label = Label(ollama_status_frame, text="未安装", 
                                        font=self.text_font, bg=self.dark_color, fg=self.error_color, 
                                        anchor="w", padx=5)
        self.ollama_status_label.pack(side="left", fill="x", expand=True)
        
        # 操作按钮框架
        button_frame = Frame(self.master, bg=self.bg_color)
        button_frame.pack(fill="x", padx=30, pady=25)
        
        # 使用ttk按钮替代普通按钮，支持样式
        from tkinter.ttk import Button as ttkButton
        
        # 安装Ollama按钮
        self.install_ollama_btn = ttkButton(button_frame, text="安装Ollama", 
                                          command=self.install_ollama_thread, 
                                          style="Primary.TButton")
        self.install_ollama_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 下载模型按钮
        self.download_model_btn = ttkButton(button_frame, text="下载DeepSeek模型", 
                                          command=self.download_model_thread, 
                                          style="Secondary.TButton")
        self.download_model_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 更新模型按钮
        self.update_model_btn = ttkButton(button_frame, text="更新DeepSeek模型", 
                                          command=self.update_model_thread, 
                                          style="Secondary.TButton")
        self.update_model_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 运行模型按钮
        self.run_model_btn = ttkButton(button_frame, text="运行DeepSeek模型", 
                                     command=self.run_model, 
                                     style="Secondary.TButton")
        self.run_model_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 删除模型按钮
        self.delete_model_btn = ttkButton(button_frame, text="删除DeepSeek模型", 
                                         command=self.delete_model_thread, 
                                         style="Secondary.TButton")
        self.delete_model_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 模型状态区域
        model_status_frame = Frame(self.master, bg=self.dark_color, bd=2, relief="groove", 
                                  highlightbackground=self.accent_color, highlightthickness=1)
        model_status_frame.pack(fill="x", padx=30, pady=10)
        
        # 模型状态标题
        model_status_title = Label(model_status_frame, text="模型状态", 
                                  font=self.header_font, bg=self.dark_color, fg=self.accent_color)
        model_status_title.pack(anchor="w", padx=15, pady=12)
        
        # 已安装模型列表
        self.model_list_text = Text(model_status_frame, bg=self.bg_color, fg=self.fg_color, 
                                   font=self.text_font, borderwidth=1, relief="sunken", 
                                   wrap="word", height=5)
        self.model_list_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # 刷新模型列表按钮
        refresh_btn = ttkButton(model_status_frame, text="刷新模型列表", 
                               command=self.refresh_model_list, style="Secondary.TButton")
        refresh_btn.pack(anchor="e", padx=15, pady=(0, 15))
        
        # 进度条区域
        progress_container = Frame(self.master, bg=self.dark_color, bd=1, relief="ridge")
        progress_container.pack(fill="x", padx=30, pady=15)
        
        # 进度标签
        self.progress_label = Label(progress_container, text="就绪", 
                                  font=self.header_font, bg=self.dark_color, fg=self.fg_color)
        self.progress_label.pack(anchor="w", padx=15, pady=10)
        
        # 进度条
        self.progress_bar = Progressbar(progress_container, orient="horizontal", 
                                      length=100, mode="determinate",
                                      style="TProgressbar")
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 15))
        
        # 日志输出区域
        log_container = Frame(self.master, bg=self.dark_color, bd=2, relief="groove", 
                            highlightbackground=self.accent_color, highlightthickness=1)
        log_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 日志标题栏
        log_header = Frame(log_container, bg=self.dark_color)
        log_header.pack(fill="x", padx=15, pady=12)
        
        # 日志标题
        log_title = Label(log_header, text="操作日志", 
                        font=self.header_font, bg=self.dark_color, fg=self.accent_color)
        log_title.pack(anchor="w", side="left")
        
        # 日志清理按钮
        clear_btn = ttkButton(log_header, text="清空", width=6, command=self.clear_log, 
                            style="Secondary.TButton")
        clear_btn.pack(anchor="e", side="right")
        
        # 日志文本框
        self.log_text = Text(log_container, bg=self.bg_color, fg=self.fg_color,
                           font=self.text_font, borderwidth=1, relief="sunken", 
                           wrap="word", selectbackground=self.accent_color, 
                           selectforeground=self.bg_color)
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15), side="left")
        
        # 滚动条样式
        scrollbar = Scrollbar(log_container, command=self.log_text.yview, 
                            bg=self.dark_color, troughcolor=self.light_color,
                            activebackground=self.accent_color, highlightthickness=0)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 底部信息
        footer_frame = Frame(self.master, bg=self.bg_color)
        footer_frame.pack(fill="x", padx=30, pady=20)
        
        footer_label = Label(footer_frame, text="DeepSeek 1.5B Local Deployer v1.1 | 科技感界面", 
                           font=tkFont.Font(family="Consolas", size=9), 
                           bg=self.bg_color, fg="#6688aa")
        footer_label.pack(anchor="center")
        
    def clear_log(self):
        """清空日志"""
        self.log_text.delete("1.0", "end")
        self.log("日志已清空")
    
    def update_status(self):
        """更新状态显示"""
        self.installer.ollama_installed = self.installer.check_ollama_installed()
        
        if self.installer.ollama_installed:
            self.ollama_status_label.config(text="Ollama: 已安装", fg=self.fg_color)
            self.download_model_btn.config(state="normal")
            self.run_model_btn.config(state="normal")
            self.update_model_btn.config(state="normal")
            self.delete_model_btn.config(state="normal")
            self.refresh_model_list()
        else:
            self.ollama_status_label.config(text="Ollama: 未安装", fg="#ff6b6b")
            self.download_model_btn.config(state="disabled")
            self.run_model_btn.config(state="disabled")
            self.update_model_btn.config(state="disabled")
            self.delete_model_btn.config(state="disabled")
            self.model_list_text.delete("1.0", "end")
            self.model_list_text.insert("end", "请先安装Ollama")
    
    def refresh_model_list(self):
        """刷新已安装模型列表"""
        models = self.installer.list_models()
        self.model_list_text.delete("1.0", "end")
        if models:
            self.model_list_text.insert("end", models)
        else:
            self.model_list_text.insert("end", "未检测到已安装的模型")
    
    def log(self, message):
        """记录日志"""
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see("end")
    
    def update_progress(self, percent, message):
        """更新进度条和状态"""
        self.progress_bar["value"] = percent
        self.progress_label.config(text=message)
        self.log(message)
        self.master.update_idletasks()
    
    def install_ollama_thread(self):
        """安装Ollama的线程"""
        self.install_ollama_btn.config(state="disabled")
        self.log("开始安装Ollama...")
        
        # 创建线程执行安装
        def install_thread():
            success = self.installer.install_ollama(progress_callback=self.update_progress)
            self.master.after(0, lambda: self.install_ollama_finished(success))
        
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()
    
    def install_ollama_finished(self, success):
        """Ollama安装完成回调"""
        self.install_ollama_btn.config(state="normal")
        self.update_status()
        
        if success:
            messagebox.showinfo("成功", "Ollama安装完成！")
        else:
            messagebox.showerror("失败", "Ollama安装失败！")
    
    def download_model_thread(self):
        """下载模型的线程"""
        self.download_model_btn.config(state="disabled")
        self.log("开始下载DeepSeek 1.5B模型...")
        
        # 创建线程执行下载
        def download_thread():
            success = self.installer.download_model(progress_callback=self.update_progress)
            self.master.after(0, lambda: self.download_model_finished(success))
        
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
    
    def download_model_finished(self, success):
        """模型下载完成回调"""
        self.download_model_btn.config(state="normal")
        
        if success:
            messagebox.showinfo("成功", "DeepSeek 1.5B模型下载完成！")
            self.refresh_model_list()
        else:
            messagebox.showerror("失败", "DeepSeek 1.5B模型下载失败！")
    
    def update_model_thread(self):
        """更新模型的线程"""
        self.update_model_btn.config(state="disabled")
        self.log("开始更新DeepSeek 1.5B模型...")
        
        # 创建线程执行更新
        def update_thread():
            success = self.installer.update_model()
            self.master.after(0, lambda: self.update_model_finished(success))
        
        thread = threading.Thread(target=update_thread)
        thread.daemon = True
        thread.start()
    
    def update_model_finished(self, success):
        """模型更新完成回调"""
        self.update_model_btn.config(state="normal")
        
        if success:
            messagebox.showinfo("成功", "DeepSeek 1.5B模型更新完成！")
            self.refresh_model_list()
        else:
            messagebox.showerror("失败", "DeepSeek 1.5B模型更新失败！")
    
    def delete_model_thread(self):
        """删除模型的线程"""
        if messagebox.askyesno("确认", f"确定要删除DeepSeek 1.5B模型吗？"):
            self.delete_model_btn.config(state="disabled")
            self.log("开始删除DeepSeek 1.5B模型...")
            
            # 创建线程执行删除
            def delete_thread():
                success = self.installer.delete_model()
                self.master.after(0, lambda: self.delete_model_finished(success))
            
            thread = threading.Thread(target=delete_thread)
            thread.daemon = True
            thread.start()
    
    def delete_model_finished(self, success):
        """模型删除完成回调"""
        self.delete_model_btn.config(state="normal")
        
        if success:
            messagebox.showinfo("成功", "DeepSeek 1.5B模型删除完成！")
            self.refresh_model_list()
        else:
            messagebox.showerror("失败", "DeepSeek 1.5B模型删除失败！")
    
    def run_model(self):
        """运行模型"""
        self.log("启动DeepSeek 1.5B模型...")
        self.log("输入 'exit' 退出模型交互")
        
        def run_thread():
            success = self.installer.run_model()
            if not success:
                self.master.after(0, lambda: messagebox.showerror("失败", "模型运行失败！"))
        
        thread = threading.Thread(target=run_thread)
        thread.daemon = True
        thread.start()

def main():
    """主函数"""
    root = Tk()
    app = DeepSeekGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()