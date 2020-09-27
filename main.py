from SystemController import SystemController
import numpy as np
from PlayerController import PlayerController
from Player import Player
from config import systemConfig, playerConfig

### Generate systems

systemController = SystemController(systemConfig)
systemController.initialise()

### Generate players

initialPlayerPoolSize = np.prod(list(systemConfig.values()))
playerController = PlayerController(playerConfig)
for _ in range(initialPlayerPoolSize):
    playerController.addPlayer()

### Add players to teams

for system in systemController.systems:
    for division in system.divisions:
        for team in division.teams:
            randomPlayer = playerController.getRandomFreeAgent()
            team.signPlayer(randomPlayer)