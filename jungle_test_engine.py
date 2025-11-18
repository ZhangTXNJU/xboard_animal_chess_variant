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
        
    def init_board(self):
        """初始化斗兽棋棋盘"""
        # 简化版：只记录棋子位置
        return {
            # 白方
            (0, 0): 'T', (0, 6): 'L',
            (1, 1): 'C', (1, 5): 'D',
            (2, 0): 'E', (2, 2): 'W', (2, 4): 'P', (2, 6): 'R',
            # 黑方
            (6, 0): 'r', (6, 2): 'p', (6, 4): 'w', (6, 6): 'e',
            (7, 1): 'd', (7, 5): 'c',
            (8, 0): 'l', (8, 6): 't',
        }
    
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
        self.send_command('feature myname="JungleTestEngine"')
        self.send_command('feature variants="normal,jungle"')
        self.send_command("feature setboard=1")
        self.send_command("feature usermove=1")
        self.send_command("feature ping=1")
        self.send_command("feature done=1")
    
    def handle_new(self):
        """处理new命令 - 开始新游戏"""
        self.log("New game started")
        self.board = self.init_board()
        self.force_mode = False
        self.my_color = None
    
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
        # 简化：不验证走法合法性，直接更新棋盘
        # 实际引擎需要验证并更新棋盘状态
        
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
    
    def generate_random_move(self):
        """生成随机走法（仅用于测试）"""
        # 简化版：生成一个随机的坐标走法
        # 格式：e2e4 (列用a-g，行用1-9)
        
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        # 随机选择起点和终点
        from_file = random.choice(files)
        from_rank = random.choice(ranks)
        to_file = random.choice(files)
        to_rank = random.choice(ranks)
        
        move = f"{from_file}{from_rank}{to_file}{to_rank}"
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

