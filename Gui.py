from Game import *
import Api as API

while True:
  for cmd in API.getCommands():
    if cmd.cmd == "trigger" and cmd.args[0] == "chai-event":
      # FIXME: у триггера может быть только один аргумент
      time = API.getGameTimeout()
      if len(cmd.args) > 1:
        time = int(cmd.args[1])
      print("Starting the game")
      Game = RealGame()
      init(Game, fake=False, gameTimeout=time)
      try:
        GameLoop(Game)
      except KeyboardInterrupt:
        Game.API.finishGame(Game)
    elif cmd.cmd == "set":
      if len(cmd.args) != 2:
        print("Failed to set, args:", cmd.args)
      key, value = cmd.args
      if key == "game_timeout":
        API.setGameTimeout(int(value))
        API.postToChat(f"Set new game timeout: {value}")
      elif key == "freeze_timeout":
        API.setFreezeTimeout(int(value))
        API.postToChat(f"Set new freeze timeout: {value}")
      elif key == "seeker_timeout":
        API.setSeekerTimeout(int(value))
        API.postToChat(f"Set new seeker timeout: {value}")

