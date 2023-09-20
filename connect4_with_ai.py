import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board(): #এই ফাংশনটি একটি নতুন বোর্ড তৈরি করে এবং ফেরত দেয়। বোর্ডটি একটি নামপাই অ্যারে হিসাবে উপস্থাপিত হয়, যেখানে প্রতিটি সারি এবং কলাম একটি খেলার টুকরা রাখার জন্য একটি অবস্থান নির্দেশ করে।
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece): #এই ফাংশনটি নির্দিষ্ট সারি, কলাম এবং টুকরা নিয়ে বোর্ডে একটি টুকরা ফেলে।

	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col): #এই ফাংশনটি নির্দিষ্ট কলামে পরবর্তী খোলা সারিটি ফেরত দেয়। যদি কলামে কোনো খোলা সারি না থাকে, তবে ফাংশনটি None ফেরত দেয়।
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))  #এই ফাংশনটি বোর্ডটি প্রিন্ট করে। বোর্ডটিকে প্রিন্ট করার আগে, ফাংশনটি বোর্ডটিকে উল্টে দেয় যাতে এটি উপর থেকে নিচে প্রিন্ট হয়।

#এই ফাংশনটি নির্দিষ্ট টুকরার জন্য একটি জয়ী পদক্ষেপ আছে কিনা তা পরীক্ষা করে এবং ফেরত দেয়। এটি বোর্ডের সব সারি এবং কলামের উপর পুনরাবৃত্তি করে এবং কোনো নির্দিষ্ট সারিতে একই ধরনের চারটি টুকরা একসঙ্গে আছে কিনা তা পরীক্ষা করে। যদি ফাংশনটি একই ধরনের চারটি টুকরা একসঙ্গে খুঁজে পায়, তবে এটি True ফেরত দেয়। অন্যথায়, এটি False ফেরত দেয়।
def winning_move(board, piece): 
	# Check horizontal locations for win=====row
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win=======Column
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


# উদাহরণস্বরূপ, যদি উইন্ডোতে দেওয়া খেলোয়াড়ের ৪টি টুকরা থাকে, তাহলে ফাংশনটি নিম্নলিখিত স্কোর ফেরত করবে:

# স্কোর = ৪ * ৪ = ১৬
# যদি উইন্ডোতে দেওয়া খেলোয়াড়ের ৩টি টুকরা এবং ১টি খালি স্কোয়ার থাকে, তাহলে ফাংশনটি নিম্নলিখিত স্কোর ফেরত করবে:

# স্কোর = ৩ * ৪ = ১২
# যদি উইন্ডোতে দেওয়া খেলোয়াড়ের ২টি টুকরা এবং ২টি খালি স্কোয়ার থাকে, তাহলে ফাংশনটি নিম্নলিখিত স্কোর ফেরত করবে:

# স্কোর = ২ * ৪ = ৮
# যদি উইন্ডোতে প্রতিপক্ষের ৩টি টুকরা এবং ১টি খালি স্কোয়ার থাকে, তাহলে ফাংশনটি নিম্নলিখিত স্কোর ফেরত করবে:

# স্কোর = ৩ * ৪ - ৪ = ৮
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board) #ফাংশনটি বোর্ডে খালি স্কোয়ারগুলির তালিকা ফেরত করে।
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal: #যদি গেমটি শেষ হয়ে গেছে বা অনুসন্ধান গভীরতা শূন্য হয় তাহলে ফাংশনটি রিকার্সিভ কল থেকে ফেরত আসে।
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
# এই ফাংশনটি একটি এআই এজেন্টকে কোনো গেমে খেলার জন্য সেরা পদক্ষেপটি বেছে নিতে সাহায্য করে। এটি প্রথমে বোর্ডের সব বৈধ অবস্থানের একটি তালিকা পায়। তারপর, এটি সেরা পদক্ষেপের স্কোর এবং সেরা পদক্ষেপের কলামের জন্য দুটি ভেরিয়েবল তৈরি করে।
# এরপরে, ফাংশনটি বোর্ডের সব বৈধ অবস্থানের উপর পুনরাবৃত্তি করে। প্রতিটি অবস্থানের জন্য, ফাংশনটি বোর্ডের একটি কপি তৈরি করে এবং এজেন্টের টুকরাটি সেই অবস্থানে ড্রপ করে। তারপর, ফাংশনটি নতুন গেম বোর্ডটির স্কোর গণনা করে।
# যদি নতুন গেম বোর্ডের স্কোর বর্তমান সেরা স্কোরের চেয়ে বেশি হয়, তবে ফাংশনটি সেরা স্কোর এবং সেরা পদক্ষেপের কলাম আপডেট করে।
# ফাংশনটি বোর্ডের সব বৈধ অবস্থানের উপর পুনরাবৃত্তি করার পরে, এটি সেরা পদক্ষেপের কলাম ফেরত দেয়। এইটি হল এজেন্টের খেলার জন্য সেরা পদক্ষেপ।
	valid_locations = get_valid_locations(board)## বোর্ডের সব বৈধ অবস্থানের তালিকা 
 
 
## সেরা পদক্ষেপের স্কোর এবং সেরা পদক্ষেপের কলামের জন্য ভেরিয়েবল তৈরি 
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_board(board):
#এই দুটি লুপ বোর্ডের সব সারি এবং কলামের উপর পুনরাবৃত্তি করে এবং প্রতিটি সারি এবং কলামের জন্য একটি নীল রঙের বর্গ আঁকা হয়। তারপর, প্রতিটি সারি এবং কলামের জন্য একটি কালো রঙের বৃত্ত আঁকা হয়।

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

#এই দুটি লুপ বোর্ডের সব সারি এবং কলামের উপর পুনরাবৃত্তি করে এবং প্রতিটি সারি এবং কলামের জন্য, যদি সেই সারি এবং কলামে প্লেয়ারের টুকরা থাকে তবে একটি লাল রঙের বৃত্ত আঁকা হয় এবং যদি সেই সারি এবং কলামে এআইয়ের টুকরা থাকে তবে একটি হলুদ রঙের বৃত্ত আঁকা হয়।	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update() #এই লাইনটি পর্দা আপডেট করে যাতে নতুন বোর্ডটি প্রদর্শিত হয়।

board = create_board()
#কোডটি প্রথমে create_board() ফাংশনটি কল করে একটি নতুন বোর্ড তৈরি করে। 
print_board(board)
#তারপর, কোডটি print_board() ফাংশনটি কল করে বোর্ডটি প্রিন্ট করে।
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)  # 45 px

screen = pygame.display.set_mode(size)#এই কোডটি একটি নতুন পর্দা তৈরি করে যার আকার size ভেরিয়েবলটি দ্বারা নির্দেশ করা হয়। size ভেরিয়েবলটি বোর্ডের প্রস্থ এবং উচ্চতা নির্দেশ করে।
draw_board(board)
pygame.display.update() #এই কোডটি পর্দা আপডেট করে যাতে নতুন বোর্ডটি প্রদর্শিত হয়।

myfont = pygame.font.SysFont("monospace", 75)#ফাংশনটি দুটি প্যারামিটার গ্রহণ করে: ফন্টের নাম এবং ফন্টের আকার।

turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update() 



		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("You win!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		#col = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("AI wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)