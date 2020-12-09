import time
from GameLogic1 import *
random.seed(100500)

DEBUG_FILE = False

def my_input(msg):
	s = input(msg)
	if DEBUG_FILE:
		print(s)
	return s

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
hits = hidersHitsAdd(players)
gametimer = time.time()


print("Seekers:", seekers)
print("Hiders:", hiders)



try:
	while True:
		if checkGameTimer(gametimer, 300):
			if seekersWon(seekers, hiders, frozen):
				print ("Seekers won!!!")
			if hidersWon(seekers, hiders, frozen):
				print ("Hiders won!!!")
			break
		if seekersWon(seekers, hiders, frozen):
			print ("Seekers won!!!")
			break

		s = my_input("> ")
		if s == "hit":
			s1 = my_input("Кто ударил? ")
			s2 = my_input("Кого ударил? ")
			if is_seeker(s1, seekers) and is_hider(s2, hiders):
				# print("awaw1")
				seekerHitHider(s1, s2, seekers, hiders, players, hits, frozen, timers)
				# print("awaw2")
		elif s == "sleep":
			x = int(my_input("How long? "))
			time.sleep(x)
		elif s == "print":
			print("Seekers:", seekers)
			print("Hiders:", hiders)
			print("Frozen:", frozen)
			print("Timers:", timers)
		elif s == "cold":
			f1 = my_input("Кто заморозил?")
			f2 = my_input("Кого заморозили?")
			if is_seeker(f1, seekers) and is_hider(f2, hiders):
				hdrfrozen(f2, hiders, frozen, timers)
		elif s == "timers":
			expiredtimer = (findExpiredTimer(timers, 30))
			print(expiredtimer)
			if expiredtimer != -1:
				timers.pop(expiredtimer)
				goToSeekers(seekers, frozen[expiredtimer], frozen)
		elif s == "unfroze":
			f2 = my_input("Кто заморожен?")
			f1 = my_input("Кто размораживает?")
			unFrozen(f1, f2, hiders, frozen, timers)
		elif s == "hits":
			print(players)
			print(hits)

			



except EOFError:
	pass
