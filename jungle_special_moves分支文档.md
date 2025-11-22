修改总结
1. 添加的函数（在 moves.c 中）
河流检查函数
IsRiverSquare(int row, int col) - 检查指定位置是否为河流
河流区域：行3-5，列1-2（左片）和列4-5（右片）
跳河相关函数
HasRatInRiverPath() - 检查跳河路径中是否有老鼠阻挡
GenerateRiverJump() - 生成狮子和老虎的跳河走法
2. 修改的走法生成函数
StepForward() (moves.c:644-651)
添加河流检查：除老鼠外，其他棋子不能进入河流
StepBackward() (moves.c:654-665)
添加河流检查：除老鼠外，其他棋子不能进入河流
StepSideways() (moves.c:753-785)
添加河流检查：除老鼠外，其他棋子不能进入河流
3. 集成跳河逻辑
老虎（WhiteRook/BlackRook）(moves.c:1328)
在 VariantJungle 中调用 GenerateRiverJump() 生成跳河走法
狮子（WhiteLion/BlackLion）(moves.c:1462)
在 VariantJungle 中调用 GenerateRiverJump() 生成跳河走法
4. 修复编译错误
添加了函数前向声明 (moves.c:639-642)
在使用这些函数之前声明，解决 "static declaration follows non-static declaration" 错误
实现的功能
河流限制：除老鼠外，其他棋子不能进入河流区域
老鼠入河：老鼠可以正常进入河流
狮虎跳河：狮子和老虎可以从河流边缘跳过整片河流
跳河阻挡：跳河路径中有老鼠（无论敌我）则不能跳
跳河落点：可以落在对岸的陆地格子（空格或可吃的敌方棋子）
代码已通过编译检查，可以测试这些功能。


代码逻辑主要有：
创建一个判断一个位置是否为河流的函数】
在原xboard的上下左右移动函数中增加对于河流的检查
只要位于河流且不是老鼠，走棋就不合法

同时：对于老虎和狮子，增加跳河的逻辑，也就是说新添加合法的走棋位置
这是由一个新增的函数实现的。