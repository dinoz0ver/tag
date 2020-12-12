from threading import Thread
from FakeApi import HitQueue
from Game import *
from Utils import input
import time
import mcse.event


def CheckInput():
  try:
    time.sleep(0.1)
    while True:
      s = input("> ")
      if s == "hit":
        s1 = input("Кто ударил? ")
        s2 = input("Кого ударил? ")
        HitQueue.put(mcse.event.EntityEvent(s1, s2))
      elif s == "hithit":
        s1 = input("Кто ударил? ")
        s2 = input("Кого ударил? ")
        num = int(input("Сколько раз? "))
        for i in range(num):
          HitQueue.put(mcse.event.EntityEvent(s1, s2))
      time.sleep(0.1)
  except EOFError:
    pass


input_thread = Thread(target=CheckInput)
input_thread.daemon = True
input_thread.start()

Game = RealGame()
init(Game)
GameLoop(Game)