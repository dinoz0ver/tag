from threading import Thread
from Game import GameLoop, CheckInput

input_thread = Thread(target=CheckInput)
input_thread.daemon = True
input_thread.start()

GameLoop()