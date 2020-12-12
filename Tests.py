import unittest
from Logic import *
import time
random.seed(100500)

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
		players = [0,1,2,3,4,5]
		hits = 		[0,2,0,0,0,0]
		seekers = [0,2,3]
		hiders = 	[1,4,5]
		frozens = []
		timer = 	[]
		seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer)
		self.assertEqual(frozens, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		goToSeekers(seekers, hdr, frozens, timer)
		self.assertEqual(frozens, [], "1 was not unfrozen!")
		self.assertEqual(timer, [], "timers were not reset")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		self.assertEqual(seekers, [0,2,3,1], "Was not moved to seekers!")

	def testCheckTimer(self):
		timer = createTimer()
		timeout = 40
		self.assertFalse(checkTimer(timer, timeout), "Timer has timeouted!")
		timer = timer-41
		self.assertTrue(checkTimer(timer, timeout), "Timer has not timeouted!")

	def testExpiredList(self):
		timers = [createTimer(),createTimer()-41,createTimer(),createTimer()]
		timeout = 40
		i = findExpiredTimer(timers, timeout)
		self.assertEqual(i, 1)
		timers.pop(i)
		i = findExpiredTimer(timers, timeout)
		self.assertEqual(i, -1)

	def testSeekerHitHider1(self):
		skr = 0
		hdr = 1
		players = [0,1,2,3,4,5]
		hits = 		[0,2,0,0,0,0]
		seekers = [0,2,3]
		hiders = 	[1,4,5]
		frozens = []
		timer = 	[]
		seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer)
		self.assertEqual(frozens, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

	def testSeekerHitHider2(self):
		skr = 0
		hdr = 1
		players = [0,1,2,3,4,5]
		hits = 		[0,4,0,0,0,0]
		seekers = [0,2,3]
		hiders = 	[1,4,5]
		frozens = []
		timer = 	[]
		seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer)
		self.assertEqual(frozens, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,5,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")

	def testSeekerHitHider3(self):
		skr = 0
		hdr = 1
		players = [0,1,2,3,4,5]
		hits = 		[0,5,0,0,0,0]
		seekers = [0,2,3]
		hiders = 	[1,4,5]
		frozens = []
		timer = 	[]
		seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer)
		self.assertEqual(frozens, [], "1 was frozen!")
		self.assertEqual(hits, [0,6,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		self.assertEqual(seekers, [0,2,3,1], "Was not moved to seekers!")

	def testPhP(self):
		skr = 0
		hdr = 1
		players = [0,1,2,3,4,5]
		hits = 		[0,2,0,0,0,0]
		seekers = [0,2,3]
		hiders = 	[1,4,5]
		frozens = []
		timer = 	[]
		playerHitPlayer(skr, hdr, hiders, seekers, frozens, players, hits, timer)
		self.assertEqual(frozens, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")
		playerHitPlayer(4, 1, hiders, seekers, frozens, players, hits, timer)
		self.assertEqual(frozens, [], "1 was not unfrozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were reset!")
		self.assertEqual(hiders, [4,5,1], "Was not added to hiders!")
		self.assertEqual(timer, [], "timers were not reset")


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
