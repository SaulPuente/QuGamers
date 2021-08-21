# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 01:19:34 2021

@author: saulp
"""
import QuantumEngine

class soldier():
    def __init__(self):
        self.status = {
            "ID": 0,
            "health": 3,
            "attack": 1,
            "defense": 1,
            "superposition": False,
            "state0": (0,0),
            "state1": (0,0),
            "prob0": 1.0,
            "prob1": 0.0,
            "image1": "",
            "image2": "",
            "istate": (0,0)
            }
        
    def createQubit(self):
        self.qubit = QuantumEngine.qubit(self.status["ID"])
    