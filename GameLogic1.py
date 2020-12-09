import random
import time

def splitPlayers(pls):
	players = []
	for p in pls:
		players.append(p)
	pls = players
	seekers = []
	newseeker = random.randint(0, len(pls)-1)
	seekers.append(pls[newseeker])
	pls.pop(newseeker)
	hiders = []
	for pl in pls:
		hiders.append(pl)

	return hiders, seekers

def is_seeker(seeker, seekers):
	# print("owo")
	for a in seekers:
		if seeker == a:
			return True
		# else:
		# 	print ("oh nooooooooooooo1")
		# 	return False

def is_hider(hider, hiders):
	# print("uwu")
	for b in hiders:
		if hider == b:
			return True
		# else:
		# 	print ("oh nooooooooooooo2")
		# 	return False

def is_frozen(frozen, frozens):
	# print("www")
	for b in frozens:
		if frozen == b:
			return True


def find_seeker(seeker, seekers):
	for i in range(len(seekers)):
		if seeker == seekers[i]:
			return i

def find_hider(hider, hiders):
	for i in range(len(hiders)):
		if hider == hiders[i]:
			return i


def find_frozen(frozen, frozens):
	for i in range(len(frozens)):
		if frozen == frozens[i]:
			return i

def increasePlayerHits(players, hits, player):
	playerhits, nomhitbox = findPlayerHits(players, hits, player)
	playerhits = playerhits+1
	hits[nomhitbox] = playerhits
	return playerhits

def findPlayerHits(players, hits, player):
	for i in range(len(players)):
		if player == players[i]:
			nomhitbox = i
			return hits[i], nomhitbox


def seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer):
	newnomhider = find_hider(hdr, hiders)
	uwu, nomhitbox = findPlayerHits(players, hits, hdr)
	uwu = uwu+1
	hits[nomhitbox] = uwu
	if uwu == 3:
		hdrfrozen(hdr, hiders, frozens, timer)
	if uwu == 5:
		hdrfrozen(hdr, hiders, frozens, timer)
	if uwu == 6:
		goToSeekersNofreeze(seekers, hdr, hiders)

def goToSeekersNofreeze(seekers, hider, hiders):
	newnomseeker = find_hider(hider, hiders)
	hiders.pop(newnomseeker)
	seekers.append(hider)

def goToSeekers(seekers, frz, frozens):
	newnomseeker = find_frozen(frz, frozens)
	frozens.pop(newnomseeker)
	seekers.append(frz)


def hdrfrozen(hdr, hiders, frozen, timer):
	nomhider = find_hider(hdr, hiders)
	if is_hider(hdr, hiders):
		hiders.pop(nomhider)
		frozen.append(hdr)
		timer.append(time.time())
		print(str(hdr)+" was frozen!")
	return frozen, timer


def findExpiredTimer(timers, timeout):
	index = 0
	for start in timers:
		timePassed = int(time.time() - start)
		if timePassed > timeout:
			return index
		index = index+1
	return -1

def unFrozen(hdr, frz, hiders, frozens, timers):
	if is_frozen(frz, frozens) and is_hider(hdr, hiders):
		nomfrozen = find_frozen(frz, frozens)
		frozens.pop(nomfrozen)
		timers.pop(nomfrozen)
		hiders.append(frz)

def checkGameTimer(gametimer, timeout):
	timePassed = int(time.time() - gametimer)
	if timePassed > timeout:
		print ("Game timer is out!!!")
		return True

def seekersWon(seekers, hiders, frozens):
	if len(seekers) >0:
		if len(hiders) == 0:
				if len(frozens) == 0:
					return True
	if len(hiders) >0:
		return False
	if len(frozens) >0:
		return False

def hidersWon(seekers, hiders, frozens):
	if len(hiders) >0:
		return True
	if len(frozens) >0:
		return True


def hidersHitsAdd(hiders):
	hits = []
	for i in hiders:
		hits.append(0)

	return hits