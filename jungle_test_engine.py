#!/usr/bin/env python3
"""
斗兽棋测试引擎 - 用于测试XBoard协议通信
功能：随机走棋，验证XBoard与引擎的通信是否正常
"""

import sys
import random

class JungleTestEngine:
    def __init__(self):
        self.board = self.init_board()
        self.variant = "normal"
        self.force_mode = False
        self.my_color = None
        self.side_to_move = 'white'  # 白方先走

    def init_board(self):
        """初始化斗兽棋棋盘 - 7x9棋盘"""
        # 创建空棋盘
        board = [[None for _ in range(7)] for _ in range(9)]

        # 白方棋子（底部，行0-2）
        # 行0: 虎(a1) 狮(g1)
        board[0][0] = 'R'  # 虎 (Rook/Tiger)
        board[0][6] = 'L'  # 狮 (Lion)

        # 行1: 狗(b2) 猫(f2)
        board[1][1] = 'D'  # 狗 (Dog)
        board[1][5] = 'C'  # 猫 (Cat)

        # 行2: 鼠(a3) 豹(c3) 狼(e3) 象(g3)
        board[2][0] = 'P'  # 鼠 (Pawn/Rat)
        board[2][2] = 'B'  # 豹 (Bishop/Leopard)
        board[2][4] = 'N'  # 狼 (Knight/Wolf)
        board[2][6] = 'Q'  # 象 (Queen/Elephant)

        # 黑方棋子（顶部，行6-8）- 镜像对称
        # 行6: 象(a7) 狼(c7) 豹(e7) 鼠(g7)
        board[6][0] = 'q'  # 象
        board[6][2] = 'n'  # 狼
        board[6][4] = 'b'  # 豹
        board[6][6] = 'p'  # 鼠

        # 行7: 猫(b8) 狗(f8)
        board[7][1] = 'c'  # 猫
        board[7][5] = 'd'  # 狗

        # 行8: 狮(a9) 虎(g9)
        board[8][0] = 'l'  # 狮
        board[8][6] = 'r'  # 虎

        return board

    def log(self, message):
        """输出调试信息（以#开头，XBoard会忽略）"""
        print(f"# {message}", flush=True)

    def send_command(self, command):
        """发送命令给XBoard"""
        print(command, flush=True)
        self.log(f"Sent: {command}")

    def handle_xboard(self):
        """处理xboard命令"""
        self.log("XBoard protocol activated")

    def handle_protover(self, version):
        """处理protover命令"""
        self.log(f"Protocol version: {version}")
        # 发送引擎特性
        self.send_command("feature done=0")
        self.send_command('feature myname="JungleTestEngine v1.0"')
        self.send_command('feature variants="jungle"')  # 声明支持jungle
        self.send_command("feature boardsize=1")  # 支持任意棋盘大小（备用）
        self.send_command("feature setboard=1")
        self.send_command("feature usermove=1")
        self.send_command("feature ping=1")
        self.send_command("feature sigint=0")
        self.send_command("feature sigterm=0")
        self.send_command("feature reuse=1")
        self.send_command("feature done=1")

    def handle_new(self):
        """处理new命令 - 开始新游戏"""
        self.log("New game started")
        self.board = self.init_board()
        self.force_mode = False
        self.my_color = None
        self.side_to_move = 'white'

    def handle_variant(self, variant):
        """处理variant命令"""
        self.variant = variant
        self.log(f"Variant set to: {variant}")
        if variant == "jungle":
            self.board = self.init_board()

    def handle_force(self):
        """处理force命令 - 进入force模式"""
        self.force_mode = True
        self.log("Force mode activated")

    def handle_go(self):
        """处理go命令 - 开始思考"""
        self.force_mode = False
        self.log("Starting to think...")
        self.make_move()

    def handle_move(self, move):
        """处理对方的走法"""
        self.log(f"Opponent move: {move}")

        # 应用对方的走法到棋盘
        if len(move) >= 4:
            from_file = ord(move[0]) - ord('a')
            from_rank = int(move[1]) - 1
            to_file = ord(move[2]) - ord('a')
            to_rank = int(move[3]) - 1

            # 更新棋盘
            if 0 <= from_rank < 9 and 0 <= from_file < 7:
                piece = self.board[from_rank][from_file]
                self.board[from_rank][from_file] = None
                if 0 <= to_rank < 9 and 0 <= to_file < 7:
                    self.board[to_rank][to_file] = piece

            # 切换走棋方
            self.side_to_move = 'black' if self.side_to_move == 'white' else 'white'

        if not self.force_mode:
            # 如果不在force模式，自动回应
            self.make_move()

    def handle_quit(self):
        """处理quit命令"""
        self.log("Quitting...")
        sys.exit(0)

    def handle_ping(self, n):
        """处理ping命令"""
        self.send_command(f"pong {n}")

    def handle_boardsize(self, width, height):
        """处理boardsize命令"""
        self.log(f"Board size set to: {width}x{height}")
        # 斗兽棋应该是7x9
        if width != 7 or height != 9:
            self.log(f"Warning: Expected 7x9, got {width}x{height}")

    def handle_result(self, result_str):
        """处理result命令 - 游戏结束"""
        self.log(f"Game ended: {result_str}")

    def make_move(self):
        """生成并发送走法"""
        # 简化版：随机生成一个看起来合法的走法
        # 实际引擎需要：
        # 1. 生成所有合法走法
        # 2. 评估局面
        # 3. 选择最佳走法

        move = self.generate_random_move()
        if move:
            self.send_command(f"move {move}")
        else:
            self.log("No legal moves available")
            self.send_command("resign")

    def is_white_piece(self, piece):
        """判断是否是白方棋子"""
        return piece and piece.isupper()

    def is_black_piece(self, piece):
        """判断是否是黑方棋子"""
        return piece and piece.islower()

    def generate_legal_moves(self):
        """生成所有合法走法"""
        moves = []

        for rank in range(9):
            for file in range(7):
                piece = self.board[rank][file]
                if piece is None:
                    continue

                # 检查是否是当前走棋方的棋子
                if self.side_to_move == 'white' and not self.is_white_piece(piece):
                    continue
                if self.side_to_move == 'black' and not self.is_black_piece(piece):
                    continue

                # 生成该棋子的所有可能走法
                # 简化版：只考虑上下左右移动一格
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for dr, df in directions:
                    new_rank = rank + dr
                    new_file = file + df

                    # 检查是否在棋盘内
                    if not (0 <= new_rank < 9 and 0 <= new_file < 7):
                        continue

                    target = self.board[new_rank][new_file]

                    # 不能吃自己的棋子
                    if target:
                        if self.side_to_move == 'white' and self.is_white_piece(target):
                            continue
                        if self.side_to_move == 'black' and self.is_black_piece(target):
                            continue

                    # 构造走法字符串
                    from_square = chr(ord('a') + file) + str(rank + 1)
                    to_square = chr(ord('a') + new_file) + str(new_rank + 1)
                    move = from_square + to_square
                    moves.append(move)

        return moves

    def generate_random_move(self):
        """生成一个合法的随机走法"""
        legal_moves = self.generate_legal_moves()

        if not legal_moves:
            self.log("No legal moves available!")
            return None

        # 随机选择一个合法走法
        move = random.choice(legal_moves)
        self.log(f"Generated move: {move} (from {len(legal_moves)} legal moves)")

        # 应用走法到棋盘
        if len(move) >= 4:
            from_file = ord(move[0]) - ord('a')
            from_rank = int(move[1]) - 1
            to_file = ord(move[2]) - ord('a')
            to_rank = int(move[3]) - 1

            piece = self.board[from_rank][from_file]
            self.board[from_rank][from_file] = None
            self.board[to_rank][to_file] = piece

            # 切换走棋方
            self.side_to_move = 'black' if self.side_to_move == 'white' else 'white'

        return move

    def run(self):
        """主循环 - 读取命令并处理"""
        self.log("JungleTestEngine started")
        self.log("Waiting for commands...")

        while True:
            try:
                line = input().strip()
                if not line:
                    continue

                self.log(f"Received: {line}")

                # 解析命令
                parts = line.split()
                command = parts[0]

                if command == "xboard":
                    self.handle_xboard()

                elif command == "protover":
                    version = int(parts[1]) if len(parts) > 1 else 1
                    self.handle_protover(version)

                elif command == "new":
                    self.handle_new()

                elif command == "variant":
                    variant = parts[1] if len(parts) > 1 else "normal"
                    self.handle_variant(variant)

                elif command == "force":
                    self.handle_force()

                elif command == "go":
                    self.handle_go()

                elif command == "quit":
                    self.handle_quit()

                elif command == "ping":
                    n = parts[1] if len(parts) > 1 else "1"
                    self.handle_ping(n)

                elif command == "usermove":
                    # usermove e2e4
                    move = parts[1] if len(parts) > 1 else ""
                    self.handle_move(move)

                elif command == "boardsize":
                    # boardsize 7 9
                    width = int(parts[1]) if len(parts) > 1 else 7
                    height = int(parts[2]) if len(parts) > 2 else 9
                    self.handle_boardsize(width, height)

                elif command == "result":
                    # result 1-0 {White wins}
                    result_str = ' '.join(parts[1:])
                    self.handle_result(result_str)

                elif len(command) >= 4 and command[0] in 'abcdefg' and command[1] in '123456789':
                    # 直接的走法：e2e4
                    self.handle_move(command)

                else:
                    self.log(f"Unknown command: {command}")

            except EOFError:
                self.log("EOF received, quitting...")
                break
            except Exception as e:
                self.log(f"Error: {e}")

if __name__ == "__main__":
    engine = JungleTestEngine()
    engine.run()

