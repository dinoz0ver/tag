import time

DEBUG_FILE = False

old_input = input
def input(msg):
  s = old_input(msg)
  if DEBUG_FILE:
    print(s)
  return s

class Command: pass

def parse_arr(ar):
  x = Command()
  if len(ar) > 0:
    x.cmd = ar[0]
  else:
    x.cmd = ""
  if len(ar) > 1:
    x.args = ar[1:]
  else:
    x.args = []
  return x

def parse_command(cmd):
  if "/" not in cmd[0]:
    return parse_arr(cmd)
  args = cmd[0].split()
  x = Command()
  if args and args[0]:
    if args[0][0] == "/":
      args[0] = args[0][1:]
    x.cmd = args[0]
    x.args = args[1:]
  else:
    x.cmd = ""
    x.args = []
  return x

def pp_timer(start, to):
  x = to - int(time.time() - start)
  if x < 0:
    x = 0
  return f"{x}"