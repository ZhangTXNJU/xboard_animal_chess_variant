# xboard基础上的斗兽棋variant开发

## 目标
在xboard基础上实现斗兽棋功能。
xboard是一个象棋类游戏的图形化前端界面，支持多种变体（比如中国象棋，日本将棋等等）
该项目需要在xboard的基础上，修改代码增加jungle variant
要求：能够链接后端引擎，与斗兽棋引擎交互，正确展示斗兽棋棋盘和棋子。支持人机对战

## 项目结构

程序入口：gtk/xboard.c
中的main函数

主要代码逻辑(variant相关)：
backend.c：
board.c
moves.c

结构体和变量的定义：
common.h

conf目录下有一些棋类的配置信息，目前还不清楚程序如何解析这些配置。

pikafish目录是我自己增加的象棋引擎，暂时不需要修改

还有一些目录用于存放程序需要的图片
themes/ 存放一些variant的图片，比如象棋的棋子图片
pixmaps/
png/
也是图片目录

目前已经理解整个项目的架构，了解核心代码框架和原理
variant定义，初始化，棋子和字符串，图片的映射关系等等，尚未修改代码，只是增加了一些注释

当前目标：完成斗兽棋variant基础代码框架的搭建，我希望能够以斗兽棋的格局打开xboard（在启动指令中指定variant为斗兽棋，打开一个9*7的棋盘）

斗兽棋variant的开发可以参考xiangqi

单元测试和开发方式：每天写完当天的代码进行代码测试，保证代码准确性。

- 
添加斗兽棋的在common.h中的定义
新VariantJungle
对应名称jungle

backend.c中增加斗兽棋的初始化代码


## 棋子类型映射规则
ELEPHANT = E

LION     = L

TIGER    = T

PANTHER  = P

WOLF     = W

DOG      = D

CAT      = C

RAT      = R



E → WhiteQueen

L → WhiteLion

T → WhiteRook

P → WhiteBishop

W → WhiteWolf

D → WhiteFalcon

C → WhiteCat

R → WhitePawn

## 会议结论：关于如何修改

需要保证及时测试
因此：先修改上层的函数，再修改相对底层的部分
目前需要完成能够让xboard以jungle 的variant启动的上层部分
包括parser解析参数，能够让xboard选择variant斗兽棋

