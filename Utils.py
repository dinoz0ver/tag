DEBUG_FILE = False

old_input = input
def input(msg):
  s = old_input(msg)
  if DEBUG_FILE:
    print(s)
  return s