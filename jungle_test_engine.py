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

    def is_river_square(self, rank, file):
        """检查是否是河流格子"""
        # 河流区域：行3-5（索引），列1-2和4-5
        if 3 <= rank <= 5:
            if 1 <= file <= 2 or 4 <= file <= 5:
                return True
        return False

    def is_trap_square(self, rank, file, side):
        """检查是否是陷阱格子
        side: 'white' 或 'black'
        陷阱在对方兽穴相邻的三个格子上（前方及左右方）
        白方兽穴在(0,3)，陷阱在(1,2), (1,3), (1,4)
        黑方兽穴在(8,3)，陷阱在(7,2), (7,3), (7,4)
        """
        if side == 'white':
            # 白方陷阱在行1，列2,3,4
            if rank == 1 and 2 <= file <= 4:
                return True
        else:
            # 黑方陷阱在行7，列2,3,4
            if rank == 7 and 2 <= file <= 4:
                return True
        return False

    def is_den_square(self, rank, file, side):
        """检查是否是兽穴格子"""
        if side == 'white':
            return rank == 0 and file == 3
        else:
            return rank == 8 and file == 3

    def get_piece_rank(self, piece):
        """获取棋子等级
        象(8) > 狮(7) > 虎(6) > 豹(5) > 狼(4) > 狗(3) > 猫(2) > 鼠(1)
        """
        piece_map = {
            'Q': 8, 'q': 8,  # 象 (Queen/Elephant)
            'L': 7, 'l': 7,  # 狮 (Lion)
            'R': 6, 'r': 6,  # 虎 (Rook/Tiger)
            'B': 5, 'b': 5,  # 豹 (Bishop/Panther)
            'N': 4, 'n': 4,  # 狼 (Knight/Wolf)
            'D': 3, 'd': 3,  # 狗 (Falcon/Dog)
            'C': 2, 'c': 2,  # 猫 (Cat)
            'P': 1, 'p': 1,  # 鼠 (Pawn/Rat)
        }
        return piece_map.get(piece, 0)

    def can_capture(self, attacker, defender, attacker_rank, attacker_file, defender_rank, defender_file, side):
        """检查是否可以吃子
        - 基本规则：大吃小
        - 特殊规则：老鼠可以吃大象，但大象不能吃老鼠
        - 陷阱效果：进入敌方陷阱的棋子可以被任何敌方棋子吃掉
        - 水战限制：陆地上的棋子不能吃水中的棋子（除鼠外），水中的鼠不能吃岸上的象
        """
        attacker_rank_val = self.get_piece_rank(attacker)
        defender_rank_val = self.get_piece_rank(defender)
        
        attacker_in_river = self.is_river_square(attacker_rank, attacker_file)
        defender_in_river = self.is_river_square(defender_rank, defender_file)
        
        # 水战限制：陆地上的棋子不能吃水中的棋子（除鼠外）
        if not attacker_in_river and defender_in_river:
            if attacker not in ['P', 'p']:  # 不是老鼠
                return False
        
        # 水战限制：水中的鼠不能吃岸上的象
        if attacker_in_river and attacker in ['P', 'p'] and not defender_in_river:
            if defender_rank_val == 8:  # 大象
                return False
        
        # 检查陷阱效果：如果防守方在敌方陷阱中，可以被任何棋子吃掉
        if self.is_trap_square(defender_rank, defender_file, 'black' if side == 'white' else 'white'):
            return True
        
        # 特殊规则：老鼠可以吃大象
        if attacker_rank_val == 1 and defender_rank_val == 8:
            return True
        
        # 特殊规则：大象不能吃老鼠
        if attacker_rank_val == 8 and defender_rank_val == 1:
            return False
        
        # 基本规则：大吃小（包括同级）
        return attacker_rank_val >= defender_rank_val

    def has_rat_in_river_path(self, from_rank, from_file, to_rank, to_file):
        """检查跳河路径中是否有老鼠阻挡"""
        dr = 1 if to_rank > from_rank else (-1 if to_rank < from_rank else 0)
        df = 1 if to_file > from_file else (-1 if to_file < from_file else 0)
        
        rank = from_rank + dr
        file = from_file + df
        
        while self.is_river_square(rank, file):
            piece = self.board[rank][file]
            if piece in ['P', 'p']:  # 有老鼠阻挡
                return True
            rank += dr
            file += df
            if not (0 <= rank < 9 and 0 <= file < 7):
                break
        return False

    def generate_river_jump_moves(self, rank, file, piece, side):
        """生成狮子和老虎的跳河走法"""
        moves = []
        
        # 只有狮子和老虎可以跳河
        if piece not in ['L', 'l', 'R', 'r']:
            return moves
        
        # 不能在河流中跳河
        if self.is_river_square(rank, file):
            return moves
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
        
        for dr, df in directions:
            next_rank = rank + dr
            next_file = file + df
            
            # 检查相邻格子是否是河流
            if not (0 <= next_rank < 9 and 0 <= next_file < 7):
                continue
            if not self.is_river_square(next_rank, next_file):
                continue
            
            # 沿着这个方向找到河流对岸的陆地格子
            to_rank = next_rank
            to_file = next_file
            while self.is_river_square(to_rank, to_file):
                to_rank += dr
                to_file += df
                if not (0 <= to_rank < 9 and 0 <= to_file < 7):
                    break
            
            # 如果找到了对岸的陆地格子
            if 0 <= to_rank < 9 and 0 <= to_file < 7 and not self.is_river_square(to_rank, to_file):
                # 检查路径中是否有老鼠阻挡
                if self.has_rat_in_river_path(rank, file, to_rank, to_file):
                    continue
                
                target = self.board[to_rank][to_file]
                
                # 不能跳到己方棋子
                if target:
                    if side == 'white' and self.is_white_piece(target):
                        continue
                    if side == 'black' and self.is_black_piece(target):
                        continue
                    
                    # 检查是否可以吃子
                    if not self.can_capture(piece, target, rank, file, to_rank, to_file, side):
                        continue
                
                # 不能进入己方兽穴
                if self.is_den_square(to_rank, to_file, side):
                    continue
                
                from_square = chr(ord('a') + file) + str(rank + 1)
                to_square = chr(ord('a') + to_file) + str(to_rank + 1)
                move = from_square + to_square
                moves.append(move)
        
        return moves

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

                # 生成基本移动（上下左右一格）
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
                        
                        # 检查是否可以吃子
                        if not self.can_capture(piece, target, rank, file, new_rank, new_file, self.side_to_move):
                            continue

                    # 河流限制：除了老鼠外，其他棋子不能进入河流
                    if self.is_river_square(new_rank, new_file):
                        if piece not in ['P', 'p']:  # 不是老鼠
                            continue

                    # 不能进入己方兽穴
                    if self.is_den_square(new_rank, new_file, self.side_to_move):
                        continue

                    # 构造走法字符串
                    from_square = chr(ord('a') + file) + str(rank + 1)
                    to_square = chr(ord('a') + new_file) + str(new_rank + 1)
                    move = from_square + to_square
                    moves.append(move)

                # 生成跳河走法（狮子和老虎）
                river_jump_moves = self.generate_river_jump_moves(rank, file, piece, self.side_to_move)
                moves.extend(river_jump_moves)

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

