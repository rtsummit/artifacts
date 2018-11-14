#-*- coding: utf-8 -*-
from PIL import ImageGrab
from PIL import Image
import win32api, win32con
from time import sleep

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.SetCursorPos((300,300))

card_width = 105
card_height = 91

gap_width = 7
gap_height = 7

start_u = 27
start_v = 248

def get_card_info(im, i, show = False):
    height_idx = int(i / 3)
    width_idx = i % 3
    left = start_u + width_idx * (card_width + gap_width)
    right = left + card_width
    upper = start_v + height_idx * (card_height + gap_height)
    lower = upper + card_height

    card_im = im.crop((left, upper, right, lower))
    if show:
        card_im.show()

    info = []
    for t in card_im.getcolors(maxcolors=8192):
        # t = (count, color)
        if t[0] > 10:
            info.append(t)
    
    return info

def compare_card(card_info1, card_info2):
    diff_count = 0
    for count1, color1 in card_info1:
        has_same_color = False
        for count2, color2 in card_info2:
            if color1 == color2:
                has_same_color = True
                diff_count += abs(count1 - count2)
                break
        
        if not has_same_color:
            diff_count += count1
    
    return diff_count

def is_same_card(card_info_lhs, card_info_rhs):
    return compare_card(card_info_lhs, card_info_rhs) < 3000

#blank_card_info = [(88, (63, 63, 63, 255)), (39, (62, 62, 62, 255)), (3527, (61, 61, 61, 255)), (68, (74, 74, 73, 255)), (81, (66, 62, 59, 255)), (276, (100, 100, 100, 255)), (24, (99, 99, 99, 255)), (21, (98, 98, 98, 255)), (11, (26, 26, 26, 255)), (71, (25, 25, 25, 255)), (115, (37, 20, 4, 255)), (12, (83, 83, 83, 255)), (27, (80, 80, 80, 255)), (4411, (79, 79, 79, 255)), (56, (78, 78, 78, 255)), (44, (77, 77, 77, 255)), (90, (76, 76, 76, 255)), (16, (75, 75, 75, 255)), (23, (74, 74, 74, 255)), (20, (73, 73, 73, 255)), (19, (72, 72, 72, 255)), (19, (69, 69, 69, 255)), (12, (68, 68, 68, 255)), (20, (67, 67, 67, 255)), (20, (66, 66, 66, 255)), (88, (65, 65, 65, 255)), (23, (64, 64, 64, 255))]
blank_card_info = None

def is_blank_card(card_info):
    if blank_card_info is None:
        return False
    return is_same_card(blank_card_info, card_info)

# [[1, 2, 3, 8], [4, 5]] 이런 식
def get_same_card_set_list(im):
    same_card_set_list = []
    card_infos = [get_card_info(im, i) for i in range(0, 12)]
    for i in range(0, 11):
        already_check = False
        for s in same_card_set_list:
            if i in s:
                already_check = True
                break

        if already_check:
            continue

        card_info = card_infos[i]
        if is_blank_card(card_info):
            continue
        
        same_card_set = []
        for j in range(i + 1, 12):
            if is_same_card(card_info, card_infos[j]):
                if len(same_card_set) == 0:
                    same_card_set.append(i)
                same_card_set.append(j)

        if len(same_card_set) > 0:
            same_card_set_list.append(same_card_set)
    
    # blank_card_info = None 이라는 것 첫 턴이라는 것이고,
    #   첫 턴에는 blank_card 카드 아닌게 2개 뿐임.
    global blank_card_info
    if blank_card_info is None:
        if len(same_card_set_list[0]) > 2:
            blank_card_info = card_infos[same_card_set_list[0][0]]
            del same_card_set_list[0]
        else:
            blank_card_info = card_infos[same_card_set_list[1][0]]
            del same_card_set_list[1]
    
    return (same_card_set_list, card_infos)

def click_tile(i, offset = 0):
    height_idx = int(i / 3)
    width_idx = i % 3
    x = start_u + width_idx * (card_width + gap_width) + 0.5 * card_width
    y = start_v + height_idx * (card_height + gap_height) + 0.5 * card_height
    x += offset
    y += offset
    click(int(x / 1920 * 1536), int(y / 1080 * 864))

# im = ImageGrab.grab()

# get_card_info(im, 0)
# get_card_info(im, 2)
# get_card_info(im, 11)
#click_tile(11)

# 시작 버튼 위치
#click(204, 519)
#sleep(7)

input()
c = 0
im = None
prev_im = None
while c < 60:
    same_set_list = None
    card_infos = None
    while True:
        im = ImageGrab.grab()
        same_set_list, card_infos = get_same_card_set_list(im)

        has_odd = False
        for s in same_set_list:
            if len(s) % 2 != 0:
                has_odd = True
                break
        if False == has_odd:
            break

        print(same_set_list)
        print('Has odd. try again')
        sleep(0.01)

    print(same_set_list)
    click_count = 0
    for s in same_set_list:
        click_count += 1
        for idx in s:
            click_tile(idx)
            click_tile(idx, 10)
            click_tile(idx, -10)
            sleep(0.02)
            im = ImageGrab.grab()
            if is_blank_card(get_card_info(im, idx)):
                print("Not flipped. Click again. {0}".format(idx))
                sleep(0.02)
                click_tile(idx)
                im = ImageGrab.grab()
                if is_blank_card(get_card_info(im, idx)):
                    print("Not flipped. Click again. {0}".format(idx))
                    sleep(0.02)
                    click_tile(idx)
    
    sleep(0.65)
    c += 1

    cursor_pos = win32api.GetCursorPos()
    if cursor_pos[0] > 350 or cursor_pos[1] > 650:
        prev_im.show()
        break

    prev_im = im
    prev_same_set_list = same_set_list
    prev_card_infos = card_infos

# card_im = get_card_info(im, 0)
# card_im = get_card_info(im, 11)