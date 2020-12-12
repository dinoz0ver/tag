from FakeApi import getFreezeTimeout, getGameTimeout, getSeekerTimeout
import mcpi.minecraft as minecraft
from Utils import pp_timer

oldPrint = print
def newPrint(*args, **kwargs):
  mc.postToChat(*args, **kwargs)
  oldPrint(*args, **kwargs)
print = newPrint

mc = minecraft.Minecraft.create("192.168.1.44")

def getSeed():
  return None

def getPlayers():
  return mc.getPlayerNames()

def getSeekersSpawn():
  return (64, 139, 15) # коробка искателей

def getHidersSpawn():
  return (75, 140, 15) # вход в особняк

def createTeam(team, players):
  mc.teams.removeTeam(team)
  mc.teams.createTeam(team)
  for pl in players:
    mc.teams.addPlayer(team, pl)

def startMainGameTimer(tmr, to):
  print(f"§9 Игра начинается, до конца осталось {pp_timer(tmr, to)}с")

def startSeekerTimer(tmr, to):
  print(f"§9 Искатели будут выпущены на поле через {pp_timer(tmr, to)}с")

def startGame(Game):
  print("§3 Начинается игра в чай-чай-выручай!")
  for pl in Game.hiders:
    mc.player.makeVisible(pl)
    mc.player.makeInvisible(pl, Game.GAME_TIMEOUT)
    mc.setPos(pl, *Game.HIDERS_SPAWN)
    print(f"{pl} прячется!")
  for pl in Game.seekers:
    mc.setPos(pl, *Game.SEEKERS_SPAWN)
    print(f"{pl} ищет!")

def releaseSeekers(seekers):
  for skr in seekers:
    mc.setPos(skr, *getHidersSpawn())
  print("$9 Искатели выпущены на поле!")

def getPlayerHits():
  return mc.events.pollEntityHits()

def removeHiders(hiders):
  for hdr in hiders:
    mc.teams.removePlayer("hiders", hdr)
    print(f"§4 Игрок {hdr} больше не прячущийся")

def addSeekers(seekers):
  for skr in seekers:
    mc.teams.addPlayer("seekers", skr)
    print(f"§4 Игрок {skr} становится искателем!")

def addFrozen(frozen, timeout):
  for pl in frozen:
    mc.player.freeze(pl)
    mc.player.givePotionEffect(pl, "SLOW", timeout)
    print(f"§4 Игрок {pl} был заморожен!")

def removeFrozen(frozen):
  for pl in frozen:
    mc.player.unfreeze(pl)
    mc.player.removePotionEffect(pl, "SLOW")
    print(f"§4 Игрок {pl} был разморожен!")

def updateScore(player, score):
  print(f"§4 По {player} ударили {score} раз!")

def announceWin(team):
  if team == "seekers":
    print("Победа достается команде искателей! Хорошо всех заморозили")
  else:
    print("Победа команды прячущихся!")

def finishGame(Game):
  removeFrozen(Game.frozen)
  for pl in Game.players:
    mc.player.makeVisible(pl)
    mc.setPos(pl, *Game.HIDERS_SPAWN)
  print("§3 Игра окончена!")