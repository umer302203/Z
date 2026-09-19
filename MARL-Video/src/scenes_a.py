#!/usr/bin/env python3
"""Scenes A: 0-348.8s — football, RL loop, maze, MARL, comp/coop, nonstat, credit, delayed, partial-obs, apps."""
import numpy as np
from engine import (W, H, draw_circle, draw_line, draw_arrow, draw_rect, draw_text,
                    draw_polyline, draw_poly_fill, ease, ramp, clamp01, fade,
                    BLUE, RED, GREEN, GOLD, PURPLE, WHITE, GREY, ORANGE, TEAL, BLUE_D)
from kit import (agent_node, chip, chip_box, robot_icon, drone_icon, flag, ball, view_cone,
                 meter, vs_divider, cross, check, pulse_ring, brain_icon, mini_net, box_icon,
                 clock_icon, shield_icon, lock_icon, human_icon, grid_world, fx_slice, glow)

def L(t, t0, dur, a, b, m="inout"):
    return a + (b - a) * ramp(t, t0, dur, m)

# ============ SCENE 1: FOOTBALL (0 - 19.9) ============
def sc_football(f, t, A):
    fx0, fy0, fx1, fy1 = 240, 300, 1680, 940
    fa = ramp(t, 0.30, 0.9)
    draw_rect(f, fx0, fy0, fx1, fy1, (46, 92, 60), 0.5*fa, width=3, radius=26)
    draw_line(f, ((fx0+fx1)/2, fy0+12), ((fx0+fx1)/2, fy1-12), WHITE, 2.5, 0.55*fa)
    draw_circle(f, (fx0+fx1)/2, (fy0+fy1)/2, 92, WHITE, 0.5*fa, width=2.5)
    draw_rect(f, fx0, (fy0+fy1)/2-130, fx0+150, (fy0+fy1)/2+130, WHITE, 0.12*fa, width=2.5, radius=8)
    draw_rect(f, fx1-150, (fy0+fy1)/2-130, fx1, (fy0+fy1)/2+130, WHITE, 0.12*fa, width=2.5, radius=8)

    blue = [(320,620),(510,430),(510,810),(650,620),(790,400),(790,840),(700,620),(930,450),(930,790),(1010,620),(860,620)]
    red  = [(1600,620),(1410,430),(1410,810),(1270,620),(1130,400),(1130,840),(1230,620),(1040,530),(1040,710),(990,620),(1090,620)]
    hero = blue[6]

    for i, (x, y) in enumerate(blue):
        t0 = 4.2 + i*0.14
        c = BLUE
        if i == 6:
            agent_node(f, x, y, t, t0, c, 17, pulse=max(0, np.sin((t-6.5)*2.2))*0.5 if t > 6.5 else 0)
        else:
            near = i in (3, 5, 10) and t > 8.0
            agent_node(f, x, y, t, t0, c, 13 if not near else 15)
    for i, (x, y) in enumerate(red):
        t0 = 5.2 + i*0.14
        opp = i in (5, 7, 9, 10) and t > 8.8
        agent_node(f, x, y, t, t0, RED, 13 if not opp else 15)

    # highlight labels
    if t > 7.2:  chip(f, "POSITION", hero[0], hero[1]-64, t, 7.24, GOLD, 24)
    if t > 8.0:  chip(f, "TEAMMATES", 700, 400, t, 8.04, BLUE, 24)
    if t > 8.8:  chip(f, "OPPONENTS", 1130, 340, t, 8.84, RED, 24)

    # decision fan (10.4)
    if t > 10.36:
        a = ramp(t, 10.36, 0.6)
        for ang in (-0.55, 0.0, 0.55):
            ex, ey = hero[0]+np.cos(ang)*150, hero[1]+np.sin(ang)*150
            draw_line(f, hero, (ex, ey), WHITE, 2.5, 0.6*a, dash=14)
            draw_circle(f, ex, ey, 5, WHITE, 0.8*a)
    # pass (13.3)
    if t > 13.0:
        tgt = blue[3]
        p = ramp(t, 13.34, 0.9)
        bx, by = L(t, 13.34, 0.9, hero[0], tgt[0]), L(t, 13.34, 0.9, hero[1], tgt[1])
        ball(f, bx, by, 9, WHITE, min(1, 2*ramp(t, 13.0, 0.3)))
        if t < 14.4:
            draw_line(f, hero, tgt, GOLD, 2.5, 0.5*(1-p)+0.15, dash=16)
    else:
        ball(f, hero[0]+26, hero[1]+18, 8, WHITE, ramp(t, 5.8, 0.4))

    # cover (14.5): two blues shift
    cv1 = (L(t, 14.46, 1.1, 650, 780), L(t, 14.46, 1.1, 620, 500))
    cv2 = (L(t, 14.70, 1.1, 790, 900), L(t, 14.70, 1.1, 840, 700))
    if t > 14.46:
        agent_node(f, cv1[0], cv1[1], t, 14.46, BLUE, 14)
        agent_node(f, cv2[0], cv2[1], t, 14.70, BLUE, 14)

    # attack (16.3)
    if t > 16.26:
        a = ramp(t, 16.26, 0.5)
        draw_arrow(f, (960, 620), (1560, 620), GOLD, 4, 0.85*a, head=20)
        for i, (x0, y0) in enumerate([(930,450),(1010,620),(930,790)]):
            ax = L(t, 16.26, 1.4, x0, x0+260)
            agent_node(f, ax, y0, t, 4.2+i*0.14, BLUE, 14)
    # result (18.0)
    if t > 18.0:
        a = ramp(t, 18.02, 0.5)
        pulse_ring(f, 1600, 620, t, 18.02, GOLD, 20, 90, 0.9)
        chip(f, "BETTER RESULT", 1480, 240, t, 18.02, GOLD, 30)
        check(f, 1290, 240, 16, t, 18.3, GREEN)

