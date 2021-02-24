# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:51:57 2021

@author: 44797
"""
import numpy as np

class RandomAgent():
    def __init__(self):
        self.possible_moves = []
        
    
    def get_actions(self, state):
        all_actions = []
        for j in range(3):
            for i in range(3):
                all_actions.append((j,i))
                
        self.possible_moves = [g for g in all_actions if state[g[0]][g[1]] == ' ']
        
    
    def move(self):
        possible_move_index = np.linspace(0, len(self.possible_moves)-1, len(self.possible_moves))
        this_one = int(np.random.choice(possible_move_index))
        move_to_make = self.possible_moves[this_one]
        
        return move_to_make
    
class QAgent():
    def __init__(self, q_table):
        self.alpha = 0.9
        self.gamma = 1
        self.eps = 0.01
        self.q_table = q_table
        self.current_state = None
        self.current_action = None
        self.next_state = None
        self.all_actions = []
        self.ticker = ''
        
    def win_check(self):
        
        diag_1 = [self.next_state[0][0], self.next_state[1][1], self.next_state[2][2]]
        diag_2 = [self.next_state[0][2], self.next_state[1][1], self.next_state[2][0]]
        
        
        if diag_1.count('o') == 3 or diag_2.count('o') == 3:
            self.ticker = 'o'
            return True
        
        elif diag_1.count('x') == 3 or diag_2.count('x') == 3:
            self.ticker = 'x'
            return True
        
        for i in range(3):
            rows = [self.next_state[i][0], self.next_state[i][1], self.next_state[i][2]]
            cols = [self.next_state[0][i], self.next_state[1][i], self.next_state[2][i]]
        
            if cols.count('o') == 3 or rows.count('o') == 3:
                self.ticker = 'o'
                return True
            
            elif cols.count('x') == 3 or rows.count('x') == 3:
                self.ticker = 'x'
                return True
        
        return False
    
    def draw_check(self):
        for row in self.next_state:
            for box in row:
                if box == ' ':
                    return False
        return True
    
    def check_end_state(self):
        if self.win_check():
            if self.ticker == 'o':
                return 1
            else:
                return -1
            
        else:
            return 0
      
    def get_actions(self, state):
        
        for j in range(3):
            for i in range(3):
                self.all_actions.append((j,i))
                
        self.possible_moves = [g for g in self.all_actions if state[g[0]][g[1]] == ' ']

        
    def move(self, state):
        tuple_state = [tuple(row) for row in state]
        if tuple(tuple_state) not in self.q_table:
            self.q_table[tuple(tuple_state)] = {}
            
        for i in self.possible_moves:
            if i not in self.q_table[tuple(tuple_state)]:
                self.q_table[tuple(tuple_state)][i] = 0
            
        if np.random.uniform(0, 1) < self.eps:
            possible_move_index = np.linspace(0, len(self.possible_moves)-1, len(self.possible_moves))
            this_one = int(np.random.choice(possible_move_index))
            move_to_make = self.possible_moves[this_one]
            self.current_action = move_to_make
        else:
            q_values = [self.q_table[tuple(tuple_state)][move] for move in self.possible_moves]
            best_moves_index = np.argwhere(q_values == np.amax(q_values))
            best_move_index = np.random.choice(best_moves_index.flatten())
            move_to_make = self.possible_moves[best_move_index]
            self.current_action = move_to_make

        self.current_state = state
        self.update_q()
        
        return move_to_make
    
    def update_q(self):
        
        current_tuple_state = [tuple(row) for row in self.current_state]
        self.current_state[self.current_action[0]][self.current_action[1]] = 'o'
        self.next_state = self.current_state
        next_tuple_state = [tuple(row) for row in self.next_state]
        if tuple(next_tuple_state) not in self.q_table:
            self.q_table[tuple(next_tuple_state)] = {}
            
        for i in self.all_actions:
            if i not in self.q_table[tuple(next_tuple_state)]:
                self.q_table[tuple(next_tuple_state)][i] = 0
                
        reward = 0
        if self.win_check():
            reward = self.check_end_state()
            
        possible_q_values  = [self.q_table[tuple(next_tuple_state)][move] for move in self.all_actions]
        if len(possible_q_values) > 0:
            self.q_table[tuple(current_tuple_state)][self.current_action] += self.alpha * (reward + (self.gamma * max(possible_q_values)) - self.q_table[tuple(current_tuple_state)][self.current_action])       
        else:
            self.q_table[tuple(current_tuple_state)][self.current_action] += self.alpha * (reward - self.q_table[tuple(current_tuple_state)][self.current_action])  
        
    def get_q_table(self):
        return self.q_table
    
    def next_state(self):
        return self.next_state
        
class TicTacToe():
    def __init__(self, player1, player2):        
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.player1 = player1
        self.player2 = player2
        self.ticker = ''
        
        
    def reset(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        
        return self.board
    
    def game_move(self, action, ticker):
        self.board[action[0]][action[1]] = ticker
    

    def win_check(self):
        
        diag_1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        diag_2 = [self.board[0][2], self.board[1][1], self.board[2][0]]
        
        
        if diag_1.count(self.ticker) == 3 or diag_2.count(self.ticker) == 3:
            return True
        
        for i in range(3):
            rows = [self.board[i][0], self.board[i][1], self.board[i][2]]
            cols = [self.board[0][i], self.board[1][i], self.board[2][i]]
        
            if cols.count(self.ticker) == 3 or rows.count(self.ticker) == 3:
                return True
        
        return False
    
    def draw_check(self):
        for row in self.board:
            for box in row:
                if box == ' ':
                    return False
        return True
    
    def check_end_state(self):
        if self.win_check():
            if self.ticker == 'o':
                return 1
            else:
                return -1
            
        else:
            return 0
        
    def print_board(self):
        for x in self.board:
             print(x[0] + '|' + x[1] + '|' + x[2])
             
    def state(board):     
        tracker = ' ' 
        for row in board:
            for box in row:
                tracker += box 
                
        return tracker
    
    def play(self):
        self.board = self.reset()
        num = np.random.uniform(0,1)
        
        while True:
            if num < 0.5:
                if self.win_check() or self.draw_check():
                    return self.check_end_state()
                
                self.player1.get_actions(self.board)
                self.game_move(self.player1.move(), 'x')
                self.ticker = 'x'
                
                if self.win_check() or self.draw_check():
                    return self.check_end_state()
                
                self.player2.get_actions(self.board)
                pos = self.player2.move(self.board)
                self.game_move(pos, 'o')
                self.ticker = 'o'
                
            else:
                if self.win_check() or self.draw_check():
                    return self.check_end_state()
                
                self.player2.get_actions(self.board)
                pos = self.player2.move(self.board)
                self.game_move(pos, 'o')
                self.ticker = 'o'
                
                if self.win_check() or self.draw_check():
                    return self.check_end_state()
                
                self.player1.get_actions(self.board)
                self.game_move(self.player1.move(), 'x')
                self.ticker = 'x'
            
            
        
                          
q_table = {}
reward_track = []

for i in range(20000):
    
    test_player1 = RandomAgent()
    test_player2 = QAgent(q_table)
    
    game = TicTacToe(test_player1, test_player2)
    q_table = test_player2.get_q_table()
    reward = game.play()
    reward_track.append(reward)
    

import matplotlib.pyplot as plt

cum_sum = np.cumsum(reward_track)
average_every_n = np.mean(np.array(reward_track).reshape(-1, 20), axis=1)
plt.plot(average_every_n)
plt.plot(cum_sum)