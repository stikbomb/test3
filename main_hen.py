import pygame

lvl1 = str(open('LVL1.txt', encoding="utf-8").read().strip()).split('\n')
lvl2 = str(open('LVL2.txt', encoding="utf-8").read().strip()).split('\n')
for el in range(len(lvl1)):
    lvl1[el] = lvl1[el].split(', ')
for el in range(len(lvl2)):
    lvl2[el] = lvl2[el].split(', ')

LEVELS = {'1': lvl1, '2': lvl2}

z_down = False
c_down = False


lvl_now = 1


def jump():
    global jump_count
    global is_jump
    global y
    global x
    global is_dash
    global can_jump
    if jump_count >= -10:
        if z_down and jump_count >= 0:
            y -= 2
        if jump_count < 0:
            y += (jump_count ** 2) / 4
        else:
            y -= (jump_count ** 2) / 4
        jump_count -= 1
        if keys[pygame.K_RIGHT]:
            x += dist
        elif keys[pygame.K_LEFT]:
            x -= dist
        if keys[pygame.K_c]:
            is_jump = False
            jump_count = 10
            is_dash = True
    else:
        is_jump = False
        jump_count = 10
        can_jump = False
    if check_place(x, y) == 'on the floor':
        is_jump = False
        jump_count = 10
        can_jump = True
        return


