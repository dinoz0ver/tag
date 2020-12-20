import random
import time
from Utils import pp_timer

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

def randomSeed(seed):
    random.seed(seed)

def wait_a_little():
  time.sleep(0.01)

# проверка принадлежности человека к одной из команд
def is_seeker(seeker, seekers):
  i = find_seeker(seeker, seekers)
  if i == -1:
    return False
  return True

def is_hider(hider, hiders):
  i = find_hider(hider, hiders)
  if i == -1:
    return False
  return True

def is_frozen(frz, frozen):
  i = find_frozen(frz, frozen)
  if i == -1:
    return False
  return True

# проверка принадлежности человека к одной из команд, возврат индекса в списке
def find_seeker(seeker, seekers):
  return generic_find(seeker, seekers)

def find_hider(hider, hiders):
  return generic_find(hider, hiders)

def find_frozen(frz, frozen):
  return generic_find(frz, frozen)

def generic_find(element, lst):
  for i in range(len(lst)):
    if element == lst[i]:
      return i
  return -1


# работа со счетчиками хитов

# увеличение хитов игрока на 1
def increasePlayerHits(players, hits, player):
  playerhits, nomhitbox = findPlayerHits(players, hits, player)
  if nomhitbox != -1:
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

def playerHitPlayer(player1, player2, Game): # (player1, player2, hiders, seekers, frozen, players, hits, timer):
  if is_seeker(player1, Game.seekers) and is_hider(player2, Game.hiders):
    seekerHitHider(player1, player2, Game)
  if is_hider(player1, Game.hiders) and is_frozen(player2, Game.frozen):
    updateHitTiming(player1, player2, Game.unfreezeTimers)

# Функция получает на вход имена seeker-а и hider-а, и увеличивает
# счетчик ударов у hider-а. В зависимости от значения счетчика
# игрок либо замораживается, либо переходит в другую команду
def seekerHitHider(skr, hdr, Game):
  newnomhider = find_hider(hdr, Game.hiders)
  uwu, nomhitbox = findPlayerHits(Game.players, Game.hits, hdr)
  uwu = uwu+1
  Game.hits[nomhitbox] = uwu
  # логика такая: в первый раз у хайдера 3 жизни, во второй
  # раз две, а в последний раз одна, плюс нет таймера на заморозку
  if uwu == 3:
    hdrfrozen(hdr, Game.hiders, Game.frozen, Game.timers)
  if uwu == 5:
    hdrfrozen(hdr, Game.hiders, Game.frozen, Game.timers)
  if uwu == 6:
    goToSeekersNofreeze(Game.seekers, hdr, Game.hiders)

# функция перекидывает хайдера в команду искателей
def goToSeekersNofreeze(seekers, hider, hiders):
  print(f"Hider {hider} becomes a seeker with no freezing!")
  newnomseeker = find_hider(hider, hiders)
  hiders.pop(newnomseeker)
  seekers.append(hider)

# функция перекидывает замороженного человека в команду искателей
def goToSeekers(seekers, frz, frozen, timers):
  print(f"Hider {frz} becomes a seeker after a timeout!")
  newnomseeker = find_frozen(frz, frozen)
  frozen.pop(newnomseeker)
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
  timePassed = time.time() - timer
  if timePassed > timeout:
    return True
  return False

def timerExpired(timer, timeout):
  return checkTimer(timer, timeout)

# функция ходит по массиву таймеров и находит истекший
def findExpiredTimer(timers, timeout):
  index = 0
  for timer in timers:
    if checkTimer(timer, timeout):
      return index
    index = index+1
  return -1

def removeUnfreezeTimers(unfreezeTimers, frz):
  toDel = []
  for key in unfreezeTimers:
    _, frzz = key
    if frzz == frz:
      toDel.append(key)
  for key in toDel:
    del(unfreezeTimers[key])

