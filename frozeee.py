# import mcpi.minecraft as minecraft
# import time
# import mcpi.block as block
# import random
# mc = minecraft.Minecraft.create()

# корды поля

X1 = 4445
Z1 = -788
Y1 = 74

X2 = 4526
Z2 = -723
Y2 = 109

timers = []
players = []


# функции

# def findExpiredTimer(timers, timeout=5):
# 	index = 0
# 	for start in timers:
# 		timePassed = int(time.time() - start)
# 		if timePassed > 5:
# 			return index
# 		index = index+1
# 	return -1

# def checkHit():
# 	events = mc.events.pollEntityHits()
# 	for a in events:
# 		pos = a.pos
# 		if pos.x>X1 and pos.x<X2 and pos.z>Z1 and pos.z<Z2 and pos.y>Y1 and pos.y<Y2:
# 			b = mc.getBlock(pos.x, pos.y, pos.z)
# 			if b == "DIAMOND_BLOCK":
# 				entities = [pos.x, pos.y, pos.z]
# 				boboboo.append(entities)
# 				timers.append(time.time())
# 				# mc.setBlock(pos.x, pos.y, pos.z, "GOLD_BLOCK")

# def checkCommand():
# 	posts = mc.events.pollChatPosts()
# 	for p in posts:
# 		print(p)

# сама прога

# while True:
# 	checkHit()
# 	checkCommand()
# 	index = findExpiredTimer(timers)
# 	if index != -1:
# 		timers.pop(index)
# 		entities = boboboo.pop(index)
# 		mc.setBlock(entities[0], entities[1], entities[2], "DIAMOND_BLOCK")