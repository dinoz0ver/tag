from Logic import *
from Utils import input

FREEZE_TIMEOUT = 30 # секунд
GAME_TIMEOUT = 300 # секунд
SEED = 100500

import random
random.seed(SEED)

players = [
"1 bruh",
"2 bruh",
"3 bruh",
"4 bruh",
"5 bruh"
]

hiders, seekers = splitPlayers(players)
frozen = []
timers = []
hits = createHidersHits(players)
gametimer = createTimer()


print("Seekers:", seekers)
print("Hiders:", hiders)


def CheckInput():
	try:
		while True:
			s = input("> ")
			if s == "hit":
				s1 = input("Кто ударил? ")
				s2 = input("Кого ударил? ")
				if is_seeker(s1, seekers) and is_hider(s2, hiders):
					seekerHitHider(s1, s2, seekers, hiders, players, hits, frozen, timers)
			elif s == "hithit":
				s1 = input("Кто ударил? ")
				s2 = input("Кого ударил? ")
				num = int(input("Сколько раз? "))
				if is_seeker(s1, seekers) and is_hider(s2, hiders):
					for i in range(num):
						seekerHitHider(s1, s2, seekers, hiders, players, hits, frozen, timers)
			elif s == "print":
				print("Seekers:", seekers)
				print("Hiders:", hiders)
				print("Frozen:", frozen)
				print("Timers:", timers)
			elif s == "cold":
				f1 = input("Кто заморозил? ")
				f2 = input("Кого заморозили? ")
				if is_seeker(f1, seekers) and is_hider(f2, hiders):
					hdrfrozen(f2, hiders, frozen, timers)
			elif s == "timers":
				expiredtimer = (findExpiredTimer(timers, FREEZE_TIMEOUT))
				print(expiredtimer)
				if expiredtimer != -1:
					timers.pop(expiredtimer)
					goToSeekers(seekers, frozen[expiredtimer], frozen)
			elif s == "unfreeze":
				f2 = input("Кого размораживаем? ")
				f1 = input("Кто размораживает? ")
				unfreeze(f1, f2, hiders, frozen, timers)
			elif s == "hits":
				print(players)
				print(hits)
	except EOFError:
		pass

def GameLoop():
	while True:
		if checkGameTimer(gametimer, GAME_TIMEOUT):
			if seekersWon(seekers, hiders, frozen):
				print ("Seekers won!!!")
			if hidersWon(seekers, hiders, frozen):
				print ("Hiders won!!!")
			break
		if seekersWon(seekers, hiders, frozen):
			print ("Seekers won!!!")
			break
		expiredtimer = (findExpiredTimer(timers, FREEZE_TIMEOUT))
		if expiredtimer != -1:
			print(f"Timer {expiredtimer} has expired")
			goToSeekers(seekers, frozen[expiredtimer], frozen)
		wait_a_little()

def wait_a_little():
	time.sleep(0.001)