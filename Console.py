from threading import Thread
from FakeApi import HitQueue
from Game import *
from Utils import input
import time
import mcpi.event


def CheckInput():
  try:
    time.sleep(0.1)
    prevS1, prevS2 = None, None
    while True:
      s = input("> ")
      if len(s.strip()) == 0 and prevS1 is not None and prevS2 is not None:
        HitQueue.put(mcpi.event.EntityEvent(prevS1, prevS2))
        print(f"hit {prevS1} {prevS2}")
      elif s == "hit":
        s1 = input("Кто ударил? ")
        s2 = input("Кого ударил? ")
        HitQueue.put(mcpi.event.EntityEvent(s1, s2))
        prevS1 = s1
        prevS2 = s2
      elif s == "hithit":
        s1 = input("Кто ударил? ")
        s2 = input("Кого ударил? ")
        num = int(input("Сколько раз? "))
        for i in range(num):
          HitQueue.put(mcpi.event.EntityEvent(s1, s2))
      time.sleep(0.1)
  except EOFError:
    pass


input_thread = Thread(target=CheckInput)
input_thread.daemon = True
input_thread.start()

Game = RealGame()
init(Game, fake=True)
GameLoop(Game)