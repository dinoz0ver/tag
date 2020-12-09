import unittest
from GameLogic1 import *
random.seed(100500)

class TestStringMethods(unittest.TestCase):

	def testHitHiders1(self):
		hiders = [1,2,3,4]
		hits = hidersHitsAdd(hiders)
		self.assertEqual(hits, [0,0,0,0], "Hits are wrong")

	def testSplitPlayers1(self):
		players = [1,2,3,4,5]
		a, b = splitPlayers(players)
		self.assertEqual(a, [1,2,3,4])
		self.assertEqual(b, [5])

	def testSeekerHitHider(self):
		skr = 0
		hdr = 1
		players = 	[0,1,2,3,4,5]
		hits = 		[0,2,0,0,0,0]
		seekers = 	[0,2,3]
		hiders = 	[1,4,5]
		frozens = 	[]
		timer = 	[]
		seekerHitHider(skr, hdr, seekers, hiders, players, hits, frozens, timer)
		self.assertEqual(frozens, [1], "1 was not frozen!")
		self.assertEqual(hits, [0,3,0,0,0,0], "Hits were not reset!")
		self.assertEqual(hiders, [4,5], "Was not removed from hiders!")


	def testVictory1(self):
		seekers = [1,2,3,4,5]
		hiders = []
		frozen = [6, 7]
		self.assertFalse(seekersWon(seekers, hiders, frozen), "Seekers won, but hiders should have won!")
		self.assertTrue(hidersWon(seekers, hiders, frozen), "Hiders lost, but they should have won!")
		return True

if __name__ == '__main__':
	unittest.main()
