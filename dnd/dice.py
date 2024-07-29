import numpy as np

class Dice:
    
    def __init__(self, sides:int = 20, modifier:int = 0):
        self.sides = sides
        self.modifier = modifier

        # Set default outcome values
        self.result = np.nan
        self.critical = 0
        
        # Quick map to set values for a critical success (1) and critical fail (-1)
        self._critionary = {20:1, 1:-1}

    def roll(self, modifier:int = None, mode:str = ''):
        
        if modifier == None:
            modifier = self.modifier

        ix = 0
        timesRolled = {'adv': 2, 'dis': 2}

        outcome = [np.random.randint(1, self.sides + 1) for _ in range(timesRolled.get(mode, 1))]

        if mode.lower() == 'adv':
            ix = np.argmax(outcome) 
        elif mode.lower() == 'dis':
            ix = np.argmin(outcome)
            
        self.result = outcome[ix] + modifier

        # Record if critical success or fail
        self.critical = self._critionary.get(outcome[ix], 0)

        return self.result
    
    def check(self, threshold:int = 0, checkCrit:bool = False):
        
        # First check if the threshold is met or a critical success (if crits are allowed)
        if self.result >= threshold or (checkCrit and self.critical == 1):
            
            # Second check is to handle if the first check is passed on merit, check if there is a crit fail
            if checkCrit and self.critical == -1:
                return False
            else:
                return True
        else:
            return False

    def damage(self, modifier:int=None, crit:bool=False):
        '''
        Damage roll simulation. 
        Follows the dnd 5e rule if the hit roll is a critical success, 
        roll the attack dice twice.
        '''

        if modifier == None:
            modifier = self.modifier

        outcome = 0
        
        if crit:
            outcome += np.sum([self.roll() for _ in range(2)]) + modifier
        else:
            outcome += self.roll() + modifier

        return outcome