def removePlayerOnQuit(Game, pl):
  iskr, ihdr, ifrz = find_seeker(pl, Game.seekers), find_seeker(pl, Game.hiders), find_seeker(pl, Game.frozen)
  if iskr != -1 or ihdr != -1 or ifrz != -1:
    flag = False
    if iskr != -1:
      print("Left player was a seeker")
      Game.seekers.pop(iskr)
      flag = True
    elif ihdr != -1:
      print("Left player was a hider")
      Game.hiders.pop(ihdr)
      flag = True
    elif ifrz != -1:
      print("Left player was frozen")
      Game.frozen.pop(ifrz)
      Game.timers.pop(ifrz)
      flag = True
    if flag:
      print("Left player was in the game")
      i = find_seeker(pl, Game.players)
      Game.hits.pop(i)
      Game.players.pop(i)

# функция размораживает человека и добавляет его обратно
# в список хайдеров
def unfreeze(hdr, frz, Game):
  removeUnfreezeTimers(Game.unfreezeTimers, frz)
  hiders, frozen, timers = Game.hiders, Game.frozen, Game.timers
  nomfrozen = find_frozen(frz, frozen)
  frozen.pop(nomfrozen)
  timers.pop(nomfrozen)
  hiders.append(frz)
  print(f"{frz} was unfrozen by {hdr}. Thanks, man!")

def updateHitTiming(hdr, frz, unfreezeTimers):
  key = (hdr, frz)
  if key not in unfreezeTimers:
    # ситуация 1: этот хайдер еще не ударял этого замороженного
    unfreezeTimers[key] = {
      "unfreeze": createTimer(),
      "hit": createTimer()
    }
    print(f"[{hdr}] начата разморозка {frz}")
  else:
    # ситуация 2: хайдер уже бил по замороженному, и таймер еще не просрочен
    # оба таймера не протекли, значит нужно сбросить таймер хитов
    print(f"[{hdr}] размораживает {frz}")
    unfreezeTimers[key]["hit"] = createTimer()
      
def checkEveryoneHitTiming(Game):
  toUnfreeze = []
  toDel = []
  for key, timers in Game.unfreezeTimers.items():
    hdr, frz = key
    res = checkHitTiming(timers, Game.HIT_TIMEOUT, Game.UNFREEZE_TIMEOUT)
    if res is None:
      # вариант 2
      print(f"[{hdr}] таймер разморозки сброшен")
      toDel.append(key)
    elif res:
      # вариант 1
      toUnfreeze.append((hdr, frz))
  for key in toDel:
    del(Game.unfreezeTimers[key])
  for key in toUnfreeze:
    hdr, frz = key
    unfreeze(hdr, frz, Game)


def checkHitTiming(timers, hitTimeout, unfreezeTimeout):
  if timerExpired(timers["unfreeze"], unfreezeTimeout):
    # вариант 1: хайдер успешно разморозил человека
    return True
  elif timerExpired(timers["hit"], hitTimeout):
    # вариант 2: хайдер продолбил свою попытку
    # нужно удалить его из внешней мапы
    return None
  else:
    # вариант 3: ни один таймер не протек
    return False


# функция проверяет таймер игры
def checkGameTimer(gametimer, timeout):
  return checkTimer(gametimer, timeout)

def createTimer():
  return time.time()

# функция проверяет, победили ли искатели
def seekersWon(seekers, hiders, frozen):
  if len(seekers) > 0 and len(hiders) == 0 and len(frozen) == 0:
    return True
  if len(hiders) > 0:
    return False
  if len(frozen) > 0:
    return False
  return False

# функция проверяет, победили ли прячущиеся
def hidersWon(seekers, hiders, frozen):
  if len(hiders) > 0:
    return True
  if len(frozen) > 0:
    return True
  return False

# функция проверяет досрочную победу хайдеров
def hidersQuicklyWon(seekers, hiders, frozen):
  if len(seekers) == 0 and len(frozen+hiders) > 0:
    return True
  return False

# вспомогательная не очень нужная функция для создания списка хитов
def createPlayersHits(players):
  hits = []
  for i in players:
    hits.append(0)
  return hits