# ============ SCENE 2: PROGRAMS / MARL TITLE (19.9 - 26.1) ============
def sc_programs(f, t, A):
    # dim field ghost
    fa = 1 - ramp(t, 19.94, 1.2)
    if fa > 0:
        draw_rect(f, 240, 300, 1680, 940, (46, 92, 60), 0.22*fa, width=2, radius=26)
        draw_line(f, (960, 312), (960, 928), WHITE, 2, 0.3*fa)
    # players morph to chips
    pts = [(700,620),(790,400),(790,840),(930,450),(1010,620)]
    for i, (x, y) in enumerate(pts):
        t0 = 20.3 + i*0.18
        a = ramp(t, t0, 0.5, "back")
        if a <= 0: continue
        s = 20*a
        draw_rect(f, x-s, y-s, x+s, y+s, BLUE, 0.4*a, width=2.5, radius=5)
        for k in range(3):
            draw_circle(f, x-8+k*8, y, 2.5, WHITE, 0.8*a)
    if t > 21.4 and t < 23.35:
        a = fade(t, 21.4, 23.35, 0.35, 0.4)
        chip(f, "COMPUTER PROGRAMS", 960, 460, t, 21.4, BLUE, 30, alpha=a)
    # title lockup 23.8
    if t > 23.4:
        a = ramp(t, 23.4, 0.7)
        draw_rect(f, 460, 380, 1460, 700, (18, 24, 34), 0.9*a, width=2, radius=18)
        draw_line(f, (700, 540), (760, 540), GOLD, 0, 0)  # noop keep
        draw_text(f, "MULTI-AGENT", 960, 470, 58, BLUE, a)
        draw_text(f, "REINFORCEMENT", 960, 545, 58, WHITE, a)
        draw_text(f, "LEARNING", 960, 620, 58, GOLD, a)
        draw_line(f, (700, 385), (1220, 385), BLUE, 3, 0.8*a)
        draw_line(f, (700, 695), (1220, 695), BLUE, 3, 0.8*a)

# ============ SCENE 3: RL LOOP (26.1 - 46.7) ============
def sc_rl_loop(f, t, A):
    ax, ay = 560, 560
    ex, ey = 1360, 560
    # agent
    aa = ramp(t, 26.1, 0.6, "back")
    if aa > 0:
        brain_icon(f, ax, ay, 30, t, 26.1, PURPLE)
        chip(f, "AGENT", ax, ay+86, t, 26.5, PURPLE, 28)
    # environment
    ea = ramp(t, 31.76, 0.7, "back")
    if ea > 0:
        draw_rect(f, ex-190, ey-130, ex+190, ey+130, (40, 50, 68), 0.55*ea, width=3, radius=16)
        grid_world(f, ex-170, ey-110, ex+170, ey+110, 6, t, 31.9, 0.4*ea)
        chip(f, "ENVIRONMENT", ex, ey+170, t, 32.3, BLUE, 28)
        # little obstacles
        draw_rect(f, ex-120, ey-60, ex-60, ey-10, GREY, 0.5*ea, width=0, radius=4)
        draw_rect(f, ex+40, ey+20, ex+120, ey+70, GREY, 0.5*ea, width=0, radius=4)
    # observation arrow (env->agent, bottom)
    if t > 36.38:
        oa = ramp(t, 36.38, 0.6)
        draw_arrow(f, (ex-190, ey+170), (ax+120, ey+170), BLUE, 4.5, 0.9*oa, head=20)
        chip(f, "OBSERVATION", 960, ey+225, t, 36.7, BLUE, 25)
    # action arrow (agent->env, top)
    if t > 37.9:
        aa2 = ramp(t, 37.9, 0.6)
        draw_arrow(f, (ax+110, ey-170), (ex-190, ey-170), ORANGE, 4.5, 0.9*aa2, head=20)
        chip(f, "ACTION", 960, ey-225, t, 38.2, ORANGE, 25)
    # reward arc (env->agent) 40.3
    if t > 40.3:
        ra = ramp(t, 40.3, 0.6)
        pts = [(ex-160, ey-60), (960, ey+40), (ax+150, ey-40)]
        draw_polyline(f, pts, GOLD, 4, 0.9*ra)
        draw_arrow(f, (ax+210, ey-52), (ax+150, ey-40), GOLD, 4, 0.9*ra, head=16)
        pen = 40.9 <= t <= 43.1
        col = RED if pen else GOLD
        chip(f, "PENALTY" if pen else "REWARD", 960, ey+95, t, 40.3 if not pen else 40.9, col, 25)
    # learning pulses 43.3
    if t > 43.26:
        cyc = (t - 43.26) % 1.6
        for tt in (36.38, 37.9, 40.3):
            pass
        p = cyc / 1.6
        glow(f, ax, ay, 26, PURPLE, 0.4*(1-p))
        chip(f, "AGENT LEARNS", ax, ay-110, t, 43.26, GREEN, 26)
        # flowing dash on observation
        draw_circle(f, 960 + np.cos(t*2.4)*430*0.0, ey+170, 6, BLUE, 0.9, ) if False else None

# ============ SCENE 4: MAZE (46.7 - 55.2) ============
def sc_maze(f, t, A):
    mx0, my0, mx1, my1 = 640, 280, 1280, 900
    ma = ramp(t, 46.72, 0.7)
    walls = [
        [(mx0, my0), (mx1, my0)], [(mx0, my1), (mx1, my1)], [(mx0, my0), (mx0, my1)],
        [(mx1, my0), (mx1, my1)],
        [(mx0, my0+155), (mx0+230, my0+155)], [(mx0+230, my0+155), (mx0+230, my0+310)],
        [(mx0+390, my0+310), (mx1-60, my0+310)], [(mx0+390, my0+155), (mx0+390, my0+465)],
        [(mx0+230, my1-140), (mx1-210, my1-140)],
    ]
    for i, w in enumerate(walls):
        a = ramp(t, 46.8 + i*0.09, 0.3)
        draw_line(f, w[0], w[1], WHITE, 5, 0.85*a)
    draw_rect(f, mx0, my0, mx1, my1, (30, 38, 52), 0.5*ma, width=0, radius=6)
    for i, w in enumerate(walls):
        a = ramp(t, 46.8 + i*0.09, 0.3)
        draw_line(f, w[0], w[1], WHITE, 5, 0.85*a)
    # exit
    if t > 48.4:
        fa = ramp(t, 48.4, 0.5, "back")
        flag(f, mx1-40, my1-60, t, 48.4, GREEN, 26)
        chip(f, "EXIT", mx1-70, my1-16, t, 48.6, GREEN, 22)
    # robot path
    path = [(mx0+70, my0+80), (mx0+160, my0+80), (mx0+160, my0+240), (mx0+80, my0+240)]
    # hit wall at ~50.9 at (mx0+160, my0+155)
    if t < 50.88:
        rx = L(t, 48.6, 2.2, mx0+70, mx0+160)
        ry = L(t, 48.6, 2.2, my0+80, my0+80)
        robot_icon(f, rx, ry, t, 48.4, BLUE, 13, dirx=1)
    elif t < 52.2:
        # bump + flash
        rx = mx0+160
        ry = L(t, 50.95, 0.35, my0+80, my0+95, "out")
        robot_icon(f, rx, ry, t, 48.4, BLUE, 13)
        if t < 51.6:
            a = 1 - ramp(t, 50.95, 0.55)
            draw_circle(f, rx+16, ry-6, 26*(1-a)+14, RED, 0.55*a, width=3)
            chip(f, "PENALTY", rx+150, ry+4, t, 51.0, RED, 24)
    else:
        # reroute downward then right along bottom, exit
        p = ramp(t, 52.2, 1.6)
        if p < 0.45:
            rx, ry = mx0+160, L(t, 52.2, 0.75, my0+95, my0+430)
        else:
            rx, ry = L(t, 52.95, 1.2, mx0+160, mx1-70), my0+430
            ry = my0+430
        robot_icon(f, rx, ry, t, 48.4, BLUE, 13, dirx=1 if p >= 0.45 else 0, diry=1 if p < 0.45 else 0)
        if t > 53.4:
            pulse_ring(f, mx1-40, my1-60, t, 53.5, GREEN, 14, 60, 0.8)
    # many agents (53.8)
    if t > 53.76:
        for i, (dx, dy) in enumerate([(-60, 120), (-140, -60), (60, 180)]):
            a = ramp(t, 53.9+i*0.2, 0.5, "back")
            if a > 0:
                x, y = mx0+160+dx, my0+240+dy
                draw_circle(f, x, y, 12, TEAL, 0.8*a)
                glow(f, x, y, 12, TEAL, 0.5*a)

