from queue import Queue

def getPlayers():
  return [f"{i+1} bruh" for i in range(5)]

def getFreezeTimeout():
  return 15

def getGameTimeout():
  return 60

def createTeam(name, players):
  print(f"Created team '{name}' with players {players}")

def startMainGameTimer():
  print("Main game timer started")
  print("Giving everyone invisibility for xxx seconds")

def startGame():
  print("started the Game, tp-ing hiders to hiders TP")

def startSeekerTimer():
  print("started SeekerTimer")
  print("giving seekers some other effect for xx seconds")

def movePlayerToSeekers(player):
  print(f"Unfreezing {player}, removing particles, switching teams")

HitQueue = Queue()
def getPlayerHits():
  hits = []
  while not HitQueue.empty():
    hits.append(HitQueue.get())
  return hits

def removeHiders(hiders):
  print(f"Removing hiders {hiders} from the team")

def addSeekers(seekers):
  print(f"Adding new seekers {seekers} to the team")

def addFrozen(frozen):
  print(f"Adding new frozen players {frozen}")

def removeFrozen(frozen):
  print(f"Unfreezing frozen players {frozen}")

def updateScore(player, score):
  print(f"Player {player} increased its score to {score}")

def announceWin(team):
  print(f"Team '{team}' has won!! Congratulations!")
def finishGame(Game):
  print("Game has finished!")