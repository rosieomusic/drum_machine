import pygame
from pygame import mixer
pygame.init()

WIDTH, HEIGHT = 1400, 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold =  (212, 175, 55)
blue =  (0, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rosie's Beat Maker")
label_font = pygame.font.Font('alagard.ttf', 32)
medium_font = pygame.font.Font('alagard.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 10
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

#load in sounds
hh = mixer.Sound('sounds/hh.wav')
oh = mixer.Sound('sounds/oh.wav')
crash = mixer.Sound('sounds/crash.aif')
ride = mixer.Sound('sounds/ride.wav')
h_tom = mixer.Sound('sounds/htom.aif')
m_tom = mixer.Sound('sounds/mtom.aif')
l_tom = mixer.Sound('sounds/ltom.aif')
clap = mixer.Sound('sounds/clap.wav')
snare = mixer.Sound('sounds/snare.aif')
kick = mixer.Sound('sounds/kick.aif')
pygame.mixer.set_num_channels(instruments + 3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                crash.play()
            if i == 1:
                ride.play()
            if i == 2:
                oh.play()
            if i == 3:
                hh.play()
            if i == 4:
                h_tom.play()
            if i == 5:
                m_tom.play()
            if i == 6:
                l_tom.play()
            if i == 7:
                clap.play()
            if i == 8:
                snare.play()
            if i == 9:
                kick.play()



def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    box_width = (WIDTH - 200) // beats
    box_height = (HEIGHT - 200) // instruments


    instrument_names = ["Crash", "Ride", "OH", "HH", "H Tom", "M Tom", "F Tom", "Clap", "Snare", "Kick"]
    for i, name in enumerate(instrument_names):
        label = label_font.render(name, True, white)
        screen.blit(label, (30, i * 60 + 20))


    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 60) + 60), (200, (i * 60) + 60), 5)


    for i in range(beats):
        for j in range(instruments):
            x = i * box_width + 200 + 5
            y = j * box_height + 5
            color = green if clicks[j][i] == 1 else gray
            rect = pygame.draw.rect(screen, color, [x, y, box_width - 10, box_height - 10], 0, 3)
            pygame.draw.rect(screen, gold, [x, y, box_width - 10, box_height - 10], 5, 5)
            pygame.draw.rect(screen, black, [x, y, box_width - 10, box_height - 10], 2, 5)
            boxes.append((rect, (i, j)))

        active =  pygame.draw.rect(screen,blue, [beat * ((WIDTH - 200) // beats) + 200, 0,((WIDTH - 200) // beats), instruments * 60], 5, 3)
    return boxes

run = True

while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0 ,5)
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
        screen.blit(play_text2, (70, HEIGHT - 100))
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
        screen.blit(play_text2, (70, HEIGHT - 100))

    #bpm stuff
    bpm_rect = pygame.draw.rect(screen,gray,[300, HEIGHT - 150, 200, 100],5,5)
    bpm_text = label_font.render("Tempo", True, white)
    screen.blit(bpm_text, (350, HEIGHT - 130))
    bpm_text2 = medium_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (375, HEIGHT - 100))

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                #print(boxes)
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

    beat_length = 3600 //bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True


    pygame.display.flip()
pygame.quit()