# ============ SCENE 5: MARL SHARED ENV (55.2 - 86.1) ============
def sc_marl(f, t, A):
    chip(f, "MARL", 960, 170, t, 55.18, GOLD, 40)
    # shared environment field
    ea = ramp(t, 55.4, 0.8)
    draw_rect(f, 480, 300, 1440, 900, (40, 50, 68), 0.45*ea, width=3, radius=20)
    grid_world(f, 480, 300, 1440, 900, 10, t, 55.5, 0.35*ea)
    agents = [(700, 470, BLUE), (1220, 470, TEAL), (700, 750, PURPLE), (1220, 750, ORANGE)]
    names = ["AGENT 1", "AGENT 2", "AGENT 3", "AGENT 4"]
    # obstacles shift at 73.8
    ob1 = (L(t, 73.78, 1.2, 880, 980), L(t, 73.78, 1.2, 560, 640))
    for tt, ox, oy in [(55.9, 880, 560), (73.78, ob1[0], ob1[1])]:
        pass
    # draw moving obstacle
    if t > 55.9:
        ox = L(t, 73.78, 1.2, 880, 1000)
        oy = L(t, 73.78, 1.2, 570, 650)
        draw_rect(f, ox-45, oy-25, ox+45, oy+25, GREY, 0.55, width=0, radius=6)
    if t > 75.48:
        # walls/roads icons flash
        a = fade(t, 75.48, 79.0, 0.3, 0.4)
        draw_rect(f, 560, 330, 700, 370, WHITE, 0.4*a, width=0, radius=4)
        draw_line(f, (520, 880), (900, 880), GREY, 6, 0.5*a)
        draw_line(f, (500, 860), (500, 900), GOLD, 4, 0.6*a)
        draw_line(f, (940, 860), (940, 900), GOLD, 4, 0.6*a)
    for i, (x, y, c) in enumerate(agents):
        t0 = 55.5 + i*0.25
        # positions shift at 69.2 (others act)
        dx = dy = 0
        if t > 69.16:
            dx = 40*np.sin(i*1.7 + (t-69.16)*0.9) * ramp(t, 69.16, 2.0)
            dy = 34*np.cos(i*2.1 + (t-69.16)*0.9) * ramp(t, 69.16, 2.0)
        agent_node(f, x+dx, y+dy, t, t0, c, 18)
        draw_text(f, names[i], x+dx, y+dy+44, 19, WHITE, 0.85)
        # observation cone 60.06
        if t > 60.06:
            ang = np.arctan2(600-(y+dy), 960-(x+dx))
            view_cone(f, x+dx, y+dy, ang, 0.9, 150, t, 60.06+i*0.1, c)
    if t > 60.06:
        # exit before policy rule card enters at 65.16 (no overlap, clean lifecycle)
        ca = 1.0 - ramp(t, 64.7, 0.4) if t > 64.7 else 1.0
        chip(f, "OBSERVATION", 960, 970, t, 60.1, BLUE, 26, alpha=ca)
    # policy chips 62.44
    if t > 62.44:
        for i, (x, y, c) in enumerate(agents):
            chip(f, "POLICY", x, y-52, t, 62.44+i*0.15, c, 20)
    # policy rule card 65.16
    if t > 65.16:
        a = ramp(t, 65.16, 0.5)
        draw_rect(f, 620, 940, 1300, 1030, (24, 30, 42), 0.92*a, width=2, radius=12)
        draw_text(f, "POLICY = RULE :  STATE  ->  ACTION", 960, 985, 30, WHITE, 0.95*a)
    # decisions mesh 79.12
    if t > 79.12:
        a = ramp(t, 79.12, 0.8)
        pairs = [(0,1),(0,2),(1,3),(2,3),(0,3),(1,2)]
        for i, (a1, a2) in enumerate(pairs):
            p1 = agents[a1][:2]; p2 = agents[a2][:2]
            draw_line(f, p1, p2, PURPLE, 2, 0.4*a, dash=12)
    if t > 79.12: chip(f, "INTELLIGENT DECISIONS", 960, 240, t, 79.12, PURPLE, 26)

# ============ SCENE 6: WAREHOUSE INTRO (86.1 - 91.5) ============
def sc_warehouse_intro(f, t, A):
    a = ramp(t, 86.12, 0.7)
    draw_rect(f, 360, 280, 1560, 920, (38, 46, 62), 0.5*a, width=3, radius=16)
    shelves = [(430,340,640,520),(760,340,970,520),(1090,340,1300,520),(430,640,640,860),(760,640,970,860),(1090,640,1300,860)]
    for i, s in enumerate(shelves):
        sa = ramp(t, 86.3+i*0.07, 0.3)
        draw_rect(f, *s, (90, 74, 52), 0.75*sa, width=2, radius=6)
    robots = [(560, 590, (1,0)), (890, 280+60, (0,1)), (1220, 590, (-1,0))]
    for i, (x, y, d) in enumerate(robots):
        t0 = 87.88 + i*0.2
        dx = 60*np.sin((t-t0)*1.1+i)*ramp(t, t0, 1.0)
        dy = 40*np.cos((t-t0)*0.9+i)*ramp(t, t0, 1.0)
        robot_icon(f, x+dx, y+dy, t, t0, BLUE, 15, dirx=int(d[0]), diry=int(d[1]))
    chip(f, "WAREHOUSE ROBOTS", 960, 200, t, 87.0, ORANGE, 30)

