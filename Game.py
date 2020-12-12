import Logic
import Api as API

class RealGame: pass

def init(Game):
  # установка таймаутов
  Game.FREEZE_TIMEOUT = API.getFreezeTimeout()
  Game.SEEKER_TIMEOUT = API.getSeekerTimeout()
  Game.GAME_TIMEOUT = API.getGameTimeout()

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

  # отправляем Майну команду "начало игры"
  API.startGame(Game)

  # запускаем таймер и отправляем Майну команду "запустить главный таймер"
  Game.gametimer = Logic.createTimer()
  API.startMainGameTimer(Game.gametimer, Game.GAME_TIMEOUT)

  # то же самое, только для таймера искателей
  Game.seekertimer = Logic.createTimer()
  API.startSeekerTimer(Game.seekertimer, Game.SEEKER_TIMEOUT)

def copyGame(Game):
  newGame = RealGame()
  newGame.players = Game.players.copy()
  newGame.hiders  = Game.hiders.copy()
  newGame.seekers = Game.seekers.copy()
  newGame.frozen  = Game.frozen.copy()
  newGame.timers  = Game.timers.copy()
  newGame.hits    = Game.hits.copy()
  newGame.gametimer = Game.gametimer
  newGame.seekertimer = Game.seekertimer
  return newGame

def listDiff(smaller, bigger):
  return list(set(bigger) - set(smaller))

def findDiff(oldGame, newGame):
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
  return changed

# TODO: seekertimer
def GameLoop(Game):
  gameCopy = copyGame(Game)
  while True:
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
    # проверка таймеров замороженных игроков
    i = Logic.findExpiredTimer(Game.timers, Game.FREEZE_TIMEOUT)
    if i != -1:
      Logic.goToSeekers(Game.seekers, Game.frozen[i], Game.frozen, Game.timers)
    # получение событий ударов
    # Пример: [EntityEvent(damager=vadimpilyugin, damagee=Dinozover)]
    hasHit = False
    for event in API.getPlayerHits():
      hasHit = True
      player1 = event.damager
      player2 = event.damagee
      Logic.playerHitPlayer(player1, player2, Game.hiders, Game.seekers, Game.frozen, Game.players, Game.hits, Game.timers)

    hasDiff = findDiff(gameCopy, Game)

    if not hasDiff and hasHit:
      print("Nothing changed after hit")
    elif hasDiff:
      print("Game state has changed, creating new copy")
      gameCopy = copyGame(Game)

    Logic.wait_a_little()
  API.finishGame(Game)
