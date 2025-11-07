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

现在使用hoichess引擎
指令：
./xboard -fcp hoixiangqi
这会直接打开hoixiangqi的引擎
运行过程中引擎向xboard发送自己的棋类类型，xboard会根据这个类型加载对应的variant文件

## clion中配置xboard项目

- 代码跳转和调试：
  bear make CFLAGS="-fcommon" -j$(nproc)
  以上指令让bear记录make的编译过程
  zhangtx@zhangtx-virtual-machine:~/Xboard/xboard$ ls compile_commands.json
  compile_commands.json

使用以下指令可以让clion进行断点调试：
make CFLAGS="-fcommon -g -O0" VERBOSE=2 -w
-g表示生成调试信息
-O0表示不进行优化
-w表示不显示警告信息


## 运行pikafish

由于pikafish是一个UCI引擎,需要使用协议转换器转换成xboard使用的协议
目前使用指令：

./xboard -variant xiangqi -fcp "uci2wb /home/zhangtx/Xboard/xboard/pikafish/src/pikafish /home/zhangtx/Xboard/xboard/pikafish/src"

可以成功在xboard中运行pikafish引擎
可以和pikafish下棋

//之前使用polyglot无法正确转换协议，应该使用uci2wb

uciwb的使用方法：
usage is: UCI2WB [debug] [-s] <engine.exe> [<engine directory>]


## xboard结构

### xaw与gtk目录

这是两个不同的图形界面前端，当前程序使用的是gtk前端（因为只编译了gtk）
xboard支持多种前端，属于同一后端逻辑对应多种前端界面
这两个目录下的文件内容大体相同

以gtk目录为例：
xboard.c是函数的入口，main函数在这里


## 如何仅仅显示棋盘？
如果直接使用./xboard -variant <name>启动，xboard会在系统目录自己找到默认的路径下的一个引擎启动
但是这个引擎通常是国际象棋引擎，当输入./xboard -variant xiangqi 会报错说fairy-max5.0(国际象棋引擎名称)不支持xiangqi

此时在后面加上 -ncp就可以
./xboard -variant xiangqi -ncp
表示只显示棋盘no chess program