# ============ SCENE 7: CHARGING / COOP / DRONES (91.5 - 127.7) ============
def sc_charging(f, t, A):
    pre = 1 - ramp(t, 102.2, 0.45)      # phase A fade-out before drones
    drone_f = 1 - ramp(t, 110.1, 0.45)  # drones fade-out before opposite goals
    # charging station right
    csx, csy = 1420, 600
    if t > 93.0 and t < 102.3:
        sa = ramp(t, 93.0, 0.5, "back") * pre
        glow(f, csx, csy, 26, GREEN, 0.5*sa)
        draw_rect(f, csx-34, csy-58, csx+34, csy+58, GREEN, 0.35*sa, width=3, radius=8)
        draw_polyline(f, [(csx-10, csy-20), (csx+6, csy-2), (csx-8, csy-2), (csx+10, csy+22)], GOLD, 3.5, sa)
    r1y, r2y = 470, 730
    # two robots approach same station
    if t < 96.74:
        r1x = L(t, 92.2, 2.6, 520, 1330); r2x = L(t, 92.45, 2.6, 520, 1330)
        robot_icon(f, r1x, r1y, t, 92.2, BLUE, 15, dirx=1)
        robot_icon(f, r2x, r2y, t, 92.45, TEAL, 15, dirx=1)
    if 94.66 < t < 96.74:
        a = ramp(t, 94.66, 0.4)
        # spark at station approach point
        for k in range(3):
            ang = np.pi/2 + k*2.1 + (t-94.66)*3
            draw_line(f, (1310, 600), (1310+np.cos(ang)*40, 600+np.sin(ang)*40), RED, 3.5, a*(1-k*0.2))
        draw_circle(f, 1310, 600, 18, RED, 0.4*a)
        chip(f, "COMPETITION", 960, 220, t, 94.66, RED, 32)
    if 96.7 < t < 102.3:
        chip(f, "CHARGING", csx, csy-96, t, 93.0, GREEN, 22, alpha=pre)
    # alternate routes 96.74
    if 96.74 < t < 102.3:
        a = ramp(t, 96.74, 0.8) * pre
        p1 = [(520,470),(760,380),(1040,380),(1300,520),(1420,540)]
        p2 = [(520,730),(760,820),(1040,820),(1300,680),(1420,660)]
        draw_polyline(f, p1, BLUE, 4, 0.7*a)
        draw_polyline(f, p2, TEAL, 4, 0.7*a)
        if t > 97.58:
            # packages delivered
            for i, (px, py) in enumerate([(960, 380), (960, 820)]):
                box_icon(f, px, py, 16, t, 97.58+i*0.2, ORANGE)
            if t > 98.76:
                chip(f, "COOPERATION", 700, 600, t, 98.76, GREEN, 32, alpha=pre)
                check(f, 490, 600, 16, t, 99.2, GREEN)
    if 101.44 < t < 102.3:
        fa = ramp(t, 101.44, 0.5) * pre
        flag(f, 960, 250, t, 101.44, GOLD, 30)
        chip(f, "COMMON GOAL", 1120, 250, t, 101.6, GOLD, 24, alpha=fa)
    # rescue drones 102.68
    if 102.68 < t < 110.3:
        # aerial area
        aa = ramp(t, 102.68, 0.7) * drone_f
        draw_rect(f, 360, 330, 1560, 900, (26, 40, 48), 0.6*aa, width=2.5, radius=18)
        drones = [(620, 500, 0.0), (1100, 480, 2.1), (860, 780, 4.2)]
        for i, (dx0, dy0, ph) in enumerate(drones):
            t0 = 102.9 + i*0.18
            dx = dx0 + 34*np.sin((t-t0)*0.8 + ph)
            dy = dy0 + 26*np.cos((t-t0)*0.8 + ph)
            drone_icon(f, dx, dy, t, t0, 14, alpha=drone_f)
        if t > 104.24 and t < 110.3:
            # coverage sweeps
            for i, (dx0, dy0, ph) in enumerate(drones):
                p = ((t-104.24)*0.7 + i*0.33) % 1.0
                r = 30 + p*130
                draw_circle(f, dx0+34*np.sin((t-102.9-i*0.18)*0.8+ph), dy0+26*np.cos((t-102.9-i*0.18)*0.8+ph), r, TEAL, 0.25*(1-p)*drone_f, width=2)
        if t > 103.1: chip(f, "RESCUE DRONES", 960, 270, t, 103.1, TEAL, 28, alpha=drone_f)
        if t > 107.78:
            chip(f, "TEAM OBJECTIVE", 960, 950, t, 107.78, GOLD, 26, alpha=drone_f)
    # opposite goals 110.78
    if t > 110.78:
        a = ramp(t, 110.78, 0.6)
        vs_divider(f, 960, 330, 900, t, 110.78)
        draw_arrow(f, (800, 560), (560, 560), GREEN, 5, a, head=20)
        draw_arrow(f, (1120, 560), (1360, 560), RED, 5, a, head=20)
        chip(f, "GOAL A", 480, 640, t, 111.0, GREEN, 24)
        chip(f, "GOAL B", 1440, 640, t, 111.2, RED, 24)
        if t > 110.9: chip(f, "OPPOSITE GOALS", 960, 250, t, 110.9, RED, 28)
        if t > 112.76:
            meter(f, 400, 720, 320, "WIN", 0.9, t, 112.76, GREEN)
            meter(f, 1200, 720, 320, "LOSE", 0.15, t, 113.76, RED)
        if t > 114.5:
            # tug of war
            a2 = ramp(t, 114.5, 0.6)
            y0 = 860
            draw_line(f, (560, y0), (1360, y0), WHITE, 4, a2)
            for i in range(4):
                x1 = 640 + i*70 - ramp(t, 114.7, 1.0)*30
                x2 = 1280 - i*70 + ramp(t, 114.7, 1.0)*30
                agent_node(f, x1, y0, t, 114.6+i*0.1, GREEN, 12)
                agent_node(f, x2, y0, t, 114.6+i*0.1, RED, 12)
            if t > 116.52:
                for i, rx in enumerate([840, 900, 960, 1020, 1080]):
                    glow(f, rx, y0, 10, GOLD, 0.6)
                    draw_circle(f, rx, y0, 8, GOLD, 0.95)
                chip(f, "RESOURCES", 960, y0-56, t, 116.52, GOLD, 22)

