import pprint

pp = pprint.PrettyPrinter(indent=4)

class Game(object):
	"""This class maintains the state of a game."""
	def __init__(self, target = 11):
		super(Game, self).__init__()
		self._state = {
			'teams': {
				1: {'players': [], 'score': 0},
				2: {'players': [], 'score': 0}
			},
			'server': {
				'team': 1,
				'player': '',
				'serveCount': 1
			},
			'target': target,
			'winner': False
		}

	def setTarget(self, target):
		self._state.target = target

	def playerExists(self, id):
		for k in self._state['teams']:
			if id in self._state['teams'][k]['players']:
				return True
		return False

	def addPlayer(self, team, id):
		if len(self._state['teams'][1]['players']) == 0 and len(self._state['teams'][2]['players']) == 0:
			self._state['server']['team'] = team
			self._state['server']['player'] = id
			self._state['server']['serveCount'] = 1
		elif self.playerExists(id):
			raise Exception('User already registered', id)
		self._state['teams'][team]['players'].append(id)

	def getState(self):
		return self._state

	def addPoint(self, team):
		self._state['teams'][team]['score'] += 1
		# Do we have a winner?
		if self._state['teams'][1]['score'] >= self._state['target'] and self._state['teams'][2]['score'] < (self._state['target'] - 1):
			self._state['winner'] = 1
		elif self._state['teams'][2]['score'] >= self._state['target'] and self._state['teams'][1]['score'] < (self._state['target'] - 1):
			self._state['winner'] = 2
		else:
			# Are both teams at or beyond target-1?
			target = self._state['target'] - 1
			if self._state['teams'][1]['score'] > target and self._state['teams'][2]['score'] > target:
				# Is one team at least 2 beyond the other?
				if (self._state['teams'][1]['score'] - 2) >= self._state['teams'][2]['score']:
					self._state['winner'] = 1
				elif (self._state['teams'][2]['score'] - 2) >= self._state['teams'][1]['score']:
					self._state['winner'] = 2
				else:
					pass
			# else:
			# 	# Normal play. Advance the server.
			# 	if self._state['server']['serveCount'] == 2:


if __name__ == "__main__":
	game = Game()
	game.addPlayer(1, 'stuart')
	game.addPlayer(1, 'thomas')
	game.addPlayer(2, 'james')
	game.addPlayer(2, 'courtney')
	game.addPoint(1)
	pp.pprint(game.getState())
