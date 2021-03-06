import pygame, sys, random 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (800,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (800,random_pipe_pos-800))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -100]
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		can_score = True
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

			
#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables 
gravity = 0.4
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/introhouse.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0



bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())


bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)



# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface) 
# bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while 60 > score:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 12
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 1:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		# Score
		pipe_score_check()
		score_display('main_game')
		#PUT ALL THE CHANGE IN BACKGROUNDS HERE aspect ratio is 288 x 512
		if  2 > score > 1:
			bg_surface = pygame.image.load('assets/introhouse.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 4 > score > 2:
			bg_surface = pygame.image.load('assets/housecomit.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 7 > score > 5:
			bg_surface = pygame.image.load('assets/sub.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 10 > score > 8:
			bg_surface = pygame.image.load('assets/fullcommit.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 14 > score > 11:
			bg_surface = pygame.image.load('assets/rules.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 16 > score > 15:
			bg_surface = pygame.image.load('assets/housefloor.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/nancy.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/nancy.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/nancy.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]
			bird_index = 0
			bird_surface = bird_frames[bird_index]
			BIRDFLAP = pygame.USEREVENT + 1
			pygame.time.set_timer(BIRDFLAP,200)
		if 19 > score > 17:
			bg_surface = pygame.image.load('assets/intosenate.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/nancy.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]
			bird_index = 0
			bird_surface = bird_frames[bird_index]
			BIRDFLAP = pygame.USEREVENT + 1
			pygame.time.set_timer(BIRDFLAP,200)
		if 22 > score > 20:
			bg_surface = pygame.image.load('assets/seninfacomit.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 25 > score > 23:
			bg_surface = pygame.image.load('assets/sensub.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 28 > score > 26:
			bg_surface = pygame.image.load('assets/fullsencomit.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 31 > score > 29:
			bg_surface = pygame.image.load('assets/senintrodebate.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/chuck.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/chuck.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/chuck.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]
			bird_index = 0
			bird_surface = bird_frames[bird_index]
			BIRDFLAP = pygame.USEREVENT + 1
			pygame.time.set_timer(BIRDFLAP,200)
		if 34 > score > 32:
			bg_surface = pygame.image.load('assets/confcomit.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bill.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]
			bird_index = 0
			bird_surface = bird_frames[bird_index]
			BIRDFLAP = pygame.USEREVENT + 1
			pygame.time.set_timer(BIRDFLAP,200)
		if 37 > score > 35:
			bg_surface = pygame.image.load('assets/confex.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 40 > score > 38:
			bg_surface = pygame.image.load('assets/houseapp.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 43 > score > 41:
			bg_surface = pygame.image.load('assets/senateapp.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 46 > score > 44:
			bg_surface = pygame.image.load('assets/filibust.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
		if 55 > score > 47:
			bg_surface = pygame.image.load('assets/prez.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/joe.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/joe.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/joe.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]
			bird_index = 0
			bird_surface = bird_frames[bird_index]
			BIRDFLAP = pygame.USEREVENT + 1
			pygame.time.set_timer(BIRDFLAP,200)
		if 59 > score > 56:
			bg_surface = pygame.image.load('assets/win.png').convert()
			bg_surface = pygame.transform.scale2x(bg_surface)


	#	if 16 > score > 14:
		#	bg_surface = pygame.image.load('assets/sub.png').convert()
		#	bg_surface = pygame.transform.scale2x(bg_surface)

	else:
		score = 0
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')
		


	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(75)


