import numpy as np
from dnd.dice import Dice

if __name__ == '__main__':
    
    runs = 10000
    d20 = Dice(20)  # 1d20 + 5
    d8 = Dice(8)    # Spear
    d4 = Dice(4)    # Unarmed Strike
    
    hitBonus = 5
    dexBonus = 3

    print(f'Simulating {runs:,.0f} dice rolls against each AC.')

    for ac in range(1,21):
        
        results = []

        for _ in range(runs):
            damage = 0
            
            # Action: Spear attack
            d20.roll(modifier=hitBonus)
            if d20.check(ac, checkCrit = True):
                damage += d8.damage(modifier=dexBonus, crit=d20.critical)
            
            # Bonus Action: Unarmed Strike
            d20.roll(modifier=hitBonus)
            if d20.check(ac, checkCrit = True):
                damage += d4.damage(modifier=dexBonus, crit=d20.critical)

            results.append(damage)

        resultsArray = np.array(results)

        resultsMean = resultsArray.mean()
        hitRate = len(resultsArray[resultsArray > 0]) / len(resultsArray)
        
        print(f'Vs. ac {ac}: avg damage =\t{resultsMean:,.2f}, accuracy {hitRate:.1%}')