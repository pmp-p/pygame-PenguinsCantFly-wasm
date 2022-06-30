import random

import pygame

pygame.init()
pygame.mixer.init()
WIDTH = 500
HEIGHT = 800
fps = 60
score = 0
timer = pygame.time.Clock()
font2 = pygame.font.Font('freesansbold.ttf', 24)
font = pygame.font.Font('assets/Terserah - Copy.ttf', 24)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (135, 206, 235)
# cloud - x pos, y pos, type
clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
cloud_images = []
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
player_x = 240
player_y = 20
direction = -1
y_speed = 0
gravity = .2
x_speed = 4
x_direction = 0
total_distance = 0
high_score = 0
game_over = False
pygame.mixer.music.load('assets/theme.mp3')
bounce = pygame.mixer.Sound('assets/bounce.mp3')
end_sound = pygame.mixer.Sound('assets/game_over.mp3')
'''pygame.mixer.music.play()'''
pygame.mixer.music.set_volume(.4)
penguin = pygame.transform.scale(pygame.image.load('assets/penguin.png'), (50, 50))
shark = pygame.transform.scale(pygame.image.load('assets/jetpack_shark.png'), (300, 200))
icon = pygame.transform.scale(penguin, (30, 30))
pygame.display.set_caption('Penguins Can\'t Fly')
pygame.display.set_icon(icon)
for i in range(1, 4):
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    cloud_images.append(img)


def draw_clouds(cloud_list, images):
    platforms = []
    for j in range(len(cloud_list)):
        image = images[cloud_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_list[j][0] + 5, cloud_list[j][1] + 40), (120, 10))
        '''screen.blit(image, (cloud_list[j][0], cloud_list[j][1]))'''
        pygame.draw.rect(screen, 'black', [cloud_list[j][0] + 10, cloud_list[j][1] + 40, 110, 3])
        platforms.append(platform)
    return platforms


def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    '''screen.blit(player_img, (x_pos, y_pos))'''
    player_rect = pygame.rect.Rect((x_pos + 7, y_pos + 47), (36, 10))
    pygame.draw.rect(screen, 'green', player_rect)
    return player_rect


def update_objects(cloud_list, play_y, speed, enemy_list):
    lowest_cloud = 0
    update_speed = 5
    if speed < 0 and play_y > 200:
        play_y -= update_speed
        for q in range(len(enemy_list)):
            enemy_list[q][1] -= update_speed
        for j in range(len(cloud_list)):
            cloud_list[j][1] -= update_speed
            if cloud_list[j][1] > lowest_cloud:
                lowest_cloud = cloud_list[j][1]
        if lowest_cloud < 750:
            num_clouds = random.randint(1, 2)
            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
            else:
                x_pos = random.randint(0, WIDTH / 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                x_pos2 = random.randint(WIDTH / 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2])
    return play_y, cloud_list, enemy_list


def draw_enemies(enemy_list, shark):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] + 20, enemy_list[j][1] + 50), (235, 70))
        pygame.draw.rect(screen, 'orange', enemy_rect, 5)
        enemy_rects.append(enemy_rect)
        '''if enemy_list[j][2] == 1:
            screen.blit(shark, (enemy_list[j][0], enemy_list[j][1]))
        if enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(shark, 1, 0), (enemy_list[j][0], enemy_list[j][1]))'''
    return enemy_rects


def move_enemies(enemy_list, score):
    enemy_speed = 2 + score//15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1
        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1
        if enemy_list[j][1] < - 100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)
    return enemy_list


run = True
while run:
    screen.fill(bg)
    timer.tick(fps)
    cloud_platforms = draw_clouds(clouds, cloud_images)
    player = draw_player(player_x, player_y, penguin, direction)
    enemy_boxes = draw_enemies(enemies, shark)
    enemies = move_enemies(enemies, score)
    player_y, clouds, enemies = update_objects(clouds, player_y, y_speed, enemies)
    if game_over:
        end_text = font.render('Game Over: Press Enter to Restart!', True, 'black')
        screen.blit(end_text, (50, 50))
        player_y = -100
        y_speed = 0
    for i in range(len(cloud_platforms)):
        if direction == -1 and player.colliderect(cloud_platforms[i]):
            if y_speed > 9:
                y_speed = 9
            y_speed *= -1
            '''bounce.play()'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                player_x = 240
                player_y = 20
                direction = -1
                y_speed = 0
                x_speed = 4
                x_direction = 0
                total_distance = 0
                '''pygame.mixer.music.play()'''

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0

    y_speed += gravity
    player_y += y_speed
    player_x += x_speed * x_direction
    if player_x > WIDTH:
        player_x = -30
    elif player_x < -50:
        player_x = WIDTH - 20

    if y_speed < 0:
        direction = 1
    else:
        direction = -1

    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            game_over = True
            '''end_sound.play()'''
    if player_y > 2000 and not game_over:
        game_over = True
        '''end_sound.play()'''

    total_distance += y_speed
    score = round(total_distance / 100)
    '''score_text = font.render(f'Score: {round(total_distance / 100)}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 70))
    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score: {round(high_score)}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 40))'''

    pygame.display.flip()
pygame.quit()
