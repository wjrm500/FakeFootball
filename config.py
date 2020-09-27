systemConfig = {
    'numSystems': 8,
    'numDivisionsPerSystem': 4,
    'numTeamsPerDivision': 20,
    'numPlayersPerTeam': 40
}

playerConfig = {
    'age': {
        'min': 15,
        'max': 40
    },
    'growthSpeed': {
        'incline': {
            'mean': 0.5,
            'stDev': 0.1
        },
        'decline': {
            'mean': 1,
            'stDev': 0.1
        }
    },
    'peakAge': {
        'min': 22,
        'max': 32
    },
    'peakRating': {
        'mean': (100 / 3 *  2),
        'stDev': 10
    },
    'positions': {
        'CF': {'offence': 1.3, 'spark': 0.95, 'defence': 0.8, 'control': 0.95}, 
        'WF': {'offence': 1.15, 'spark': 1.3, 'defence': 0.8, 'control': 0.75}, 
        'CAM': {'offence': 0.85, 'spark': 1.45, 'defence': 0.75, 'control': 0.95}, 
        'WM': {'offence': 1.05, 'spark': 1.25, 'defence': 0.9, 'control': 0.8}, 
        'CM': {'offence': 0.95, 'spark': 1.05, 'defence': 0.9, 'control': 1.1}, 
        'CDM': {'offence': 0.85, 'spark': 0.95, 'defence': 1.1, 'control': 1.1}, 
        'WB': {'offence': 1, 'spark': 1.2, 'defence': 1.05, 'control': 0.75}, 
        'FB': {'offence': 0.95, 'spark': 1.1, 'defence': 1.1, 'control': 0.85}, 
        'CB': {'offence': 0.85, 'spark': 0.85, 'defence': 1.25, 'control': 1.05}
    },
    'retirementThreshold': {
        'mean': 0.85,
        'stDev': 0.025
    },
    'skillDistribution': {
        'mean': 1,
        'stDev': 0.25
    }
}