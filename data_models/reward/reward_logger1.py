# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 18:12:49 2019

@author: 2427060M
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:25:27 2019

@author: 2427060M
"""

from statistics import mean

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import deque
import os
import csv
import numpy as np
#%%

REWARD_PNG_PATH = "./reward/reward.png"
#POSITION_CSV_PATH = "./reward/position.csv"
SOLVED_CSV_PATH = "./reward/solved.csv"
SOLVED_PNG_PATH = "./reward/solved.png"
AVERAGE_SCORE_TO_SOLVE = 200
CONSECUTIVE_RUNS_TO_SOLVE = 100


class RewardLogger:


    def __init__(self, env_name, reward_path, estimate_path ,position_path):
        #self.reward = deque(maxlen=CONSECUTIVE_RUNS_TO_SOLVE)
        self.reward = deque(maxlen=10000000000)
        self.r_estimate=deque(maxlen=10000000000)
        self.rv_estimate=deque(maxlen=10000000000)
        self.v_estimate=deque(maxlen=10000000000)
        self.env_name = env_name
        self.REWARD_CSV_PATH, self.POSITION_CSV_PATH  = reward_path, position_path
        self.ESTIMATE_CSV_PATH = estimate_path
        if os.path.exists(REWARD_PNG_PATH):
            os.remove(REWARD_PNG_PATH)
        if os.path.exists(self.REWARD_CSV_PATH):
            os.remove(self.REWARD_CSV_PATH)
        if os.path.exists(self.ESTIMATE_CSV_PATH):
            os.remove(self.ESTIMATE_CSV_PATH)
        if os.path.exists(self.POSITION_CSV_PATH):
            os.remove(self.POSITION_CSV_PATH)
    def add_reward(self, reward, run,episode):
        self._save_csv(self.REWARD_CSV_PATH, reward,run)

        self.reward.append(reward)
        self.r_estimate.append(mean(self.reward))

        if len(self.reward) % 400==0 :
            mean_reward = mean(self.reward)
            print ("Scores: (min: " + str(min(self.reward)) + ", avg: " + str(mean_reward) + ", max: " + str(max(self.reward)) + ")\n")
            mean_plot=np.ones(len(self.reward))*mean_reward
            plt.figure(figsize=(12,6)) 
            plt.plot(range(len(self.reward)),self.reward,'b')
#            plt.plot(range(len(mean_plot)),mean_plot,'r')
            plt.plot(range(len(self.r_estimate)),self.r_estimate,'r')
            plt.xlabel('Episode')
            plt.ylabel('Reward')
            plt.show()
            
    def add_estimation(self, v_estimate, run,episode):
        self._save_csv(self.ESTIMATE_CSV_PATH, v_estimate,run)

        self.v_estimate.append(v_estimate)
        self.rv_estimate.append(mean(self.v_estimate))
            
        if len(self.v_estimate) % 450==0 :
            mean_v_estimate = mean(self.v_estimate)
            print ("Scores: (min: " + str(min(self.v_estimate)) + ", avg: " + str(mean_v_estimate) + ", max: " + str(max(self.v_estimate)) + ")\n")
#            mean_plot=np.ones(len(self.reward))*mean_reward
            plt.figure(figsize=(12,6)) 
            plt.plot(range(len(self.v_estimate)),self.v_estimate,'b')
#            plt.plot(range(len(mean_plot)),mean_plot,'r')
            plt.plot(range(len(self.rv_estimate)),self.rv_estimate,'r')
            plt.xlabel('Episode')
            plt.ylabel('Value Estimate')
            plt.show()
        
#        if len(self.reward) >= CONSECUTIVE_RUNS_TO_SOLVE:
#            solve_reward = run-CONSECUTIVE_RUNS_TO_SOLVE
#            print ("Solved in " + str(solve_reward) + " runs, " + str(run) + " total runs.")
#            self._save_csv(SOLVED_CSV_PATH, solve_reward, run)
##            self._save_png(input_path=SOLVED_CSV_PATH,
#                           output_path=SOLVED_PNG_PATH,
#                           x_label="trials",
#                           y_label="steps before solve",
#                           average_of_n_last=None,
#                           show_goal=False,
#                           show_trend=False,
#                           show_legend=False)
#            exit()

#    def _save_png(self, input_path, output_path, x_label, y_label, average_of_n_last, show_goal, show_trend, show_legend):
#        x = []
#        y = []
#        with open(input_path, "r") as reward:
#            reader = csv.reader(reward)
#            data = list(reader)
#
#            for i in range(0, len(data)):
#                if i % 2 == 0: 
#                    x.append(int(i))
#                    y.append(int(data[i][0]))
#
#        plt.subplots()
#        plt.plot(x, y, label="reward per run")
#
#        average_range = average_of_n_last if average_of_n_last is not None else len(x)
#        plt.plot(x[-average_range:], [np.mean(y[-average_range:])] * len(y[-average_range:]), linestyle="--", label="last " + str(average_range) + " runs average")
#
#        if show_goal:
#            plt.plot(x, [AVERAGE_SCORE_TO_SOLVE] * len(x), linestyle=":", label=str(AVERAGE_SCORE_TO_SOLVE) + " score average goal")
#
#        if show_trend and len(x) > 1:
#            trend_x = x[1:]
#            z = np.polyfit(np.array(trend_x), np.array(y[1:]), 1)
#            p = np.poly1d(z)
#            plt.plot(trend_x, p(trend_x), linestyle="-.",  label="trend")
#
#        plt.title(self.env_name)
#        plt.xlabel(x_label)
#        plt.ylabel(y_label)
#
#        if show_legend:
#            plt.legend(loc="upper left")
#
#        plt.savefig(output_path, bbox_inches="tight")
#        plt.close()
   
    def meanreward(self):
        return mean(self.reward)
            
    def add_position(self, position, cell):
        self._save_csv_position(self.POSITION_CSV_PATH, position,cell)
#        self._save_png(input_path=REWARD_CSV_PATH,
#                       output_path=REWARD_PNG_PATH,
#                       x_label="runs",
#                       y_label="scores",
#                       average_of_n_last=CONSECUTIVE_RUNS_TO_SOLVE,
#                       show_goal=True,
#                       show_trend=True,
#                       show_legend=True)

#        print ("position: (position: " + str(min(position)) + ", cell: " + str('and') + ", : " + str(max(cell)) + ")\n")

    def _save_csv(self, path, reward,run):
        if not os.path.exists(path):
            with open(path, "w", newline=""):
                pass
        reward_file = open(path, "a", newline="")
        with reward_file:
            writer = csv.writer(reward_file)
            writer.writerow([run, reward])
 
    def _save_csv_position(self, path, position,cell):
        if not os.path.exists(path):
            with open(path, "w", newline=""):
                pass
        reward_file = open(path, "a", newline="")
        with reward_file:
            writer = csv.writer(reward_file)
            writer.writerow([position[0], position[1], position[2], position[3], position[4], cell])
                       

