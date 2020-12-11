import random
import time

# функция делит список игроков на две команды случайным образом
def splitPlayers(pls):
	players_copy = pls.copy()
	pls = players_copy

	seekers = []
	newseeker = random.randint(0, len(pls)-1)
	seekers.append(pls[newseeker])
	pls.pop(newseeker)

	hiders = []
	for pl in pls:
		hiders.append(pl)

	return hiders, seekers


# проверка принадлежности человека к одной из команд
def is_seeker(seeker, seekers):
	i = find_seeker(seeker, seekers)
	if i == -1:
		return False
	return True

def is_hider(hider, hiders):
	i = find_hider(seeker, seekers)
	if i == -1:
		return False
	return True

def is_frozen(frozen, frozens):
	i = find_frozen(seeker, seekers)
	if i == -1:
		return False
	return True

# проверка принадлежности человека к одной из команд, возврат индекса в списке
def find_seeker(seeker, seekers):
	for i in range(len(seekers)):
		if seeker == seekers[i]:
			return i
	return -1

def find_hider(hider, hiders):
	for i in range(len(hiders)):
		if hider == hiders[i]:
			return i
	return -1


def find_frozen(frozen, frozens):
	for i in range(len(frozens)):
		if frozen == frozens[i]:
			return i
	return -1

# работа со счетчиками хитов

# увеличение хитов игрока на 1
def increasePlayerHits(players, hits, player):
	playerhits, nomhitbox = findPlayerHits(players, hits, player)
	playerhits = playerhits + 1
	hits[nomhitbox] = playerhits
	return playerhits

# поиск счетчика хитов по имени игрока
def findPlayerHits(players, hits, player):
	for i in range(len(players)):
		if player == players[i]:
			nomhitbox = i
			return hits[i], nomhitbox
	return -1, -1

def playerHitPlayer(player1, player2, hiders, seekers, frozens, players, hits, timer):
	if is_seeker(player1) and is_hider(player2):
		seekerHitHider(player1, player2, seekers, hiders, players, hits, frozens, timer)
	if is_hider(player1) and is_frozen(player2):
		unfreeze(player1, player2, hiders, frozens, timer)

# Функция получает на вход имена seeker-а и hider-а, и увеличивает
# счетчик ударов у hider-а. В зависимости от значения счетчика
# игрок либо замораживается, либо переходит в другую команду
def seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer):
	newnomhider = find_hider(hdr, hiders)
	uwu, nomhitbox = findPlayerHits(players, hits, hdr)
	uwu = uwu+1
	hits[nomhitbox] = uwu
	# логика такая: в первый раз у хайдера 3 жизни, во второй
	# раз две, а в последний раз одна, плюс нет таймера на заморозку
	if uwu == 3:
		hdrfrozen(hdr, hiders, frozens, timer)
	if uwu == 5:
		hdrfrozen(hdr, hiders, frozens, timer)
	if uwu == 6:
		goToSeekersNofreeze(seekers, hdr, hiders)

# функция перекидывает хайдера в команду искателей
def goToSeekersNofreeze(seekers, hider, hiders):
	print(f"Hider {hider} becomes a seeker with no freezing!")
	newnomseeker = find_hider(hider, hiders)
	hiders.pop(newnomseeker)
	seekers.append(hider)

# функция перекидывает замороженного человека в команду искателей
def goToSeekers(seekers, frz, frozens):
	print(f"Hider {frz} becomes a seeker after a timeout!")
	newnomseeker = find_frozen(frz, frozens)
	frozens.pop(newnomseeker)
	timers.pop(newnomseeker)
	seekers.append(frz)

# функция добавляет хайдера в список замороженных и заводит таймер
def hdrfrozen(hdr, hiders, frozen, timers):
	nomhider = find_hider(hdr, hiders)
	hiders.pop(nomhider)
	frozen.append(hdr)
	freeze_timer = createTimer()
	timers.append(freeze_timer)
	print(str(hdr)+" was frozen!")
	return frozen, timers

def checkTimer(timer, timeout):
	timePassed = int(time.time() - timer)
	if timePassed > timeout:
		return True
	return False

# функция ходит по массиву таймеров и находит истекший
def findExpiredTimer(timers, timeout):
	index = 0
	for timer in timers:
		if checkTimer(timer, timeout):
			return index
		index = index+1
	return -1

# функция размораживает человека и добавляет его обратно
# в список хайдеров
def unfreeze(hdr, frz, hiders, frozens, timers):
	nomfrozen = find_frozen(frz, frozens)
	frozens.pop(nomfrozen)
	timers.pop(nomfrozen)
	hiders.append(frz)
	print(f"{frz} was unfrozen by {hdr}. Thanks, man!")

# функция проверяет таймер игры
def checkGameTimer(gametimer, timeout):
	return checkTimer(gametimer, timeout)

def createTimer():
	return time.time()

# функция проверяет, победили ли искатели
def seekersWon(seekers, hiders, frozens):
	if len(seekers) > 0 and len(hiders) == 0 and len(frozens) == 0:
		return True
	if len(hiders) > 0:
		return False
	if len(frozens) > 0:
		return False
	return False

# функция проверяет, победили ли прячущиеся
def hidersWon(seekers, hiders, frozens):
	if len(hiders) > 0:
		return True
	if len(frozens) > 0:
		return True
	return False

# вспомогательная не очень нужная функция для создания списка хитов
def createHidersHits(hiders):
	hits = []
	for i in hiders:
		hits.append(0)
	return hits