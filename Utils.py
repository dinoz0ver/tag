import time

DEBUG_FILE = False

old_input = input
def input(msg):
  s = old_input(msg)
  if DEBUG_FILE:
    print(s)
  return s


def pp_timer(start, to):
  x = to - int(time.time() - start)
  if x < 0:
    x = 0
  return f"{x}"