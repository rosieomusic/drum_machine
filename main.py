import pygame
import sys
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 1400, 800

black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (170, 170, 170)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rosie's Beat Maker")
label_font = pygame.font.Font("alagard.ttf", 32)
medium_font = pygame.font.Font("alagard.ttf", 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 10
boxes = []
index = 100
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_channel = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
# file creation/loading
file = open("saved_beats.txt", "r")
for line in file:
    saved_beats.append(line)
beat_name = ""
typing = False

# load in sounds
hh = mixer.Sound("sounds/hh.wav")
oh = mixer.Sound("sounds/oh.wav")
crash = mixer.Sound("sounds/crash.wav")
shaker = mixer.Sound("sounds/shaker.wav")
h_tom = mixer.Sound("sounds/htom.wav")
m_tom = mixer.Sound("sounds/mtom.wav")
l_tom = mixer.Sound("sounds/ltom.wav")
clap = mixer.Sound("sounds/clap.wav")
snare = mixer.Sound("sounds/snare.wav")
kick = mixer.Sound("sounds/kick.wav")
pygame.mixer.set_num_channels(instruments + 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_channel[i] == 1:
            if i == 0:
                crash.play()
            if i == 1:
                shaker.play()
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


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    box_width = (WIDTH - 200) // beats
    box_height = (HEIGHT - 200) // instruments

    instrument_names = [
        "Crash",
        "Shaker",
        "OH",
        "HH",
        "H Tom",
        "M Tom",
        "F Tom",
        "Clap",
        "Snare",
        "Kick",
    ]
    for i, name in enumerate(instrument_names):
        label = label_font.render(name, True, colors[actives[i]])
        screen.blit(
            label,
            (30, i * 60 + 20),
        )

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 60) + 60), (200, (i * 60) + 60), 5)

    for i in range(beats):
        for j in range(instruments):
            x = i * box_width + 200 + 5
            y = j * box_height + 5
            if clicks[j][i] == 1:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            else:
                color = gray
            rect = pygame.draw.rect(
                screen, color, [x, y, box_width - 10, box_height - 10], 0, 3
            )
            pygame.draw.rect(
                screen, gold, [x, y, box_width - 10, box_height - 10], 5, 5
            )
            pygame.draw.rect(
                screen, black, [x, y, box_width - 10, box_height - 10], 2, 5
            )
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(
            screen,
            blue,
            [
                beat * ((WIDTH - 200) // beats) + 200,
                0,
                ((WIDTH - 200) // beats),
                instruments * 60,
            ],
            5,
            3,
        )
    return boxes


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render(
        "SAVE MENU: Enter a Name for Current Beat", True, white
    )
    saving_btn = pygame.draw.rect(
        screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100]
    )
    saving_text = label_font.render("Save Beat", True, white)
    screen.blit(saving_text, (WIDTH // 2 - 80, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, [400, 40])
    exit_btn = pygame.draw.rect(
        screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5
    )
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)

    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f"{beat_name}", True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = []
    loaded_bpm = []
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render("LOAD MENU: Select a Beat to Load:", True, white)
    loading_btn = pygame.draw.rect(
        screen, gray, [WIDTH // 2 - 200, HEIGHT - 100, 400, 90]
    )
    screen.blit(menu_text, [450, 40])
    loading_text = label_font.render("Load Beat", True, white)
    screen.blit(loading_text, (WIDTH // 2 - 80, HEIGHT - 70))
    delete_btn = pygame.draw.rect(
        screen, gray, [(WIDTH // 2) - 500, HEIGHT - 100, 180, 90], 0, 5
    )
    delete_text = label_font.render("Delete Beat", True, white)
    screen.blit(delete_text, ((WIDTH // 2) - 490, HEIGHT - 70))
    exit_btn = pygame.draw.rect(
        screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5
    )
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    exit_btn = pygame.draw.rect(
        screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5
    )
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loaded_rectangle = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 100 + index * 50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f"{beat + 1}", True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index("name: ") + 6
            name_index_end = saved_beats[beat].index(", beats:")
            name_text = medium_font.render(
                saved_beats[beat][name_index_start:name_index_end], True, white
            )
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(", bpm:")
            loaded_beats = int(saved_beats[beat][name_index_end + 8: beat_index_end])
            bpm_index_end = saved_beats[beat].index(", selected:")
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = loaded_clicks_rows[row].split(", ")
                for item in range(len(loaded_clicks_row)):
                    if (
                            loaded_clicks_row[item] == "1"
                            or loaded_clicks_row[item] == "-1"
                    ):
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    return exit_btn, loading_btn, delete_btn, loaded_rectangle, loaded_info


run = True
while run:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_channel)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render("Playing", True, dark_gray)
        screen.blit(play_text2, (70, HEIGHT - 100))
    else:
        play_text2 = medium_font.render("Paused", True, dark_gray)
        screen.blit(play_text2, (70, HEIGHT - 100))

    # bpm stuff
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = label_font.render("Tempo", True, white)
    screen.blit(bpm_text, (350, HEIGHT - 130))
    bpm_text2 = medium_font.render(f"{bpm}", True, white)
    screen.blit(bpm_text2, (375, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render("+5", True, white)
    sub_text = medium_font.render("-5", True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT - 90))

    # beats stuff
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render("Beats In Loop", True, white)
    screen.blit(beats_text, (618, HEIGHT - 130))
    beats_text2 = medium_font.render(f"{beats}", True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    beats_add_text = medium_font.render("+1", True, white)
    beats_sub_text = medium_font.render("-1", True, white)
    screen.blit(beats_add_text, (820, HEIGHT - 140))
    screen.blit(beats_sub_text, (820, HEIGHT - 90))
    # save and load
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (920, HEIGHT - 90))
    # clear board
    clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render("Clear Beat", True, white)
    screen.blit(clear_text, (1175, HEIGHT - 115))
    # instrument rects
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 60), (200, 60))
        instrument_rects.append(rect)

    if save_menu:
        exit_button, saving_button, entry_rect = draw_save_menu(beat_name, typing)

    if load_menu:
        exit_button, loading_button, delete_button, loaded_rect, loaded_info = (
            draw_load_menu(index)
        )

    # play sounds
    if beat_changed:
        play_notes()
        beat_changed = False
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                # print(boxes)
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
            elif not playing:
                playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True

            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_channel[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ""
                typing = False
            if load_menu:
                if loaded_rect.collidepoint(event.pos):
                    index = (event.pos[1] - 100) // 50
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_info[0]
                        bpm = loaded_info[1]
                        clicked = loaded_info[2]
                        index = 100
                        load_menu = False
            if save_menu:
                if entry_rect.collidepoint(event.pos):
                    if typing:
                        typing = False
                    elif not typing:
                        typing = True
                if saving_button.collidepoint(event.pos):
                    file = open("saved_beats.txt", "w")
                    saved_beats.append(
                        f"\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}"
                    )
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    typing = False
                    beat_name = ""

        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm
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
sys.exit()
