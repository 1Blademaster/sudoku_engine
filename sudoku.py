import copy
import random


class Board:
	"""
	__init__ [code (optional): string]:
		Initilise the board object

	boardToCode [input_board (optional): list]:
		Convert a board represented by a list into a string representation

	findSpaces []:
		Finds the first empty space, represented by a 0, on the current board

	checkSpace [num: integer, space: tuple]:
		Returns a bool, depending if the number passed in can exist in a space on the current board, provided by the tuple argument

	solve []:
		Solves the current board using backtracking

	solveForCode []:
		Calls the solve method and returns the solved board in a string code format

	generateQuestionBoardCode [difficulty: integer]:
		Calls the generateQuestionBoard method and returns a question board and its solution in code format

	generateQuestionBoard [fullBoard: list, difficulty: integer]:
		Returns a randomly generated question board and the solution to the same board, the difficulty represents the number of number squares
		removed from the board

	__generateRandomCompleteBoard []:
		Returns a full randomly generated board

	__generateCont []:
		Uses recursion to finish generating a full board, whilst also making sure the board is solvable by calling the solve method

	findNumberOfSolutions []:
		Finds the number of solutions to the current board and returns a list of all the solutions in code format

	__findSpacesToFindNumberOfSolutions [board: list, h: integer]:
		Finds the first empty space in the board given as the argument, used within the findNumberOfSolutions method

	__solveToFindNumberOfSolutions [row: integer, col: interger]:
		Solves the current board using recursion by starting at the position determined by the row and col, used within the findNumberOfSolutions method

	__resetBoard []:
		Resets the current board to an empty state
	"""
	def __init__(self, code=None):
		self.__resetBoard()

		if code: # create a board from the code inputted
			self.code = code

			for row in range(9):
				for col in range(9):
					self.board[row][col] = int(code[0])
					code = code[1:]
		else:
			self.code = None

	
	def boardToCode(self, input_board=None): # turn a pre-existing board into a code
		if input_board:
			_code = ''.join([str(i) for j in input_board for i in j])
			return _code
		else:
			self.code = ''.join([str(i) for j in self.board for i in j])
			return self.code

	
	def findSpaces(self): # finds the first empty space in the board; where there is not a number
		for row in range(len(self.board)):
			for col in range(len(self.board[0])):
				if self.board[row][col] == 0:
					return (row, col)

		return False

	
	def checkSpace(self, num, space): #checks to see if a number can be fitted into a specifc space; row, col
		if not self.board[space[0]][space[1]] == 0: # check to see if space is a number already
			return False

		for col in self.board[space[0]]: # check to see if number is already in row
			if col == num:
				return False

		for row in range(len(self.board)): # check to see if number is already in column
			if self.board[row][space[1]] == num:
				return False

		_internalBoxRow = space[0] // 3
		_internalBoxCol = space[1] // 3

		for i in range(3): # check to see if internal box already has number
			for j in range(3):
				if self.board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
					return False
		
		return True

	
	def solve(self): # solves a board using recursion
		_spacesAvailable = self.findSpaces()

		if not _spacesAvailable:
			return True
		else:
			row, col = _spacesAvailable

		for n in range(1, 10):
			if self.checkSpace(n, (row, col)):
				self.board[row][col] = n
				
				if self.solve():
					return self.board

				self.board[row][col] = 0

		return False

	
	def solveForCode(self): # solves a board and returns the code of the solved board
		return self.boardToCode(self.solve())


	def generateQuestionBoardCode(self, difficulty): # generates a new random board and its board code depending on the difficulty
		self.board, _solution_board = self.generateQuestionBoard(self.__generateRandomCompleteBoard(), difficulty)
		return self.boardToCode(), self.boardToCode(_solution_board)


	def generateQuestionBoard(self, fullBoard, difficulty): # generates a question board with a certain amount of numbers removed depending on the chosen difficulty
			self.board = copy.deepcopy(fullBoard)
			
			print('[+] Generating board with {} difficulty'.format(difficulty))
			if difficulty == 0:
				_squares_to_remove = 36
			elif difficulty == 1:
				_squares_to_remove = 46
			elif difficulty == 2:
				_squares_to_remove = 52
			else:
				return

			_counter = 0
			while _counter < 4:
				_rRow = random.randint(0, 2)
				_rCol = random.randint(0, 2)
				if self.board[_rRow][_rCol] != 0:
					self.board[_rRow][_rCol] = 0
					_counter += 1

			_counter = 0
			while _counter < 4:
				_rRow = random.randint(3, 5)
				_rCol = random.randint(3, 5)
				if self.board[_rRow][_rCol] != 0:
					self.board[_rRow][_rCol] = 0
					_counter += 1

			_counter = 0
			while _counter < 4:
				_rRow = random.randint(6, 8)
				_rCol = random.randint(6, 8)
				if self.board[_rRow][_rCol] != 0:
					self.board[_rRow][_rCol] = 0
					_counter += 1

			_squares_to_remove -= 12
			_counter = 0
			while _counter < _squares_to_remove:
				_row = random.randint(0, 8)
				_col = random.randint(0, 8)

				if self.board[_row][_col] != 0:
					n = self.board[_row][_col]
					self.board[_row][_col] = 0

					if len(self.findNumberOfSolutions()) != 1:
						self.board[_row][_col] = n
						continue

					_counter += 1

			print('[+] Done generating board')
			return self.board, fullBoard


	def __generateRandomCompleteBoard(self): # generates a brand new completely random board full of numbers
			self.__resetBoard()

			_l = list(range(1, 10))
			for row in range(3):
				for col in range(3):
					_num = random.choice(_l)
					self.board[row][col] = _num
					_l.remove(_num)

			_l = list(range(1, 10))
			for row in range(3, 6):
				for col in range(3, 6):
					_num = random.choice(_l)
					self.board[row][col] = _num
					_l.remove(_num)

			_l = list(range(1, 10))
			for row in range(6, 9):
				for col in range(6, 9):
					_num = random.choice(_l)
					self.board[row][col] = _num
					_l.remove(_num)

			return self.__generateCont()


	def __generateCont(self): # uses recursion to finish generating a random board
		for row in range(len(self.board)):
			for col in range(len(self.board[row])):
				if self.board[row][col] == 0:
					_num = random.randint(1, 9)

					if self.checkSpace(_num, (row, col)):
						self.board[row][col] = _num

						if self.solve():
							self.__generateCont()
							return self.board

						self.board[row][col] = 0

		return False


	def findNumberOfSolutions(self): # finds the number of solutions to a board and returns the list of solutions
			_z = 0
			_list_of_solutions = []

			for row in range(len(self.board)):
				for col in range(len(self.board[row])):
					if self.board[row][col] == 0:
						_z += 1

			for i in range(1, _z+1):
				_board_copy = copy.deepcopy(self)

				_row, _col = self.__findSpacesToFindNumberOfSolutions(_board_copy.board, i)
				_board_copy_solution = _board_copy.__solveToFindNumberOfSolutions(_row, _col)

				_list_of_solutions.append(self.boardToCode(input_board=_board_copy_solution))

			return list(set(_list_of_solutions))
	
	
	def __findSpacesToFindNumberOfSolutions(self, board, h): # finds the first empty space it comes across, is used within the findNumberOfSolutions method
		_k = 1
		for row in range(len(board)):
			for col in range(len(board[row])):
				if board[row][col] == 0:
					if _k == h:
						return (row, col)

					_k += 1

		return False

	
	def __solveToFindNumberOfSolutions(self, row, col): # solves the board using recursion, is used within the findNumberOfSolutions method
		for n in range(1, 10):
			if self.checkSpace(n, (row, col)):
				self.board[row][col] = n

				if self.solve():
					return self.board

				self.board[row][col] = 0

		return False

	
	def __resetBoard(self): # resets the board to an empty state
		self.board = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
		]

		return self.board





if __name__ == '__main__':
	board = Board()

	question_board_code = board.generateQuestionBoardCode(1) # generates a medium level sudoku
	print(question_board_code[0])

	code = '300105000060200000008090060050000800800007040071009035000900084704006000902048300'
	solved_board_code = Board(code).solveForCode() # solves a hard level sudoku 
