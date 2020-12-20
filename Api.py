# from FakeApi import getFreezeTimeout, getGameTimeout, getSeekerTimeout
# DONE: нужно сбрасывать хиты перед началом игры
# DONE: спавн в лобби по окончании игры
# DONE: у искателей всегда алмазная броня и меч
# DONE: у хайдеров не бывает алмазного меча и брони
# DONE: новая команда set timeout <timeout>
# TO_CHECK: проверить, что ники игроков не видны другой команде
# TODO: rg на особняк, запретить строить

import mcpi.minecraft as minecraft
from Utils import pp_timer, parse_command
from datetime import datetime

oldPrint = print
def newPrint(msg):
  mc.postToChat(msg)
  dt_string = now = datetime.now().strftime("[%H:%M:%S]")
  oldPrint(f"{dt_string} {msg}")
print = newPrint

mc = minecraft.Minecraft.create("192.168.1.44")

def getSeed():
  return None

def getPlayers():
  return mc.getPlayerNames()

def getSeekersSpawn():
  return (65, 139, 15) # коробка искателей

def getHidersSpawn():
  return (47, 72, 12) # вход в особняк

def getLobbySpawn():
  return (48, 139, 21)

freeze_timeout = 40
def setFreezeTimeout(val):
  global freeze_timeout
  freeze_timeout = val
def getFreezeTimeout():
  return freeze_timeout

seeker_timeout = 30
def setSeekerTimeout(val):
  global seeker_timeout
  seeker_timeout = val
def getSeekerTimeout():
  return seeker_timeout

game_timeout = 300
def setGameTimeout(val):
  global game_timeout
  game_timeout = val

def getGameTimeout():
  return game_timeout

def createTeam(team, players):
  mc.teams.removeTeam(team)
  mc.teams.createTeam(team)
  if team == "hiders":
    mc.teams.setTeamProperties(team, canSeeFriendlyInvisibles=False, allowFF=True, nameTagVisibility="NEVER", collisionRule="FOR_OWN_TEAM")
  else:
    mc.teams.setTeamProperties(team, canSeeFriendlyInvisibles=False, allowFF=True, nameTagVisibility="ALWAYS", collisionRule="FOR_OWN_TEAM")
  for pl in players:
    mc.teams.addPlayer(team, pl)

def startMainGameTimer(tmr, to):
  print(f"§9Игра начинается, до конца осталось {pp_timer(tmr, to)}с")

def startSeekerTimer(tmr, to):
  print(f"§9Искатели будут выпущены на поле через {pp_timer(tmr, to)}с")

def clotheHider(hdr):
  chestplate = mc.player.getChestplate(hdr)
  if chestplate.type == "NULL" or chestplate.type == "DIAMOND_CHESTPLATE":
    mc.player.setChestplate(hdr, material="LEATHER_CHESTPLATE")
    print(f"§4[{hdr}] Игрок не одел нагрудник")
  helmet = mc.player.getHelmet(hdr)
  if helmet.type == "NULL" or helmet.type == "DIAMOND_HELMET":
    mc.player.setHelmet(hdr, material="LEATHER_HELMET")
    print(f"§4[{hdr}] Игрок не одел шлем")
  hand = mc.player.getItem(hdr, "HAND")
  if hand == "AIR" or hand == "DIAMOND_SWORD":
    mc.player.setItem(hdr, "HAND", "AIR")

def clotheSeeker(skr):
  mc.player.setChestplate(skr, material="DIAMOND_CHESTPLATE")
  mc.player.setHelmet(skr, material="DIAMOND_HELMET")
  mc.player.setItem(skr, "HAND", "DIAMOND_SWORD")

def getArmor(pl):
  return mc.player.getChestplate(pl), mc.player.getHelmet(pl)

def saveArmor(Game, hdr):
  Game.hidersArmor[hdr] = (mc.player.getChestplate(hdr), mc.player.getHelmet(hdr))

