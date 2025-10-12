this file is my log

# 基于xboard的斗兽棋前端开发日志

## xboard的编译


sudo apt install -y libgtk2.0-dev

sudo apt install -y libcairo2-dev libpango1.0-dev librsvg2-dev pkg-config
sudo apt install -y libgtk-3-dev
sudo apt install texinfo//其中包含makeinfo

- INSTALL文件直接执行遇到困难
需要安装不少的依赖工具（）

首先执行./autogen.sh
安装configure相关的文件

- 之后./configure安装配置

如果成功，应该会看到source下有Makefile
之后 make

- make遇到问题：

由于代码过于古老，在现代编译器下有些写法会报错
报错信息大概如下：ics_type被重复定义
因为许多文件include同一个文件
这个文件中定义了ics_type
引用的文件又重新定义了一遍

解决方法：
make CFLAGS="-fcommon"
这个指令指定使用旧版本的编译规则，可以编译成功

- 编译成功之后执行./xboard
可能有报错，我在执行之后只能看见空白的棋盘，这是因为没有下载棋子图像资源。

sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
//安装声音资源


sudo make install 安装棋子图像等资源
执行之后会将资源安装到/usr/local/bin/

- 运行xboard出现报错
因为没有设置象棋引擎，只有前端界面导致的

 sudo apt install fairymax gnuchess

安装以上象棋引擎就可以正常使用

///
在我执行sudo make install之后发现我/usr/local/bin/xboard
这个目录下有xboard的可执行文件

这个其实就是我自己的源代码编译出来之后脚本复制了一份到这里，之后可以直接通过xboard打开这个项目了。

## variant编写。

首先需要安装象棋的引擎
安装eleeye引擎（手动编译）

sudo apt install git build-essential
git clone https://github.com/xqbase/eleeye.git
cd eleeye/src








