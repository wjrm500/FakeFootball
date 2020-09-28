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
        'CF': {
            'realName': "Centre Forward",
            'skillDistribution': {
                'offence': 1.52,
                'spark': 1.06,
                'technique': 1.03,
                'defence': 0.69,
                'authority': 0.95,
                'fitness': 0.75
            }
        },
        'WF': {
            'realName': "Wing Forward",
            'skillDistribution': {
                'offence': 1.19,
                'spark': 1.35,
                'technique': 1.08,
                'defence': 0.75,
                'authority': 0.69,
                'fitness': 0.94
            }
        },
        'COM': {
            'realName': "Centre Offensive Midfielder",
            'skillDistribution': {
                'offence': 1.05,
                'spark': 1.42,
                'technique': 1.48,
                'defence': 0.66,
                'authority': 0.73,
                'fitness': 0.66
            }
        },
        'WM': {
            'realName': "Wing Midfielder",
            'skillDistribution': {
                'offence': 1.06,
                'spark': 1.24,
                'technique': 1.06,
                'defence': 0.81,
                'authority': 0.76,
                'fitness': 1.07
            }
        },
        'CM': {
            'realName': "Centre Midfielder",
            'skillDistribution': {
                'offence': 0.87,
                'spark': 0.92,
                'technique': 1.04,
                'defence': 0.86,
                'authority': 1.28,
                'fitness': 1.03
            }
        },
        'CDM': {
            'realName': "Centre Defensive Midfielder",
            'skillDistribution': {
                'offence': 0.73,
                'spark': 0.84,
                'technique': 0.95,
                'defence': 1.10,
                'authority': 1.23,
                'fitness': 1.15
            }
        },
        'WB': {
            'realName': "Wing Back",
            'skillDistribution': {
                'offence': 0.75,
                'spark': 1.03,
                'technique': 1.03,
                'defence': 1.05,
                'authority': 0.68,
                'fitness': 1.46
            }
        },
        'FB': {
            'realName': "Full Back",
            'skillDistribution': {
                'offence': 0.73,
                'spark': 0.92,
                'technique': 0.94,
                'defence': 1.24,
                'authority': 0.93,
                'fitness': 1.24
            }
        },
        'CB': {
            'realName': "Centre Back",
            'skillDistribution': {
                'offence': 0.72,
                'spark': 0.77,
                'technique': 0.92,
                'defence': 1.35,
                'authority': 1.26,
                'fitness': 0.98
            }
        }               
        # 'CF': {'skillDistribution': {'offence': 1.52, 'spark': 1.06, 'technique': 1.03, 'defence': 0.69, 'authority': 0.95, 'fitness': 0.75}}, 
        # 'WF': {'skillDistribution': {'offence': 1.19, 'spark': 1.35, 'technique': 1.08, 'defence': 0.75, 'authority': 0.69, 'fitness': 0.94}}, 
        # 'COM': {'skillDistribution': {'offence': 1.05, 'spark': 1.42, 'technique': 1.48, 'defence': 0.66, 'authority': 0.73, 'fitness': 0.66}}, 
        # 'WM': {'skillDistribution': {'offence': 1.06, 'spark': 1.24, 'technique': 1.06, 'defence': 0.81, 'authority': 0.76, 'fitness': 1.07}}, 
        # 'CM': {'skillDistribution': {'offence': 0.87, 'spark': 0.92, 'technique': 0.97, 'defence': 0.86, 'authority': 1.35, 'fitness': 1.03}}, 
        # 'CDM': {'skillDistribution': {'offence': 0.73, 'spark': 0.84, 'technique': 0.95, 'defence': 1.1, 'authority': 1.23, 'fitness': 1.15}}, 
        # 'WB': {'skillDistribution': {'offence': 0.75, 'spark': 1.03, 'technique': 1.03, 'defence': 1.05, 'authority': 0.68, 'fitness': 1.46}}, 
        # 'FB': {'skillDistribution': {'offence': 0.73, 'spark': 0.92, 'technique': 0.94, 'defence': 1.24, 'authority': 0.93, 'fitness': 1.24}}, 
        # 'CB': {'skillDistribution': {'offence': 0.72, 'spark': 0.77, 'technique': 0.92, 'defence': 1.35, 'authority': 1.26, 'fitness': 0.98}}
    },
    'retirementThreshold': {
        'mean': 0.85,
        'stDev': 0.025
    },
    'skill': {
        'distribution': {
            'mean': 1,
            'stDev': 0.375,
            'min': 0.375,
            'max': 1.875
        },
        'normalisingFactor': {
            'mean': 0.25,
            'stDev': 0.05,
            'min': 0,
            'max': 0.5
        },
        'skills': [
            'offence', 
            'spark', ### A player's ability to create something from nothing
            'technique',
            'defence',
            'authority', ### How well a player is able to take control of a situation
            'fitness'
        ]
    }
}