def dash():
    global dash_count
    global x
    global y
    global is_dash
    global can_dash
    global can_jump
    global is_fall
    if dash_count > 0:
        if (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]) or (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
            if can_dash:
                if keys[pygame.K_z]:
                    if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                        x -= (dash_count ** 2) / 1.5
                    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                        x += (dash_count ** 2) / 1.5
                    y -= 10
                    dash_count -= 0.5
        else:
            if keys[pygame.K_LEFT]:
                x -= (dash_count ** 2) / 3
            if keys[pygame.K_UP]:
                y -= (dash_count ** 2) / 3
            if keys[pygame.K_DOWN]:
                y += (dash_count ** 2) / 3
            if keys[pygame.K_RIGHT]:
                x += (dash_count ** 2) / 3
            dash_count -= 1
    else:
        dash_count = 10
        is_dash = False
        can_dash = False
        can_jump = False
        is_fall = True


def check_place(x_, y_):
    lvl = LEVELS[str(lvl_now)]
    if lvl[int(y_ // 20)][int(x_ // 20)].strip() == 'EXIT':
        return 'EXIT'
    x__, y__ = get_coords()
    try:
        ans = ''
        if lvl[int(y__ + 1)][int(x__)].strip() == 'FLOOR' and lvl[int(y__)][int(x__ + 1)].strip() == 'FLOOR' or\
            lvl[int(y__ + 1)][int(x__)].strip() == 'FLOOR' and lvl[int(y__)][int(x__ - 1)].strip() == 'FLOOR':
            ans += 'in the corner '
        w1 = lvl[int(y__)][int(x__) - 1].strip() == 'FLOOR'
        w2 = lvl[int(y__)][int(x__) + 1].strip() == 'FLOOR'
        if w1:
            ans += 'on the wall(L)'
        elif w2:
            ans += 'on the wall(R)'
        if ans:
            return ans
    except Exception:
        pass
    try:
        if y_ == 772 and (x == 0 or x_ == 780) or lvl[int(y__ + 1)][int(x__)].strip() == 'FLOOR' and\
                (x == 0 or x_ == 780):
            return 'in the corner'
    except Exception:
        pass
    try:
        if lvl[int(y__ + 1)][int(x__)].strip() == 'TRAP' or lvl[int(y__)][int(x__)].strip() == 'TRAP':
            return 'on the trap'
        if lvl[int(y__ + 1)][int(x__)].strip() == 'FLOOR':
            return 'on the floor'
        if lvl[int(y__ + 1)][int(x__ + 1)].strip() == 'FLOOR':
            print(place)
            return 'on the floor'
    except Exception:
        pass
    if y_ == 772:
        return 'on the floor'
    if x_ == 0 or x_ == 780:
        return 'on the wall'
    return 'fly'


def render_rect():
    for y_ in range(40):
        for x_ in range(40):
            if LEVELS[str(lvl_now)][y_][x_].strip() == 'FLOOR':
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (x_ * 20, y_ * 20, 20, 20), 0)
            elif LEVELS[str(lvl_now)][y_][x_].strip() == 'TRAP':
                pygame.draw.rect(screen, pygame.Color(255, 0, 0), (x_ * 20, y_ * 20, 20, 20), 0)
            elif LEVELS[str(lvl_now)][y_][x_].strip() == 'EXIT':
                pygame.draw.rect(screen, pygame.Color(0, 255, 0), (x_ * 20, y_ * 20, 20, 20), 0)


def check_coords(x_, y_):
    global r_down
    global deaths
    try:
        pos = LEVELS[str(lvl_now)][int(y_ // 20)][int(x_ // 20)].strip()
        pos_down = LEVELS[str(lvl_now)][int((y_ + 20) // 20)][int(x_ // 20)].strip()
        # print(pos)
        # print(place)
        # print(pos_down)

        if 'on the wall(R)' in place and pos == 'FLOOR':
            x_ = x_ // 20 * 20 - 19
            r_down = True

        if 'on the wall(L)' in place and pos == 'FLOOR':
            x_ = x_ // 20 * 20 + 20

        while pos_down != '0':
            y_ -= 1
            pos_down = LEVELS[str(lvl_now)][int((y_ + 20) // 20)][int(x_ // 20)].strip()
            # print(y_, pos_down)
        if LEVELS[str(lvl_now)][int((y_ + 20) // 20)][int(x_ // 20)].strip() == 'FLOOR':
            while LEVELS[str(lvl_now)][int((y_ + 20) // 20)][int(x_ // 20)].strip() != 0:
                y_ -= 1
        if place != 'on the floor':
            y_ += 1

        if place == 'on the floor' and pos == 'FLOOR':
            y_ = y_ // 20 * 21

        if place == 'on the trap':
            x_, y_ = 0, 760
            deaths += 1
    except Exception:
        pass
        # print((y_ + 20) // 20)
    if x_ > 780:
        x_ = 780
    elif x_ < 0:
        x_ = 0

    if y_ > 760:
        y_ = 760
    elif y_ < 0:
        y_ = 0
    if LEVELS[str(lvl_now)][int((y_ + 21) // 20)][int(x_ // 20)].strip() == 'FLOOR':
        y_ += 1

    return int(x_), int(y_)


def get_coords():
    # x_, y_ = event.pos
    return x // 20, y // 20


if __name__ == '__main__':
    deaths = 0
    pygame.init()
    font = pygame.font.SysFont(
        "Helvetica Neue,Helvetica,Ubuntu Sans,Bitstream Vera Sans,DejaVu Sans,Latin Modern Sans,Liberation Sans,Nimbus Sans L,Noto Sans,Calibri,Futura,Beteckna,Arial",
        16)
    pygame.display.set_caption('Обучение')

    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    can_dash = True
    can_jump = True
    z_down = False
    c_down = False
    r_down = False

    is_fall = False
    fall_count = 1
    is_jump = False
    jump_count = 10
    is_dash = False
    dash_count = 10

    walljumps_count = 2

    running = True
    coords = 0, 760
    dist = 10
    pygame.init()
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        x, y = coords
        place = check_place(x, y)
        print(can_jump)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not can_jump or not can_dash:
            place = check_place(x, y)
            if not can_jump and (place == 'on the floor' or 'in the corner' in place) and not z_down:
                can_jump = True
            if not can_dash and place == 'on the floor' or 'in the corner' in place and not c_down:
                can_dash = True

        keys = pygame.key.get_pressed()
        # print(LEVELS[str(lvl_now)][int(y // 20)][int(x // 20)].strip())
        if not keys[pygame.K_RIGHT]:
            r_down = False
        if z_down and not keys[pygame.K_z]:
            z_down = False
        elif c_down and not keys[pygame.K_c]:
            c_down = False
        if not is_jump and not is_dash:
            if not r_down:
                if keys[pygame.K_RIGHT] and place != 'on the wall':
                    x += dist
            if keys[pygame.K_LEFT] and place != 'on the wall':
                x -= dist
            if keys[pygame.K_z] and can_jump and not z_down:
                is_jump = True
            elif keys[pygame.K_c] and can_dash and not c_down:
                is_dash = True
        else:
            if is_jump:
                jump()
                z_down = True
            elif is_dash:
                dash()
                c_down = True

        if place in ['on the wall', 'on the wall(L)', 'on the wall(R)', 'fly'] and\
                (not is_dash and not is_jump):

            is_fall = True
            walls = ['on the wall', 'on the wall(L)', 'on the wall(R)']
            if place in walls or check_place(x + 1, y) in walls or check_place(x - 1, y) in walls:
                if not keys[pygame.K_x]:
                    if keys[pygame.K_RIGHT]:
                        x += dist
                    elif keys[pygame.K_LEFT]:
                        x -= dist
                    if place in ['on the wall(L)', 'on the wall(R)']:
                        y += (fall_count ** 2) / 24

                    fall_count += 1

                    if keys[pygame.K_z]:
                        if can_jump:
                            if walljumps_count > 0:
                                if jump_count >= 0:
                                    y -= (jump_count ** 2) / 4
                                    jump_count -= 1
                                else:
                                    jump_count = 10
                                    can_jump = True
                                walljumps_count -= 1
                            else:
                                can_jump = False
                                walljumps_count = 2
                    else:
                        if place != 'on the floor':
                            y += 1
            else:
                if place == 'fly' and (not is_dash and not is_jump):
                    y += (fall_count ** 2) / 7
                    fall_count += 0.6
        else:
            fall_count = 1
            is_fall = False

        if place == 'on the floor' and walljumps_count < 2:
            walljumps_count = 2
            can_dash = True
            can_jump = True
        if place == 'EXIT':
            # НИКОГДА БЛЯТЬ НЕ ПИШИТЕ ТАК КОД, ИЗУЧИТЕ ЬЛЯДСКИЕ СПРАЙТЫ
            if lvl_now < 3:
                deaths = 0
                lvl_now += 1
                coords = 0, 760
            else:
                break
        screen.fill(pygame.Color('black'))
        render_rect()
        checked_coords = check_coords(int(x), int(y))
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), (checked_coords, (20, 20)), 0)
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (checked_coords, (3, 3)), 0)
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), ((int(x) + 17, int(y)), (3, 3)), 0)
        coords = checked_coords
        message = f"Level:{lvl_now},   deaths:{deaths},    fps:{round(clock.get_fps(), 2)}"
        surf = font.render(message, True, (10, 255, 0))
        screen.blit(surf, (0, 0))
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()