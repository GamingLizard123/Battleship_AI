import bot
import numpy as np
import sys


hard = bot.HardBot()

ship_coord = [[4,4],[4,5],[4,6],[4,7], [3,2],[3,3],[3,4]]
cont = True
hard.gen_prob_map()
print(f"Prob map:\n{hard.PROB_MAP}")

while cont:
    strike = hard.strike()

    if strike in ship_coord:
        ship_coord.remove(strike)
        if ship_coord == []:
            hard.success_log.append("sunk")
            sys.exit("Ship sunk succesfully")
        hard.success_log.append("hit")
    else:
        hard.success_log.append("miss")
        

    hard.gen_prob_map()
    print(f"Prob map:\n{hard.PROB_MAP}\nstrike coord: {strike}")


    if hard.success_log[-1] == "hit":
        print("hit")


    inp = input("continue: ")
    print("-------------------------------------------------------------")