# ============ SCENE 8: NON-STATIONARITY (127.7 - 149.5) ============
def sc_nonstat(f, t, A):
    chip(f, "NON-STATIONARY ENVIRONMENT", 960, 200, t, 129.58, ORANGE, 32)
    # wavy environment curve
    pts = []
    for i in range(140):
        x = 420 + i*8
        y = 560 + 70*np.sin(i*0.22 + (t-127.7)*1.4)*ramp(t, 128.5, 1.5)
        pts.append((x, y))
    if t > 128.5:
        draw_polyline(f, pts, ORANGE, 5, 0.95)
        draw_text(f, "ENVIRONMENT", 420, 660, 22, ORANGE, 0.9)
    # strategy curve shifting 132.6
    if t > 132.6:
        pts2 = []
        for i in range(140):
            x = 420 + i*8
            y = 680 + 55*np.sin(i*0.18 + (t-132.6)*1.1 + 1.5)*ramp(t, 132.6, 1.2)
            pts2.append((x, y))
        draw_polyline(f, pts2, BLUE, 5, 0.95)
        draw_text(f, "STRATEGY (ALSO CHANGING)", 420, 780, 22, BLUE, 0.9)
    # defense shield 137.06
    if t > 137.06:
        shield_icon(f, 1280, 480, 34, t, 137.06, GREEN, check_on=False)
        draw_text(f, "DEFENSE", 1280, 560, 22, GREEN, 0.9)
        a = ramp(t, 137.3, 0.5)
        draw_arrow(f, (1080, 480), (1215, 480), RED, 5, a, head=18)
    if t > 138.52:
        a = ramp(t, 138.52, 0.6)
        # attack curves around
        pth = [(1080, 700), (1160, 780), (1330, 700), (1400, 560)]
        draw_polyline(f, pth, RED, 4.5, a)
        draw_arrow(f, (1370, 610), (1400, 560), RED, 4.5, a, head=16)
        draw_text(f, "ATTACK CHANGES", 1240, 830, 22, RED, 0.9)
    if t > 140.94:
        a = ramp(t, 140.94, 0.5)
        for i, (x, y, c) in enumerate([(560, 420, BLUE), (1360, 900, TEAL)]):
            draw_arrow(f, (x, y+60), (x, y-40), c, 5, a, head=18)
        chip(f, "BOTH IMPROVE", 960, 950, t, 140.94, GREEN, 28)
    if t > 142.72:
        a = ramp(t, 142.72, 0.5)
        glow(f, 330, 950, 16, GREEN, 0.5*a); draw_circle(f, 330, 950, 13, GREEN, 0.9*a)
        glow(f, 330, 950-52, 16, RED, 0.5*a); draw_circle(f, 330, 898, 13, RED, 0.9*a)
        draw_text(f, "COMPETITION", 360, 898, 22, WHITE, 0.9*a, anchor="lm")
        draw_text(f, "COOPERATION", 360, 950, 22, WHITE, 0.9*a, anchor="lm")

# ============ SCENE 9: CREDIT ASSIGNMENT (149.5 - 200.9) ============
def sc_credit(f, t, A):
    chip(f, "CREDIT ASSIGNMENT", 960, 190, t, 149.46, GOLD, 34)
    # team reward bar
    if t > 153.36:
        a = ramp(t, 153.36, 0.7)
        wbar = 560*a
        draw_rect(f, 680, 260, 680+wbar, 310, GOLD, 0.85, width=0, radius=8)
        draw_text(f, "TEAM REWARD", 680, 240, 24, GOLD, 0.95, anchor="lm")
    # split ? 156.5
    if t > 156.5:
        a = ramp(t, 156.5, 0.5)
        for i in range(4):
            x = 700 + i*140
            draw_rect(f, x, 330, x+120, 380, (120, 100, 40), 0.8*a, width=0, radius=6)
            draw_text(f, "?", x+60, 355, 30, GOLD, 0.95*a)
    # 4 robots + box
    robots = [(760, 620, "A"), (1160, 620, "B"), (960, 430, "C"), (960, 810, "D")]
    cols = [BLUE, TEAL, PURPLE, GREY]
    for i, (x, y, nm) in enumerate(robots):
        robot_icon(f, x, y, t, 158.54+i*0.15, cols[i], 16)
        draw_text(f, nm, x, y+46, 22, WHITE, 0.9)
    # heavy box center
    bx = 960
    if t > 160.24:
        s = 40
        draw_rect(f, bx-s, 540-s, bx+s, 540+s, ORANGE, 0.5, width=3, radius=6)
        draw_text(f, "BOX", bx, 540, 26, WHITE, 0.95)
    # destination + team reward 162
    if t > 161.96:
        fa = ramp(t, 161.96, 0.5)
        flag(f, 1560, 540, t, 161.96, GOLD, 34)
        bxp = L(t, 162.2, 1.6, 960, 1470)
        draw_rect(f, bxp-40, 500, bxp+40, 580, ORANGE, 0.5, width=3, radius=6)
        if t > 163.9:
            pulse_ring(f, 1560, 540, t, 163.9, GOLD, 26, 110, 1.0)
    # contributions 166.5
    if t > 166.5: chip(f, "DIRECTION", 760, 690, t, 166.5, BLUE, 22)
    if t > 168.24:
        chip(f, "PUSH", 1160, 690, t, 168.24, TEAL, 22)
        if t < 170.5: bx2 = L(t, 168.3, 0.5, 1000, 1010); draw_arrow(f, (1160, 600), (1040, 560), TEAL, 4, ramp(t, 168.3, 0.4), head=14)
    if t > 169.7:
        chip(f, "CLEAR PATH", 560, 355, t, 169.7, PURPLE, 22)
        # obstacle fades
        oa = 1 - ramp(t, 169.9, 0.8)
        if oa > 0: draw_rect(f, 1060, 380, 1140, 430, GREY, 0.6*oa, width=0, radius=4)
    if t > 171.1:
        a = ramp(t, 171.1, 0.5)
        draw_circle(f, 960, 810, 26, GREY, 0.25*a, width=2)
        chip(f, "IDLE", 960, 880, t, 171.1, GREY, 22)
    # same reward wrong 174.5
    if t > 174.52:
        a = ramp(t, 174.52, 0.6)
        for i, (x, y, nm) in enumerate(robots):
            glow(f, x, y-60, 12, GOLD, 0.55*a)
            draw_circle(f, x, y-60, 10, GOLD, 0.95*a)
        if t > 175.54:
            b = ramp(t, 175.54, 0.5)
            cross(f, 960, 750, 14, t, 175.54, RED, 5)
            chip(f, "INACTIVE ROBOT GETS REWARD?", 1220, 880, t, 175.54, RED, 22)
    # shared vs individual 185.18
    if t > 185.18:
        a = ramp(t, 185.18, 0.6)
        draw_text(f, "SHARED REWARD", 500, 430, 26, GREEN, 0.95*a, anchor="lm")
        draw_rect(f, 500, 450, 900, 470, GREEN, 0.75*a, width=0, radius=6)
        draw_text(f, "TEAM SUCCESS", 500, 510, 20, GREY, 0.9*a, anchor="lm")
    if t > 186.26:
        a = ramp(t, 186.26, 0.6)
        draw_text(f, "INDIVIDUAL REWARD", 1120, 430, 26, BLUE, 0.95*a, anchor="lm")
        ws = [0.7, 0.55, 0.4, 0.08]
        for i, w in enumerate(ws):
            x = 1120 + i*90
            draw_rect(f, x, 560-160*w, x+70, 560, BLUE, 0.75*a, width=0, radius=5)
        draw_text(f, "LOCAL ACTION GUIDE", 1120, 590, 20, GREY, 0.9*a, anchor="lm")
    # balance 195.78
    if t > 195.78:
        a = ramp(t, 195.78, 0.5)
        bx0, by0 = 960, 950
        draw_line(f, (bx0-70, by0), (bx0+70, by0), WHITE, 4, a)
        draw_line(f, (bx0, by0-6), (bx0, by0-70), WHITE, 4, a)
        tilt = 0.25*np.sin((t-195.78)*1.6)
        for s in (-1, 1):
            px = bx0 + s*60
            py = by0 - 70 + s*tilt*60
            draw_line(f, (bx0, by0-70), (px, py), WHITE, 3, a)
            draw_circle(f, px, py+16, 18, GOLD if s < 0 else BLUE, 0.5*a, width=2.5)
        draw_circle(f, bx0, by0-70, 8, WHITE, a)
    if t > 197.46:
        a = ramp(t, 197.46, 0.4)
        chip(f, "SELFISH?", 1180, 950, t, 197.46, RED, 24)
        # robot grabbing coins
        if a > 0:
            for k in range(3):
                gx = L(t, 197.5, 0.8, 950+0, 1060)
                draw_circle(f, gx, 930, 9, GOLD, 0.9*a)

