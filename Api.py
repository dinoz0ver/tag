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
  print(f"§4 В игрока {player} ударили {score} раз!")

def announceWin(team):
  print(f"§3 Команда {team} победюла!! Мои поздравления")

def finishGame(Game):
  removeFrozen(Game.frozen)
  for pl in Game.players:
    mc.player.makeVisible(pl)
  print("§3 Игра окончена!")