def loadArmor(Game, hdr):
  if hdr in Game.hidersArmor:
    chest, helmet = Game.hidersArmor[hdr]
    if chest.type != "NULL" and chest.type != "DIAMOND_CHESTPLATE":
      mc.player.setChestplate(hdr, armor=chest)
    if helmet.type != "NULL" and helmet.type != "DIAMOND_HELMET":
      mc.player.setHelmet(hdr, armor=helmet)

def checkHidersWearArmor(Game):
  for hdr in Game.hiders:
    clotheHider(hdr)

def startGame(Game):
  print("§3Начинается игра в чай-чай-выручай!")
  for pl in Game.hiders:
    mc.player.makeVisible(pl)
    mc.player.makeInvisible(pl, Game.GAME_TIMEOUT)
    mc.setPos(pl, *Game.HIDERS_SPAWN)
    mc.player.setGameMode(pl, "SURVIVAL")
    clotheHider(pl)
    saveArmor(Game, pl)
    print(f"{pl} прячется!")
  for pl in Game.seekers:
    mc.player.makeVisible(pl)
    mc.setPos(pl, *Game.SEEKERS_SPAWN)
    mc.player.setGameMode(pl, "SURVIVAL")
    saveArmor(Game, pl)
    clotheSeeker(pl)
    print(f"{pl} ищет!")
  mc.events.clearAll()

def releaseSeekers(seekers):
  for skr in seekers:
    mc.setPos(skr, *getHidersSpawn())
  print("§9Искатели выпущены на поле!")

def getPlayerHits():
  return mc.events.pollEntityHits()

def getProjectileHits():
  return mc.events.pollProjectileHits()

def slowPlayer(name):
  mc.player.givePotionEffect(name, "SLOW", 1, amplifier=1, ambient=True, particles=True)

def getCommands():
  cmds = mc.events.pollCommands()
  return list(map(parse_command, cmds))

def getPlayerExistence():
  return mc.events.pollPlayerExistence()

def onPlayerQuit(pl):
  pass
  # print(f"§8[{pl}] покидает нас")

def removeHiders(hiders):
  pass

def addSeekers(seekers):
  for skr in seekers:
    mc.teams.addPlayer("seekers", skr)
    mc.player.makeVisible(skr)
    clotheSeeker(skr)
    print(f"§4Игрок {skr} становится искателем!")

def addFrozen(frozen, timeout):
  for pl in frozen:
    mc.player.freeze(pl)
    mc.player.givePotionEffect(pl, "SLOW", timeout, amplifier=3)
    print(f"§4Игрок {pl} был заморожен!")

def removeFrozen(frozen):
  for pl in frozen:
    mc.player.unfreeze(pl)
    mc.player.removePotionEffect(pl, "SLOW")
    print(f"§4Игрок {pl} был разморожен")

def updateScore(player, score):
  print(f"§4По {player} ударили {score} раз!")

def announceWin(team):
  if team == "seekers":
    print("§6Победа достается команде искателей! Хорошо всех заморозили")
  else:
    print("§6Победа команды прячущихся!")

def finishGame(Game):
  resetAll(Game)
  print("§3Игра окончена!")

def addUnfreezers(unfreezers):
  for key in unfreezers:
    hdr, frz = key
    print(f"[{hdr}] размораживает {frz}")

def sendUnfreezeCount(hdr, frz, timePassed, timeTotal):
  frac = timePassed / timeTotal
  frac = int(frac*100)
  if frac > 100:
    frac = 100
  print(f"[{frz}] разморозка {frac}%")

def postToChat(msg):
  print(msg)

def resetAll(Game):
  removeFrozen(Game.frozen)
  for pl in Game.players:
    mc.setPos(pl, *getLobbySpawn())
    mc.player.makeVisible(pl)
    loadArmor(Game, pl)
  for team in ["hiders", "seekers"]:
    mc.teams.removeTeam(team)

