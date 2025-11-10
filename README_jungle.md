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


图片设置--不需要修改代码，只需要加配置文件和图片资源
char *pngPieceNames[] = // must be in same order as internal piece encoding
{ "Pawn", "Knight", "Bishop", "Rook", "Queen", "Advisor", "Elephant", "Archbishop", "Marshall", "Gold", "Commoner",
"Canon", "Nightrider", "CrownedBishop", "CrownedRook", "Crown", "Chancellor", "Hawk", "Lance", "Cobra", "Unicorn", "Lion",
"Sword", "Zebra", "Camel", "Tower", "Wolf", "Hat", "Duck", "Lance", "Dragon", "Gnu", "Cub",
"LShield", "Pegasus", "Wizard", "Copper", "Iron", "Viking", "Flag", "Axe", "Dolphin", "Leopard", "Claw",
"Left", "Butterfly", "PromoBishop", "PromoRook", "HCrown", "RShield", "Prince", "Phoenix", "Kylin", "Drunk", "Right",
"GoldPawn", "GoldKnight", "PromoHorse", "PromoDragon", "GoldLance", "GoldSilver", "HSword", "PromoSword", "PromoHSword", "Princess", "King",
NULL
};
上面这个定义是draw.c中的，用于与chessSquare进行一一映射，每个ChessSquare类型对应一个字符串，图片命名方式需要按照上面的名称来
White/Black + name.svg为名称即可
themes/jungle/
├── WhiteQueen.svg      # 白象 (E)
├── BlackQueen.svg      # 黑象
├── WhiteLion.svg       # 白狮 (L)
├── BlackLion.svg       # 黑狮
├── WhiteRook.svg       # 白虎 (T)
├── BlackRook.svg       # 黑虎
├── WhiteBishop.svg     # 白豹 (P)
├── BlackBishop.svg     # 黑豹
├── WhiteWolf.svg       # 白狼 (W)
├── BlackWolf.svg       # 黑狼
├── WhiteHawk.svg       # 白狗 (D) - 注意是Hawk不是Falcon
├── BlackHawk.svg       # 黑狗
├── WhiteLeopard.svg    # 白猫 (C) - 注意是Leopard不是Cat
├── BlackLeopard.svg    # 黑猫
├── WhitePawn.svg       # 白鼠 (R)
└── BlackPawn.svg       # 黑鼠

## 走棋逻辑部分开发流程

jungle基础上新建分支jungle_moves
主要文件：moves

feat: 实现斗兽棋(Jungle)基本走棋功能

## 功能概述
在XBoard基础上实现斗兽棋变体，支持基本走棋和吃子功能。

## 主要修改

### 1. 变体定义 (common.h)
- 添加 VariantJungle 枚举
- 支持 -variant jungle 命令行参数

### 2. 棋盘初始化 (backend.c)
- 实现7x9棋盘布局
- 定义8种棋子的起始位置
- 建立棋子与字符的映射关系
    * 鼠(R) → WhitePawn/BlackPawn
    * 猫(C) → WhiteCat/BlackCat
    * 狗(D) → WhiteFalcon/BlackFalcon
    * 狼(W) → WhiteWolf/BlackWolf
    * 豹(P) → WhiteBishop/BlackBishop
    * 虎(T) → WhiteRook/BlackRook
    * 狮(L) → WhiteLion/BlackLion
    * 象(E) → WhiteQueen/BlackQueen

### 3. 走法生成 (moves.c)
- 修复CheckTest：支持无King变体（关键修复）
- 实现所有8种棋子的基本走法（4方向1格）
- 复用Wazir函数实现正交4方向移动
- 支持基本吃子功能

### 关键修复

// moves.c CheckTest函数
if(gameInfo.variant == VariantJungle) {
    return 0;  // 斗兽棋没有King，跳过将军检查
}


### 走法实现
所有棋子都使用Wazir函数（正交4方向1格）：
```c
case WhitePawn:  // 鼠
    if(gameInfo.variant == VariantJungle) {
        Wazir(board, flags, rf, ff, callback, closure);
        break;
    }
```

## 测试验证

已测试功能：
- ✅ 棋盘正确显示（7x9）
- ✅ 棋子正确显示和移动
- ✅ 点击棋子高亮可走位置
- ✅ 所有棋子可以走4个方向
- ✅ 可以吃敌方棋子
- ✅ 不能吃己方棋子
- ✅ 边界检查正常

## 待实现功能

特殊规则（下一阶段）：
- [ ] 大吃小规则
- [ ] 鼠象互吃规则
- [ ] 河流限制（非鼠不能进入）
- [ ] 跳河功能（虎、狮）
- [ ] 陷阱规则
- [ ] 兽穴规则（胜利条件）


启动：
```bash
./xboard -variant jungle -ncp
```
这一阶段修改的内容：
moves.c中的GenPseudoLegal函数中的switch语句中增加各种棋子在variant == VariantJungle情况下的走棋逻辑
初步全部设置为上下左右走一格的走法。


moves.c中的CheckTest 函数，取消斗兽棋对于将军的判断（如果没有这部分无法走棋，因为默认似乎是被将军状态）
增加了一个if语句判断是不是jungle，如果是直接return 0

