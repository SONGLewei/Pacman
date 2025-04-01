import json
import math
import sys
import os
import time
import numpy as np
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.controller.game import Game
from training.pacmanAI import PacmanOfReseauNeuron
from elements.dot import Dot
from elements.bigDot import BigDot
from elements.ghost import Ghost
from visual.showAI import VisualAIPlayerGame



class SelectTheBestInTheJson(VisualAIPlayerGame):
    def __init__(self):
        super().__init__(headless=False)
        self.path = '../IR/final_res_json.json'
        with open(self.path,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.ai_list = data["ai_results"]
        self.best_score = 0
        self.best_individual = None
        self.thisNumber = 0
        
            
    def run(self):
        for ai_data in self.ai_list:
            self.thisNumber+=1;
            print(f"This is the {self.thisNumber}th AI")
            self.resetGameState()
            weights = ai_data["network_weights"]
            loaded_weight = []
            for layer2d in weights:
                arr = np.array(layer2d,dtype = float)
                loaded_weight.append(arr)
            self.ai_agent = PacmanOfReseauNeuron()
            self.ai_agent.network_weights = loaded_weight

            self.loadLevel()
            while self.isRunning:
                state = self.get_game_state()
                action = self.ai_agent.getDecision(state)
                self.player.setDirection(action)

                super().update()
                super().render()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.endGame()


            
            score = self.score
            if score > self.best_score:
                self.best_score = score
                self.best_individual = ai_data

        
        self.saveBestIndividual(self.best_individual)
        
    
    def saveBestIndividual(self,best_individual):
        path = './IR/best_individual.json'
        with open(path,'w',encoding='utf-8') as f:
            json.dump(best_individual,f,indent=4)
        print("Best individual saved")
                
    def resetGameState(self):
        self.score = 0
        self.isRunning = True
        self.staticEntities.clear()
        self.movableEntities.clear()
        self.loadConfig()
        self.loadLevel()
                
                
