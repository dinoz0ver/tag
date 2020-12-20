from queue import Queue
from Utils import parse_command

def getPlayers():
  return [f"{i+1} bruh" for i in range(5)]

def getFreezeTimeout():
  return 15

def getSeekerTimeout():
  return 15

def getGameTimeout():
  return 60

def getSeed():
  return 100500

def getSeekersSpawn():
  return getHidersSpawn()

def getHidersSpawn():
  return (75, 140, 15) # вход в особняк

def createTeam(name, players):
  print(f"Created team '{name}' with players {players}")

def startMainGameTimer(sec, to):
  print("Main game timer started")
  print("Giving everyone invisibility for xxx seconds")

def startGame(Game):
  print("started the Game, tp-ing hiders to hiders TP")

def startSeekerTimer(sec, to):
  print("started SeekerTimer")
  print("giving seekers some other effect for xx seconds")

def releaseSeekers(seekers):
  print("seekers have been released! hiders, be careful!")

def getSeekersSpawn():
  return getHidersSpawn()

def getHidersSpawn():
  return (75, 140, 15) # вход в особняк):

HitQueue = Queue()
def getPlayerHits():
  hits = []
  while not HitQueue.empty():
    hits.append(HitQueue.get())
  return hits

CmdQueue = Queue()
def getCommands():
  cmds = []
  while not CmdQueue.empty():
    cmds.append(parse_command(CmdQueue.get()))
  return cmds

def removeHiders(hiders):
  print(f"Removing hiders {hiders} from the team")

def addSeekers(seekers):
  print(f"Adding new seekers {seekers} to the team")

def addFrozen(frozen, to):
  print(f"Adding new frozen players {frozen}")

def removeFrozen(frozen):
  print(f"Unfreezing frozen players {frozen}")

def updateScore(player, score):
  print(f"Player {player} increased its score to {score}")

def announceWin(team):
  print(f"Team '{team}' has won!! Congratulations!")
def finishGame(Game):
  print("Game has finished!")

def addUnfreezers(unfreezers):
  for key in unfreezers:
    hdr, frz = key
    print(f"{hdr} размораживает {frz}")

def sendUnfreezeCount(hdr, frz, timePassed, timeTotal):
  frac = timePassed / timeTotal
  print(frac)
  frac = int(frac*100)
  if frac > 100:
    frac = 100
  print(f"[{frz}] разморозка {frac}%")