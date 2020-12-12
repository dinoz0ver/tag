import unittest
from Logic import *
import time
random.seed(100500)

class TestGame: pass

class TestStringMethods(unittest.TestCase):

	def testFind(self):
		players = [1,2,3,4]
		self.assertTrue(is_seeker(1, players))
		self.assertTrue(is_hider(1, players))
		self.assertTrue(is_frozen(1, players))
		self.assertFalse(is_seeker(0, players))
		self.assertFalse(is_hider(0, players))
		self.assertFalse(is_frozen(0, players))

	def testHitHiders1(self):
		hiders = [1,2,3,4]
		hits = createPlayersHits(hiders)
		self.assertEqual(hits, [0,0,0,0], "Hits are wrong")

	def testSplitPlayers1(self):
		players = [1,2,3,4,5]
		a, b = splitPlayers(players)
		self.assertEqual(a, [1,2,3,4])
		self.assertEqual(b, [5])

	def testFreezeTimeout(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,2,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]
		seekerHitHider(skr, hdr, Game)
		self.assertEqual(frozen, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		goToSeekers(seekers, hdr, frozen, timers)
		self.assertEqual(frozen, [], "1 was not unfrozen!")
		self.assertEqual(timers, [], "timerss were not reset")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		self.assertEqual(seekers, [0,2,3,1], "Was not moved to seekers!")

	def testCheckTimers(self):
		timers = createTimer()
		timeout = 40
		self.assertFalse(checkTimer(timers, timeout), "Timers has timeouted!")
		timers = timers-41
		self.assertTrue(checkTimer(timers, timeout), "Timers has not timeouted!")

	def testExpiredList(self):
		timerss = [createTimer(),createTimer()-41,createTimer(),createTimer()]
		timeout = 40
		i = findExpiredTimer(timerss, timeout)
		self.assertEqual(i, 1)
		timerss.pop(i)
		i = findExpiredTimer(timerss, timeout)
		self.assertEqual(i, -1)

	def testSeekerHitHider1(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,2,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]
		seekerHitHider(skr, hdr, Game)
		self.assertEqual(frozen, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

	def testSeekerHitHider2(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,4,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]
		seekerHitHider(skr, hdr, Game)
		self.assertEqual(frozen, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,5,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

	def testSeekerHitHider3(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,5,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]

		seekerHitHider(skr, hdr, Game)
		self.assertEqual(frozen, [], "1 was frozen!")
		self.assertEqual(hits, [0,6,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		self.assertEqual(seekers, [0,2,3,1], "Was not moved to seekers!")

	def testPhP1(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,2,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]
		unfreezeTimers = Game.unfreezeTimers = 	{}
		playerHitPlayer(skr, hdr, Game)
		self.assertEqual(frozen, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

		Game.UNFREEZE_TIMEOUT = 3
		Game.HIT_TIMEOUT = 0.3
		playerHitPlayer(4, 1, Game)
		key = (4, 1)
		self.assertTrue(key in unfreezeTimers)
		unfreezeTimers[key]["hit"] -= (Game.HIT_TIMEOUT - 0.1)
		x1 = unfreezeTimers[key]["hit"]
		updateHitTiming(key[0], key[1], unfreezeTimers)
		x2 = unfreezeTimers[key]["hit"]
		self.assertNotEqual(x1, x2, "They are equal!")

		unfreezeTimers[key]["hit"] -= (Game.HIT_TIMEOUT + 1)
		checkEveryoneHitTiming(Game)
		self.assertNotIn(key, unfreezeTimers)

	def testPhP2(self):
		skr = 0
		hdr = 1
		Game = TestGame()
		players = Game.players = [0,1,2,3,4,5]
		hits = Game.hits = 		[0,2,0,0,0,0]
		seekers = Game.seekers = [0,2,3]
		hiders = Game.hiders = 	[1,4,5]
		frozen = Game.frozen = []
		timers = Game.timers = 	[]
		unfreezeTimers = Game.unfreezeTimers = 	{}
		playerHitPlayer(skr, hdr, Game)
		self.assertEqual(frozen, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

		Game.UNFREEZE_TIMEOUT = 3
		Game.HIT_TIMEOUT = 0.3
		playerHitPlayer(4, 1, Game)
		key = (4, 1)
		checkEveryoneHitTiming(Game)
		unfreezeTimers[key]["unfreeze"] -= (Game.UNFREEZE_TIMEOUT + 1)
		
		checkEveryoneHitTiming(Game)
		self.assertEqual(frozen, [], "1 was not unfrozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5,1], "Was not added to hiders!")
		self.assertEqual(timers, [], "timerss were not reset")
		

	def testPlayerHits(self):
		players = ["x", "y", "z", "a"]
		hits = [1,2,3,4]
		increasePlayerHits(players, hits, "x")
		self.assertEqual(hits, [2,2,3,4], "Hits are not equal!")
		increasePlayerHits(players, hits, "Foobar")
		self.assertEqual(hits, [2,2,3,4], "Hits are not equal!")

	def testVictory1(self):
		seekers = [1,2,3,4,5]
		hiders = []
		frozen = [6, 7]
		self.assertFalse(seekersWon(seekers, hiders, frozen), "Seekers won, but hiders should have won!")
		self.assertTrue(hidersWon(seekers, hiders, frozen), "Hiders lost, but they should have won!")

	def testVictory2(self):
		seekers = [1,2,3,4,5]
		hiders = [6,7]
		frozen = []
		self.assertFalse(seekersWon(seekers, hiders, frozen))
		self.assertTrue(hidersWon(seekers, hiders, frozen))

	def testVictory3(self):
		seekers = [1,2,3,4,5]
		hiders = []
		frozen = []
		self.assertTrue(seekersWon(seekers, hiders, frozen))
		self.assertFalse(hidersWon(seekers, hiders, frozen))

	def testVictory4(self):
		seekers = []
		hiders = []
		frozen = []
		self.assertFalse(seekersWon(seekers, hiders, frozen))
		self.assertFalse(hidersWon(seekers, hiders, frozen))


if __name__ == '__main__':
	unittest.main()
