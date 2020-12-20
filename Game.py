import Logic
import copy
import time

class RealGame: pass

def init(Game, fake=True, gameTimeout=400):
  if not fake:
    import Api as API
  else:
    import FakeApi as API
  # установка таймаутов
  Game.FREEZE_TIMEOUT = API.getFreezeTimeout()
  Game.SEEKER_TIMEOUT = API.getSeekerTimeout()
  Game.GAME_TIMEOUT = gameTimeout
  Game.SEEKERS_SPAWN = API.getSeekersSpawn()
  Game.HIDERS_SPAWN = API.getHidersSpawn()
  Game.HIT_TIMEOUT = 0.8
  Game.UNFREEZE_TIMEOUT = 3
  Game.CHECK_TIMER = 1
  Game.API = API

  # инициализация генератора случайных чисел
  Game.SEED = API.getSeed()
  Logic.randomSeed(Game.SEED)

  # получения от Майнкрафта списка игроков
  players = API.getPlayers()

  # деление игроков на команды (внутри программы)
  hiders, seekers = Logic.splitPlayers(players)

  # деление игроков на команды в Майне
  API.createTeam("hiders", hiders)
  API.createTeam("seekers", seekers)

  # складываем все списки в коробку Game
  Game.players = players
  Game.hiders = hiders
  Game.seekers = seekers
  Game.frozen = []
  Game.timers = []
  Game.hits = Logic.createPlayersHits(players)
  Game.unfreezeTimers = {}
  Game.hidersArmor = {}

  # отправляем Майну команду "начало игры"
  API.startGame(Game)

  # запускаем таймер и отправляем Майну команду "запустить главный таймер"
  Game.gametimer = Logic.createTimer()
  API.startMainGameTimer(Game.gametimer, Game.GAME_TIMEOUT)

  # то же самое, только для таймера искателей
  Game.seekertimer = Logic.createTimer()
  API.startSeekerTimer(Game.seekertimer, Game.SEEKER_TIMEOUT)

  Game.checktimer = Logic.createTimer()

def copyGame(Game):
  newGame = RealGame()
  for name, obj in vars(Game).items():
    if isinstance(obj, list) or isinstance(obj, dict):
      newObj = copy.deepcopy(obj)
    else:
      newObj = obj
    setattr(newGame, name, newObj)
  return newGame

def listDiff(smaller, bigger):
  return list(set(bigger) - set(smaller))

def findDiff(oldGame, newGame):
  API = oldGame.API
  changed = False
  if len(newGame.hiders) < len(oldGame.hiders):
    # хайдеров стало меньше
    API.removeHiders(listDiff(newGame.hiders, oldGame.hiders))
    changed = True
  if len(newGame.seekers) > len(oldGame.seekers):
    API.addSeekers(listDiff(oldGame.seekers, newGame.seekers))
    changed = True
  if set(oldGame.frozen) != set(newGame.frozen):
    newFrozen = listDiff(oldGame.frozen, newGame.frozen)
    if len(newFrozen) > 0:
      # добавились замороженные люди
      API.addFrozen(newFrozen, newGame.FREEZE_TIMEOUT)
    newUnfrozen = listDiff(newGame.frozen, oldGame.frozen)
    if len(newUnfrozen) > 0:
      # люди разморозились по таймеру
      API.removeFrozen(newUnfrozen)
    changed = True
  if oldGame.hits != newGame.hits:
    for i,score in enumerate(newGame.hits):
      if score != oldGame.hits[i]:
        API.updateScore(newGame.players[i], score)
    changed = True
  if oldGame.unfreezeTimers != newGame.unfreezeTimers:
    changed = True
    # поменялись таймеры на разморозку
    if len(oldGame.unfreezeTimers) < len(newGame.unfreezeTimers):
      # кто-то начал разморозку
      newUnfreezers = listDiff(oldGame.unfreezeTimers, newGame.unfreezeTimers)
      API.addUnfreezers(newUnfreezers)
    elif len(oldGame.unfreezeTimers) == len(newGame.unfreezeTimers):
      # обновился таймер
      for key, oldTimers in oldGame.unfreezeTimers.items():
        newTimers = newGame.unfreezeTimers[key]
        hdr, frz = key
        if key in newGame.unfreezeTimers and oldTimers != newTimers:
          API.sendUnfreezeCount(hdr, frz, time.time() - newTimers["unfreeze"], newGame.UNFREEZE_TIMEOUT)

  return changed

# TODO: seekertimer
def GameLoop(Game):
  API = Game.API
  gameCopy = copyGame(Game)
  while True:
    # проверка таймера искателей
    if Game.seekertimer is not None and Logic.checkTimer(Game.seekertimer, Game.SEEKER_TIMEOUT):
      API.releaseSeekers(Game.seekers)
      Game.seekertimer = None

    # проверка победы по завершении таймера игры
    if Logic.checkGameTimer(Game.gametimer, Game.GAME_TIMEOUT):
      if Logic.seekersWon(Game.seekers, Game.hiders, Game.frozen):
        API.announceWin("seekers")
      if Logic.hidersWon(Game.seekers, Game.hiders, Game.frozen):
        API.announceWin("hiders")
      break
    # проверка досрочной победы искателей
    if Logic.seekersWon(Game.seekers, Game.hiders, Game.frozen):
      API.announceWin("seekers")
      break
    # проверка досрочной победы хайдеров
    if Logic.hidersQuicklyWon(Game.seekers, Game.hiders, Game.frozen):
      API.announceWin("hiders")
      break
    # проверка, не вышел ли кто-либо из игры
    for event in API.getPlayerExistence():
      if event.hasLeft():
        API.onPlayerQuit(event.name)
        Logic.removePlayerOnQuit(Game, event.name)
    # проверка всякого раз в секунду
    if Logic.checkTimer(Game.checktimer, Game.CHECK_TIMER):
      Game.checktimer = Logic.createTimer()
      API.checkHidersWearArmor(Game)
    # проверка таймеров замороженных игроков
    i = Logic.findExpiredTimer(Game.timers, Game.FREEZE_TIMEOUT)
    if i != -1:
      Logic.goToSeekers(Game.seekers, Game.frozen[i], Game.frozen, Game.timers)
    # проверка таймеров разморозки
    Logic.checkEveryoneHitTiming(Game)
    # получение событий снежков
    for event in API.getProjectileHits():
      if Logic.is_hider(event.originName, Game.hiders) and Logic.is_seeker(event.targetName, Game.seekers):
        API.slowPlayer(event.targetName)
    # получение событий ударов
    # Пример: [EntityEvent(damager=vadimpilyugin, damagee=Dinozover)]
    hasHit = False
    for event in API.getPlayerHits():
      hasHit = True
      player1 = event.damager
      player2 = event.damagee
      Logic.playerHitPlayer(player1, player2, Game)

    hasDiff = findDiff(gameCopy, Game)

    if not hasDiff and hasHit:
      print("Nothing changed after hit")
    elif hasDiff:
      print("Game state has changed, creating new copy")
      gameCopy = copyGame(Game)

    Logic.wait_a_little()
  API.finishGame(Game)