# ============ SCENE 10: DELAYED REWARD (200.9 - 239.5) ============
def sc_delayed(f, t, A):
    chip(f, "DELAYED REWARD", 960, 200, t, 200.86, ORANGE, 34)
    ty = 880
    x0, x1 = 500, 1420
    if t > 201.4:
        draw_line(f, (x0, ty), (x1, ty), GREY, 4, 0.8)
    # action point
    if t > 202.56:
        agent_node(f, x0, ty, t, 202.56, BLUE, 15)
        chip(f, "ACTION", x0, ty+64, t, 202.7, BLUE, 24)
        draw_arrow(f, (x0+30, ty-70), (x0, ty-24), BLUE, 3.5, ramp(t, 202.6, 0.4), head=13)
        draw_text(f, "ACTION NOW", x0+10, ty-100, 22, BLUE, 0.9)
    # result point
    if t > 204.22:
        fa = ramp(t, 204.22, 0.5, "back")
        flag(f, x1, ty-14, t, 204.22, GOLD, 28)
        chip(f, "RESULT", x1-10, ty+64, t, 204.4, GOLD, 24)
        draw_text(f, "MUCH LATER", x1-20, ty-100, 22, GOLD, 0.9)
    # drone flies along arc 206.54
    if t > 206.54:
        p = clamp01((t-206.54)/2.2)
        px = L(t, 206.54, 2.2, x0, x1)
        py = ty - 160*np.sin(p*np.pi)
        drone_icon(f, px, py, t, 206.54, 13)
        if t > 208.5:
            a = ramp(t, 208.5, 0.4)
            clock_icon(f, px, py-70, 22, t, 208.5, frac=0.8)
            chip(f, "10 MIN", px, py-130, t, 208.6, WHITE, 22)
        if t > 210.32 and p > 0.97:
            pulse_ring(f, x1, ty-30, t, 210.32, GREEN, 20, 90, 0.9)
            chip(f, "TARGET FOUND", x1-90, ty-170, t, 210.32, GREEN, 24)
    # temporal credit backflow 215.12
    if t > 215.12:
        a = ramp(t, 215.12, 0.7)
        for k in range(7):
            p = ((t-215.12)*0.55 + k/7.0) % 1.0
            px = x1 - (x1-x0)*p
            py = ty - 120*np.sin((1-p)*np.pi) - 20
            draw_circle(f, px, py, 5, GOLD, 0.85*a*(0.4+0.6*np.sin(p*np.pi)))
        chip(f, "TEMPORAL CREDIT ASSIGNMENT", 960, 560, t, 215.12, GOLD, 26)
    # manager feedback 218.16
    if t > 218.16:
        a = ramp(t, 218.16, 0.6)
        human_icon(f, 960, 300, 30, t, 218.16, WHITE)
        chip(f, "MANAGER FEEDBACK", 1240, 290, t, 218.6, PURPLE, 24)
        chips = [("PLANNING OK", GREEN, 480), ("TIMING OK", GREEN, 550), ("COMMS WEAK", RED, 620)]
        for i, (txt, c, y) in enumerate(chips):
            chip(f, txt, 1400, y, t, 219.5+i*0.3, c, 20)
    # AI agents estimate from signal 225.3
    if t > 225.34:
        a = ramp(t, 225.34, 0.6)
        robot_icon(f, 480, 300, t, 225.34, BLUE, 14)
        robot_icon(f, 560, 300, t, 225.5, TEAL, 14)
        chip(f, "AI AGENTS", 560, 220, t, 225.6, BLUE, 22)
    if t > 229.3:
        a = ramp(t, 229.3, 0.5)
        for k in range(4):
            p = ((t-229.3)*0.8 + k/4) % 1
            draw_circle(f, 620+p*180, 300, 6, GOLD, 0.8*a*(1-p))
        chip(f, "ONLY A REWARD SIGNAL", 900, 240, t, 229.3, GOLD, 24)
    if t > 231.9:
        a = ramp(t, 231.9, 0.5)
        clock_icon(f, 1290, 330, 24, t, 231.9, frac=0.15, color=GREY)
        chip(f, "LATE -> SLOW LEARNING", 1460, 400, t, 232.2, RED, 22)
    # subgoals 237.86
    if t > 237.86:
        for i, gx in enumerate([730, 960, 1190]):
            a = ramp(t, 237.86+i*0.18, 0.4, "back")
            draw_circle(f, gx, ty, 11, GREEN, 0.9*a)
            pulse_ring(f, gx, ty, t, 237.86+i*0.18, GREEN, 10, 44, 0.8)
        chip(f, "SUBGOALS HELP", 960, 970, t, 238.3, GREEN, 26)

