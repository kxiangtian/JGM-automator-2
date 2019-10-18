# JGM-automator
> 原 <家国梦> [JGM-automator ](https://github.com/Jiahonzheng/JGM-Automator "<JGM-automator>")自动化脚本的改写

## 计划
- [ ] GUI 显示信息 和 配置勾选
- [x] 转换基本配置文件
- [x] 改写收取金币 (Android)
- [x] 适配收取金币 (IOS)
- [x] 改写安卓移动物品
- [ ] IOS根据对比物品来判断位置

## 功能
- [x] Print out Information Every n times

### Android
- [x] 自动收金币
- [x] 自动收货

### IOS
- [x] 自动收金币
- [ ] 自动收货


## 安装与运行

### Mac
```bash
brew update
brew install python3
brew install tesseract
brew cask install android-platform-tools
brew install --HEAD usbmuxd
brew install --HEAD libimobiledevice
```
### Windows
- [Python3.7.4](https://www.python.org/downloads/release/python-374/)
- ADB 请将本项目下adb文件夹路径添加到环境变量的 `Path`
- [tesseract](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows)
- 出现Emulator-5554输入一下找到5554+1(5555)端口的pid 结束进程
```powershell
netstat –ano
kill pid 
```

### IOS + MacOS

#### 环境安装

- 使用真机调试 WDA，参考 iOS 真机如何安装 [WebDriverAgent · TesterHome](https://testerhome.com/topics/7220)
- 安装 [openatx/facebook-wda](https://github.com/openatx/facebook-wda)

### 安装python的库
```bash
python -m pip install -r requirements.txt
```
### 运行
- 使用 MuMu 模拟器，请先 adb 连接 MuMu 模拟器。
```bash
adb connect 127.0.0.1:7555
```
- 获取 device 名称 填写至config.json. 如果是 MuMu 模拟器在Main 部分 MUMU为 True
```bash
adb devices
"""
device: 如果是 USB 连接，则为 adb devices 的返回结果；
如果是模拟器，则为模拟器的控制 URL 。
"""
```
- 在已完成 adb 连接后，在手机安装 ATX 应用。
```bash
python -m uiautomator2 init
```
- 在手机上打开 ATX ，点击 `启动 UIAutomator` 选项，确保 UIAutomator 是运行的。如果是 MuMu 模拟器，长时间不运行的话，再次运行前也需要重新打开ATX(小黄车)。

### 如何运行这个脚本:
```bash
# IOS 可以用下面的映射USB端口
iproxy 8100 8100
# 在该项目的文件夹根目录打开
python main.py
```

+ 能动就说明能成功运行，接下来你可以退出脚本(`Ctrl`+`C` 或者 关掉终端窗口)，在 `main.py` 中修改你的配置。

### IOS屏幕比例信息
<img src="https://github.com/openatx/facebook-wda/raw/master/images/ios-display.png" style="zoom:40%" />

## Log
### 10/17
- pytesseract 中文识别效果并不好 中文改换成百度ORC

## Contributors
[jiahonzheng](https://github.com/Jiahonzheng/)

