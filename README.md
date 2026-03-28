# DeepSeek 1.5B 本地部署工具

一个自动安装Ollama并部署DeepSeek 1.5B模型的工具，支持跨平台使用，提供科技感图形界面。

## 功能特性

- ✅ **自动安装Ollama**：支持Windows、macOS和Linux系统
- ✅ **一键下载DeepSeek 1.5B模型**：官方标准模型名称 `deepseek:1.5b`
- ✅ **模型管理功能**：
  - 列出已安装的所有Ollama模型
  - 更新DeepSeek模型到最新版本
  - 删除不再需要的模型
- ✅ **科技感图形界面**：直观易用的GUI操作界面
- ✅ **实时进度显示**：安装和下载过程实时反馈
- ✅ **详细日志记录**：操作过程全程记录
- ✅ **跨平台支持**：适配主流操作系统
- ✅ **配置管理**：支持模型路径、端口和代理设置

## 系统要求

- Windows 10/11、macOS 10.15+ 或 Linux
- Python 3.7+（Windows用户需要安装Python）
- 至少4GB RAM（推荐8GB以上）
- 至少5GB可用磁盘空间

## 使用方法

### 1. 运行安装工具

**Windows用户**：
```powershell
python deepseek_installer.py
```

**macOS/Linux用户**：
```bash
chmod +x deepseek_installer.py
./deepseek_installer.py
```

### 2. GUI界面操作指南

启动工具后，您将看到一个科技感十足的图形界面，包含以下主要功能区域：

#### 2.1 系统状态区域
- 显示当前操作系统信息
- 显示Ollama安装状态

#### 2.2 操作按钮区域
- **安装Ollama**：自动检测并安装最新版本的Ollama
- **下载DeepSeek模型**：一键下载官方标准模型 `deepseek:1.5b`
- **更新DeepSeek模型**：将已安装的模型更新到最新版本
- **运行DeepSeek模型**：启动交互式对话界面
- **删除DeepSeek模型**：删除已安装的模型（需确认）

#### 2.3 模型状态区域
- 显示已安装的所有Ollama模型
- 支持手动刷新模型列表

#### 2.4 进度显示区域
- 实时显示安装和下载进度
- 显示当前操作状态

#### 2.5 日志输出区域
- 详细记录所有操作过程
- 支持清空日志

### 3. 安装步骤

1. **启动工具**：运行 `deepseek_installer.py` 脚本
2. **安装Ollama**：点击「安装Ollama」按钮，工具将自动下载并安装适合您系统的Ollama版本
3. **下载模型**：点击「下载DeepSeek模型」按钮，工具将自动下载 `deepseek:1.5b` 模型
4. **运行模型**：点击「运行DeepSeek模型」按钮，启动交互式对话界面
5. **管理模型**：使用「更新DeepSeek模型」和「删除DeepSeek模型」按钮管理已安装的模型

### 4. 模型使用示例

```
正在启动DeepSeek 1.5B模型 (deepseek:1.5b)...
输入 'exit' 退出模型交互
==================================================
>>> 你好
你好！我是一个AI助手，很高兴为你提供帮助。有什么我可以为你解答的问题吗？
>>> 什么是深度学习？
深度学习是机器学习的一个分支，它通过模拟人类大脑的神经网络结构...
>>> exit
已退出模型交互
```

## 配置选项

### 模型保存路径

- **Windows**：`C:\Users\[用户名]\.ollama\models`
- **macOS**：`/Users/[用户名]/.ollama/models`
- **Linux**：`/home/[用户名]/.ollama/models`

### Ollama服务端口

默认端口：`11434`

## 注意事项

1. **网络要求**：安装和下载过程需要稳定的网络连接
2. **权限问题**：macOS/Linux用户可能需要管理员权限
3. **Windows防火墙**：首次运行可能需要允许Ollama访问网络
4. **模型大小**：DeepSeek 1.5B模型约需要2-3GB磁盘空间
5. **硬件加速**：Ollama会自动检测并使用可用的GPU加速

## 常见问题

**Q: 安装Ollama失败怎么办？**
A: 请检查网络连接，或手动访问[Ollama官网](https://ollama.com/)下载安装包

**Q: 模型运行缓慢怎么办？**
A: 1.5B参数模型对硬件要求较低，如仍觉缓慢可尝试关闭其他占用大量内存的程序

**Q: 如何更新模型？**
A: 点击「更新DeepSeek模型」按钮，Ollama会自动更新模型到最新版本

**Q: 如何查看已安装的模型？**
A: 在「模型状态」区域查看，或点击「刷新模型列表」按钮更新

**Q: 如何修改模型保存路径？**
A: 目前工具使用Ollama默认路径，如需修改可通过Ollama命令行工具配置

## 卸载说明

**卸载Ollama**：
- Windows: 通过控制面板或设置应用卸载
- macOS: `rm -rf ~/.ollama`
- Linux: `sudo rm -rf /usr/local/bin/ollama ~/.ollama`

**删除模型**：
- 使用工具中的「删除DeepSeek模型」按钮
- 或通过命令行：`ollama rm deepseek:1.5b`

## 版本信息

- Ollama: 最新版本（自动检测）
- DeepSeek模型: `deepseek:1.5b`（官方标准模型）
- 工具版本: 1.2.0

## 许可证

MIT License