# ============ SCENE 11: PARTIAL OBSERVABILITY (239.5 - 283.1) ============
def sc_partial(f, t, A):
    chip(f, "PARTIAL OBSERVABILITY", 960, 190, t, 239.52, ORANGE, 32)
    # two corridors
    ca = ramp(t, 240.2, 0.7)
    draw_rect(f, 440, 300, 880, 900, (36, 44, 60), 0.55*ca, width=2.5, radius=12)
    draw_rect(f, 1040, 300, 1480, 900, (36, 44, 60), 0.55*ca, width=2.5, radius=12)
    draw_line(f, (560, 300), (560, 900), GREY, 2, 0.4*ca)
    draw_line(f, (760, 300), (760, 900), GREY, 2, 0.4*ca)
    draw_line(f, (1160, 300), (1160, 900), GREY, 2, 0.4*ca)
    draw_line(f, (1360, 300), (1360, 900), GREY, 2, 0.4*ca)
    # robot A sees own corridor
    ax_, ay_ = 660, 560
    if t > 245.78:
        view_cone(f, ax_, ay_, -np.pi/2, 1.5, 220, t, 245.9, BLUE, 0.3)
        robot_icon(f, ax_, ay_, t, 245.78, BLUE, 16)
        draw_text(f, "RESCUE ROBOT A", ax_, 660, 20, WHITE, 0.9)
    # robot B
    if t > 246.88:
        bx_, by_ = 1260, 620
        view_cone(f, bx_, by_, np.pi/2, 1.5, 200, t, 247.0, TEAL, 0.3)
        robot_icon(f, bx_, by_, t, 246.88, TEAL, 16)
        draw_text(f, "ROBOT B", bx_, 720, 20, WHITE, 0.9)
    # other corridor dark
    if t > 248.14:
        a = ramp(t, 248.14, 0.6)
        draw_rect(f, 1040, 300, 1480, 480, (8, 10, 14), 0.55*a, width=0, radius=10)
        draw_text(f, "HIDDEN", 1260, 390, 22, GREY, 0.9*a)
    # ? between 253.3
    if t > 253.3:
        a = ramp(t, 253.3, 0.5)
        draw_text(f, "?", 960, 560, 72, RED, 0.95*a, glow=True)
    # memory + communication 255.56
    if t > 255.56:
        a = ramp(t, 255.56, 0.5)
        chip(f, "MEMORY", 660, 250, t, 255.56, PURPLE, 24)
        chip(f, "COMMUNICATION", 1260, 250, t, 255.9, TEAL, 24)
        draw_line(f, (760, 560), (1160, 620), TEAL, 3, 0.6*a, dash=10)
    # message: left searched 260.38
    if t > 260.38:
        a = ramp(t, 260.38, 0.5)
        chip(f, "LEFT: SEARCHED", 660, 440, t, 260.38, BLUE, 22)
        # packet travels
        p = clamp01((t-260.8)/1.0)
        px = L(t, 260.8, 1.0, 760, 1160)
        py = L(t, 260.8, 1.0, 500, 560)
        if 0 < p < 1:
            glow(f, px, py, 9, GOLD, 0.7); draw_circle(f, px, py, 7, GOLD, 0.95)
    # B moves to new area 262.66
    if t > 262.66:
        nx = L(t, 262.66, 1.4, 1260, 1300)
        ny = L(t, 262.66, 1.4, 620, 420)
        robot_icon(f, nx, ny, t, 246.88, TEAL, 16, diry=-1)
        if t > 263.6:
            glow(f, nx, ny-60, 14, GREEN, 0.4)
            chip(f, "NEW AREA", nx, ny-100, t, 263.7, GREEN, 20)
    # guess intentions 271.4
    if t > 271.4:
        a = ramp(t, 271.4, 0.6)
        draw_arrow(f, (1260, 700), (900, 660), GREY, 3, 0.7*a, head=14)
        chip(f, "GUESS INTENTION", 1080, 780, t, 271.6, GREY, 22)
    if t > 273.04:
        a = ramp(t, 273.04, 0.5)
        for k in range(3):
            p = ((t-273.04)*0.9 + k/3) % 1.0
            px = 760 + (1160-760)*p
            py = 560 + (620-560)*p
            draw_circle(f, px, py, 6, TEAL, 0.8*(1-p*0.3))
        chip(f, "COMMUNICATION = FASTER LEARNING", 960, 970, t, 273.2, TEAL, 24)

# ============ SCENE 12A: TRAFFIC (283.1 - 304.9) ============
def sc_traffic(f, t, A):
    a = ramp(t, 283.12, 0.6)
    # intersection
    draw_rect(f, 480, 300, 1440, 900, (30, 38, 52), 0.5*a, width=2.5, radius=14)
    # roads
    draw_rect(f, 880, 300, 1040, 900, (52, 58, 70), 0.9*a, width=0, radius=0)
    draw_rect(f, 480, 540, 1440, 700, (52, 58, 70), 0.9*a, width=0, radius=0)
    for i in range(6):
        yy = 320 + i*100
        if yy < 540 or yy > 700:
            draw_line(f, (945, yy), (975, yy), WHITE, 3, 0.5*a)
            draw_line(f, (945, yy+50), (975, yy+50), WHITE, 3, 0.5*a) if False else None
    for i in range(8):
        xx = 520 + i*110
        if xx < 880 or xx > 1040:
            draw_line(f, (xx, 605), (xx, 635), WHITE, 3, 0.5*a)
    # signals at corners 288.06
    sig = [(880, 540), (1040, 540), (880, 700), (1040, 700)]
    cols = [RED, GREEN, RED, GREEN]
    for i, (x, y) in enumerate(sig):
        if t > 288.06 + i*0.12:
            aa = ramp(t, 288.06+i*0.12, 0.4, "back")
            draw_rect(f, x-26, y-26, x+26, y+26, (20, 26, 36), 0.9*aa, width=2.5, radius=6)
            draw_circle(f, x, y, 12, cols[i], 0.95*aa)
    chip(f, "TRAFFIC LIGHTS = AGENTS", 960, 250, t, 286.14, ORANGE, 28)
    # coordination 295.38
    if t > 295.38:
        a2 = ramp(t, 295.38, 0.6)
        for i in range(4):
            p1 = sig[i]; p2 = sig[(i+1) % 4]
            draw_line(f, p1, p2, GREEN, 2.5, 0.6*a2, dash=12)
        chip(f, "COORDINATE", 960, 470, t, 295.5, GREEN, 24)
    # jam 300.5
    if t > 300.5:
        a3 = ramp(t, 300.5, 0.5)
        for k in range(7):
            yy = 760 + k*18 if False else 720 - k*0
            y = 750 - 0
            # cars pile on vertical road below center
            cy = 760 + k*16
            draw_rect(f, 930-14, cy, 930+14, cy+34, RED, 0.85*a3, width=0, radius=4)
        chip(f, "JAM", 1180, 800, t, 300.6, RED, 26)
    # smooth flow 303.64
    if t > 303.64:
        a4 = ramp(t, 303.64, 0.6)
        # moving dots along roads
        for k in range(5):
            p = ((t-303.64)*0.35 + k*0.2) % 1.0
            yy = 900 - 600*p
            if not (540 < yy < 700):
                draw_circle(f, 930, yy, 9, GREEN, 0.9*a4)
            xx = 480 + 960*p
            if not (880 < xx < 1040):
                draw_circle(f, xx, 620, 9, GREEN, 0.9*a4)
        chip(f, "SMOOTH FLOW = SHARED GOAL", 960, 960, t, 303.64, GREEN, 26)

# ============ SCENE 12B: WAREHOUSE APP (304.9 - 325.5) ============
def sc_wh_app(f, t, A):
    a = ramp(t, 305.62, 0.6)
    draw_rect(f, 360, 280, 1560, 920, (38, 46, 62), 0.5*a, width=2.5, radius=14)
    shelves = [(440,320,660,540),(990,320,1210,540),(440,660,660,880),(990,660,1210,880)]
    for i, s in enumerate(shelves):
        sa = ramp(t, 305.8+i*0.08, 0.3)
        draw_rect(f, *s, (90, 74, 52), 0.8*sa, width=2, radius=6)
    # packages 307.78
    if t > 307.78:
        for i, (px, py) in enumerate([(550,430),(1100,430),(550,770),(1100,770)]):
            box_icon(f, px, py, 15, t, 307.78+i*0.15, ORANGE)
    chip(f, "WAREHOUSE ROBOTS", 960, 220, t, 305.7, ORANGE, 28)
    # robots moving
    robots = [(760, 480, BLUE), (860, 780, TEAL), (1300, 620, PURPLE)]
    for i, (x, y, c) in enumerate(robots):
        t0 = 306.4+i*0.2
        dx = 46*np.sin((t-t0)*1.0+i*1.4)*ramp(t, t0, 0.8)
        robot_icon(f, x+dx, y, t, t0, c, 14)
    # busy aisle red 312.06
    if t > 312.06:
        a2 = ramp(t, 312.06, 0.5)
        draw_rect(f, 660, 320, 990, 900, (120, 40, 36), 0.35*a2, width=0, radius=8)
        chip(f, "BUSY AISLE", 820, 300, t, 312.2, RED, 22)
        # reroute arrow
        pts = [(700, 600), (820, 560), (940, 600)]
        if a2 > 0: draw_polyline(f, pts, WHITE, 3, 0.8*a2, dash=0)
    # task divide 315.14
    if t > 315.14:
        a3 = ramp(t, 315.14, 0.5)
        chip(f, "TASKS DIVIDED", 960, 960, t, 315.14, BLUE, 26)
    # charging conflict 317.14
    if t > 317.14:
        a4 = ramp(t, 317.14, 0.5)
        csx, csy = 1420, 480
        draw_rect(f, csx-26, csy-46, csx+26, csy+46, GREEN, 0.4*a4, width=2.5, radius=6)
        r1 = (L(t, 317.2, 1.2, 1300, 1360), 440); r2 = (L(t, 317.4, 1.2, 1300, 1360), 530)
        robot_icon(f, r1[0], r1[1], t, 317.2, BLUE, 12, dirx=1)
        robot_icon(f, r2[0], r2[1], t, 317.4, TEAL, 12, dirx=1)
        chip(f, "CHARGING CONFLICT", 1330, 330, t, 317.4, RED, 22)
    # collision avoided 320.98
    if t > 320.98:
        a5 = ramp(t, 320.98, 0.5)
        shield_icon(f, 960, 600, 40, t, 320.98, GREEN)
        chip(f, "COLLISION AVOIDED", 960, 700, t, 321.2, GREEN, 24)

# ============ SCENE 12C: DRONES APP (325.5 - 348.8) ============
def sc_drones_app(f, t, A):
    a = ramp(t, 326.5, 0.6)
    draw_rect(f, 420, 280, 1500, 920, (26, 40, 48), 0.6*a, width=2.5, radius=18)
    chip(f, "SEARCH AREA", 960, 220, t, 326.6, TEAL, 28)
    drones = [(640, 460), (1180, 440), (700, 800), (1240, 780)]
    for i, (x, y) in enumerate(drones):
        t0 = 326.7+i*0.15
        dx = x + 40*np.sin((t-t0)*0.7+i)
        dy = y + 30*np.cos((t-t0)*0.7+i)
        drone_icon(f, dx, dy, t, t0, 14)
    # large area label 328.88
    if 328.88 < t < 339.5:
        a2 = ramp(t, 328.88, 0.4) * (1 - ramp(t, 338.6, 0.9))
        draw_text(f, "LARGE AREA", 960, 950, 24, WHITE, 0.9*a2)
    # random overlapping scans 331.88
    if t > 331.88 and t < 340.0:
        a3 = fade(t, 331.88, 340.2, 0.4, 0.5)
        for i, (x, y) in enumerate([(760, 520), (860, 560), (800, 620), (900, 500)]):
            p = ((t-331.88)*0.5 + i*0.25) % 1.0
            draw_circle(f, x, y, 40+p*110, GREY, 0.3*a3*(1-p), width=2.5)
        if t > 332.2: chip(f, "RANDOM = WASTED SCANS", 960, 580, t, 332.2, GREY, 24)
    # coordinated coverage 340.2
    if t > 340.2:
        a4 = ramp(t, 340.2, 1.2)
        # tiles fill
        for gy in range(4):
            for gx in range(6):
                x0 = 480 + gx*170; y0 = 320 + gy*150
                ta = clamp01(a4*6 - (gx+gy)*0.5)
                if ta > 0:
                    draw_rect(f, x0, y0, x0+150, y0+130, TEAL, 0.16*ta, width=1.5, radius=6)
        chip(f, "COORDINATED COVERAGE", 960, 950, t, 340.4, GREEN, 26)
    # detect object 343.44
    if t > 343.44:
        a5 = ramp(t, 343.44, 0.4)
        ox, oy = 1000, 560
        pulse_ring(f, ox, oy, t, 343.44, RED, 16, 70, 0.8)
        draw_circle(f, ox, oy, 12, RED, 0.95*a5)
        chip(f, "OBJECT DETECTED", ox+150, oy-80, t, 343.6, RED, 24)
        if t > 345.0:
            for i, (x, y) in enumerate(drones[:3]):
                p = clamp01((t-345.0)/1.2)
                px = L(t, 345.0, 1.2, x, ox-40+i*40)
                py = L(t, 345.0, 1.2, y, oy-60)
                drone_icon(f, px, py, t, 326.7+i*0.15, 12)
                draw_line(f, (x, y), (px, py), TEAL, 1.5, 0.4*p)

DRAW_A = [
    (0.0,   19.94, sc_football),
    (19.94, 26.10, sc_programs),
    (26.10, 46.72, sc_rl_loop),
    (46.72, 55.18, sc_maze),
    (55.18, 86.12, sc_marl),
    (86.12, 91.48, sc_warehouse_intro),
    (91.48, 127.66, sc_charging),
    (127.66, 149.02, sc_nonstat),
    (149.02, 200.32, sc_credit),
    (200.32, 239.02, sc_delayed),
    (239.02, 281.48, sc_partial),
    (281.48, 304.94, sc_traffic),
    (304.94, 325.54, sc_wh_app),
    (325.54, 348.08, sc_drones_app),
]
