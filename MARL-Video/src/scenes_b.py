#!/usr/bin/env python3
"""Scenes B: 348.8-779.4s — CTDE, limitations, recap, team game, stability, comm design, exploration, evaluation, future."""
import numpy as np
from engine import (W, H, draw_circle, draw_line, draw_arrow, draw_rect, draw_text,
                    draw_polyline, draw_poly_fill, ease, ramp, clamp01, fade,
                    BLUE, RED, GREEN, GOLD, PURPLE, WHITE, GREY, ORANGE, TEAL, BLUE_D)
from kit import (agent_node, chip, chip_box, robot_icon, drone_icon, flag, ball, view_cone,
                 meter, vs_divider, cross, check, pulse_ring, brain_icon, mini_net, box_icon,
                 clock_icon, shield_icon, lock_icon, human_icon, grid_world, glow)

def L(t, t0, dur, a, b, m="inout"):
    return a + (b - a) * ramp(t, t0, dur, m)

# ============ SCENE 13: CTDE (348.8 - 370.5) ============
def sc_ctde(f, t, A):
    chip(f, "CENTRALIZED TRAINING", 960, 200, t, 348.84, PURPLE, 30)
    agents = [(560, 500, BLUE), (560, 720, TEAL), (760, 610, ORANGE), (380, 610, PURPLE)]
    # central brain
    if t > 349.4:
        a = ramp(t, 349.4, 0.6, "back")
        draw_rect(f, 1080, 480, 1440, 740, (40, 32, 56), 0.7*a, width=3, radius=18)
        brain_icon(f, 1260, 610, 40, t, 349.5, PURPLE)
        mini_net(f, 1260, 610, t, 349.8, (3, 4, 2), 40, 26, PURPLE)
    for i, (x, y, c) in enumerate(agents):
        agent_node(f, x, y, t, 349.0+i*0.12, c, 17)
    # info arrows in
    if t > 350.34:
        a = ramp(t, 350.34, 0.6)
        for i, (x, y, c) in enumerate(agents):
            draw_arrow(f, (x+30, y-10), (1070, 580+ (i-1.5)*30), PURPLE, 3, 0.7*a, head=13)
        chip(f, "ALL AGENT INFO", 1260, 800, t, 350.6, PURPLE, 24)
    # coordination web 357.68
    if t > 357.68:
        a = ramp(t, 357.68, 0.6)
        pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        for p1, p2 in pairs:
            a1 = agents[p1][:2]; a2 = agents[p2][:2]
            draw_line(f, a1, a2, GREEN, 2, 0.5*a)
        chip(f, "TEAM COORDINATION LEARNED", 700, 880, t, 357.9, GREEN, 24)
    # transition to execution 362.7
    if t > 362.7:
        # central fades
        a = ramp(t, 362.7, 0.5)
        draw_rect(f, 1080, 480, 1440, 740, (13, 17, 23), 0.95*a, width=0, radius=18)
        chip(f, "DECENTRALIZED EXECUTION", 960, 200, t, 362.7, BLUE, 30)
        # each agent local cone only
        for i, (x, y, c) in enumerate(agents):
            view_cone(f, x, y, 0, 1.1, 170, t, 363.0+i*0.1, c, 0.3)
        chip(f, "LOCAL OBSERVATION -> ACTION", 700, 880, t, 363.4, BLUE, 24)
    if t > 365.04:
        a = ramp(t, 365.04, 0.5)
        draw_rect(f, 1080, 480, 1400, 700, (30, 38, 52), 0.85*a, width=2.5, radius=10)
        grid_world(f, 1110, 510, 1370, 670, 5, t, 365.2, 0.5*a)
        draw_text(f, "TRAINING: FULL MAP", 1240, 740, 24, WHITE, 0.95*a)
    if t > 369.14:
        a = ramp(t, 369.14, 0.5)
        chip(f, "MISSION: SENSORS ONLY", 1240, 820, t, 369.14, ORANGE, 24)

# ============ SCENE 14: LIMITATIONS (370.5 - 451.5) ============
def sc_limits(f, t, A):
    chip(f, "LIMITATIONS", 960, 180, t, 371.12, RED, 34)
    # 1. sample efficiency 373.3
    if t < 391.48:
        a = ramp(t, 373.3, 0.6)
        chip(f, "SAMPLE EFFICIENCY", 960, 260, t, 373.3, ORANGE, 28)
        # trials accumulate
        n = int(clamp01((t-373.8)/6.0) * 42)
        rng = np.random.default_rng(11)
        if not hasattr(sc_limits, "_pts"):
            sc_limits._pts = rng.uniform([420, 380], [1500, 820], (42, 2))
        for i in range(n):
            x, y = sc_limits._pts[i]
            aa = ramp(t, 373.8+i*0.14, 0.3)
            draw_circle(f, x, y, 8, BLUE, 0.55*aa)
            draw_circle(f, x, y, 8, RED, 0.35*aa) if i % 3 == 0 else None
        draw_text(f, "MANY TRIALS NEEDED", 960, 880, 26, WHITE, 0.9*a)
        if t > 381.12:
            a2 = ramp(t, 381.12, 0.5)
            robot_icon(f, 500, 940, t, 381.12, BLUE, 13)
            meter(f, 560, 940, 300, "EXPENSIVE + RISKY", 0.85, t, 381.2, RED, 20)
        if t > 386.04:
            # sim vs real gap
            a3 = ramp(t, 386.04, 0.6)
            draw_circle(f, 560, 620, 90, BLUE, 0.25*a3, width=3)
            draw_text(f, "SIM", 560, 620, 34, BLUE, 0.95*a3)
            draw_circle(f, 1360, 620, 90, GREEN, 0.25*a3, width=3)
            draw_text(f, "REAL", 1360, 620, 34, GREEN, 0.95*a3)
            # gap crack
            for k in range(4):
                yy = 560 + k*40
                draw_line(f, (920 + (k%2)*30, yy), (1000 - (k%2)*30, yy+20), RED, 3, 0.8*a3)
            chip(f, "SIM-TO-REAL GAP", 960, 480, t, 388.78, RED, 26)
    # 2. scalability 392.14
    elif t < 402.76:
        a = ramp(t, 392.14, 0.6)
        chip(f, "SCALABILITY", 960, 260, t, 392.14, ORANGE, 28)
        # agents multiply
        n_agents = [2, 4, 8]
        centers = [(640, 600), (960, 600), (1280, 600)]
        counts = [2 + int(clamp01((t-392.8)/1.0)*1), 3 + int(clamp01((t-393.8)/1.0)*2), 5 + int(clamp01((t-394.8)/1.0)*4)]
        rng = np.random.default_rng(5)
        if not hasattr(sc_limits, "_ring"):
            sc_limits._ring = [rng.uniform(0, 2*np.pi, 8) for _ in range(3)]
        for g, (cx, cy) in enumerate(centers):
            for i in range(counts[g]):
                ang = sc_limits._ring[g][i % 8] + (t-392.14)*0.25
                x = cx + np.cos(ang)*70; y = cy + np.sin(ang)*55
                aa = ramp(t, 392.8 + g + i*0.12, 0.3)
                draw_circle(f, x, y, 11, BLUE, 0.9*aa)
            # interaction lines grow
            il = min(counts[g]*(counts[g]-1)//2, 12)
            for i in range(il):
                a1 = sc_limits._ring[g][i % 8]; a2 = sc_limits._ring[g][(i*3) % 8] + 1.1
                x1 = cx + np.cos(a1+(t-392.14)*0.25)*70; y1 = cy + np.sin(a1+(t-392.14)*0.25)*55
                x2 = cx + np.cos(a2+(t-392.14)*0.25)*70; y2 = cy + np.sin(a2+(t-392.14)*0.25)*55
                draw_line(f, (x1, y1), (x2, y2), GREY, 1.5, 0.45*a)
        if t > 395.68:
            a2 = ramp(t, 395.68, 0.5)
            chip(f, "INTERACTIONS EXPLODE", 960, 900, t, 395.68, RED, 26)
    # 3. reward design 403.58
    elif t < 412.52:
        a = ramp(t, 403.58, 0.6)
        chip(f, "REWARD DESIGN", 960, 260, t, 403.58, ORANGE, 28)
        # delivery robot speed dial
        robot_icon(f, 700, 620, t, 404.0, BLUE, 16, dirx=1)
        meter(f, 560, 740, 400, "SPEED REWARD", 0.95, t, 404.6, ORANGE, 22)
        # hazard ahead
        if t > 406.2:
            a2 = ramp(t, 406.2, 0.4)
            draw_triangle_pts = [(1240, 560), (1300, 660), (1180, 660)]
            draw_poly_fill(f, draw_triangle_pts, RED, 0.7*a2)
            draw_text(f, "!", 1240, 620, 34, WHITE, 0.95*a2)
            # robot zooms past
            rx = L(t, 406.4, 1.0, 700, 1500)
            robot_icon(f, min(rx, 1560), 620, t, 404.0, BLUE, 16, dirx=1)
        if t > 408.0:
            a3 = ramp(t, 408.0, 0.5)
            shield_icon(f, 960, 880, 34, t, 408.0, GREY, check_on=False)
            cross(f, 960, 880, 20, t, 408.3, RED, 5)
            chip(f, "SAFETY IGNORED", 1150, 880, t, 408.2, RED, 24, pad=10)
        if t > 409.24:
            chip(f, "ALIGN REWARD WITH BEHAVIOR", 960, 340, t, 409.4, GREEN, 24)
    # 4. explainability 413.28
    else:
        a = ramp(t, 413.28, 0.6)
        chip(f, "EXPLAINABILITY", 960, 260, t, 413.28, ORANGE, 28)
        # black box
        if t > 413.8:
            a2 = ramp(t, 413.8, 0.6, "back")
            draw_rect(f, 780, 440, 1140, 720, (20, 22, 30), 0.95*a2, width=3, radius=14)
            draw_text(f, "?", 960, 580, 90, PURPLE, 0.95*a2, glow=True)
            draw_arrow(f, (640, 580), (770, 580), BLUE, 4, a2, head=16)
            draw_arrow(f, (1150, 580), (1280, 580), GREEN, 4, a2, head=16)
            draw_text(f, "TEAM WINS", 500, 580, 26, BLUE, 0.95*a2, anchor="rm")
            draw_text(f, "BUT WHY?", 1420, 580, 26, GOLD, 0.95*a2, anchor="lm")
        if t > 424.36:
            a3 = ramp(t, 424.36, 0.5)
            chip(f, "ENGINEERS NEED THE WHY", 960, 820, t, 424.36, WHITE, 24)
        if t > 428.08:
            a4 = ramp(t, 428.08, 0.5)
            for i, txt in enumerate(["COMM RULES", "ROLE POLICIES", "MONITORING"]):
                chip(f, txt, 660+i*300, 900, t, 428.3+i*0.25, GREEN, 22)
        if t > 436.7:
            a5 = ramp(t, 436.7, 0.5)
            chip(f, "SAFETY CONSTRAINTS > REWARD ONLY", 960, 380, t, 436.7, RED, 26)
        if t > 440.12:
            a6 = ramp(t, 440.12, 0.6)
            # narrow corridor
            draw_rect(f, 620, 480, 1300, 540, (46, 54, 68), 0.9*a6, width=0, radius=6)
            draw_rect(f, 620, 660, 1300, 720, (46, 54, 68), 0.9*a6, width=0, radius=6)
            r1x = L(t, 440.4, 1.4, 680, 1240); r2x = L(t, 440.6, 1.4, 1240, 680)
            robot_icon(f, r1x, 590, t, 440.4, BLUE, 12, dirx=1)
            robot_icon(f, r2x, 610, t, 440.6, TEAL, 12, dirx=-1)
            chip(f, "SLOW DOWN FIRST", 960, 800, t, 442.0, GREEN, 24)

# ============ SCENE 15: RECAP (451.5 - 506.2) ============
def sc_recap(f, t, A):
    chip(f, "CORE IDEA", 960, 170, t, 453.5, GOLD, 32, alpha=1 - ramp(t, 494.5, 0.8))

    # ---- PHASE 1: loop diagram (451.5 - 470.5) ----
    p1 = fade(t, 451.5, 470.8, 0.6, 0.7)
    if p1 > 0:
        agents = [(620, 480, BLUE), (620, 700, TEAL), (620, 920, PURPLE)]
        env_x, env_y = 1400, 600
        for i, (x, y, c) in enumerate(agents):
            agent_node(f, x, y, t, 454.5+i*0.15, c, 16, alpha=p1)
        a = ramp(t, 455.12, 0.6) * p1
        draw_rect(f, env_x-200, env_y-200, env_x+200, env_y+200, (40, 50, 68), 0.5*a, width=3, radius=16)
        grid_world(f, env_x-180, env_y-180, env_x+180, env_y+180, 6, t, 455.3, 0.4*a)
        chip(f, "SHARED ENVIRONMENT", env_x, env_y-250, t, 455.3, BLUE, 26, alpha=p1)
        if t > 458.62:
            a2 = ramp(t, 458.62, 0.5) * p1
            for i, (x, y, c) in enumerate(agents):
                draw_arrow(f, (x+40, y), (env_x-210, env_y-100+i*100), ORANGE, 3.5, 0.8*a2, head=14)
            chip(f, "POLICIES -> ACTIONS", 620, 300, t, 458.7, ORANGE, 24, alpha=p1)
        if t > 460.74:
            a3 = ramp(t, 460.74, 0.5) * p1
            for k in range(6):
                p = ((t-460.74)*0.6 + k/6) % 1.0
                px = env_x-210 + (660-(env_x-210))*p
                py = env_y+100 - 80*np.sin(p*np.pi)
                draw_circle(f, px, py, 5, GOLD, 0.8*(1-p*0.4)*a3)
            chip(f, "REWARDS = FEEDBACK", 380, 1020, t, 460.8, GOLD, 24, alpha=p1)
        if t > 466.1:
            chip(f, "COOPERATION", 250, 600, t, 466.1, GREEN, 24, alpha=p1)
            chip(f, "COMPETITION", 250, 700, t, 466.4, RED, 24, alpha=p1)

    # ---- PHASE 2: single vs multi (471.5 - 481.3) ----
    p2 = fade(t, 471.5, 481.4, 0.5, 0.6)
    if p2 > 0:
        a = ramp(t, 471.56, 0.6) * p2
        vs_divider(f, 960, 380, 1000, t, 471.56)
        # scale VS elements
        draw_circle(f, 960, (380+1000)/2, 17, (30, 36, 48), 0.9*a)
        draw_text(f, "VS", 960, (380+1000)/2, 20, WHITE, 0.9*a)
        agent_node(f, 780, 620, t, 471.8, BLUE, 18, alpha=p2)
        draw_text(f, "SINGLE AGENT", 780, 700, 22, GREY, 0.9*p2)
        for i, (x, y, c) in enumerate([(1100, 540, BLUE), (1240, 660, TEAL), (1080, 760, PURPLE)]):
            agent_node(f, x, y, t, 472.0+i*0.12, c, 14, alpha=p2)
            for j, (x2, y2, c2) in enumerate([(1100, 540, BLUE), (1240, 660, TEAL), (1080, 760, PURPLE)]):
                if j > i: draw_line(f, (x, y), (x2, y2), GREY, 1.5, 0.4*a)
        draw_text(f, "MULTI-AGENT", 1160, 900, 22, GREY, 0.9*p2)
        if t > 474.72:
            chip(f, "LEARNS FROM ENV + OTHER LEARNERS", 960, 1000, t, 474.72, WHITE, 24, alpha=p2)

    # ---- PHASE 3: shared world strip (482.5 - 495.3) ----
    p3 = fade(t, 482.5, 495.4, 0.5, 0.6)
    if p3 > 0:
        items = [(420, 482.5, "CARS SHARE ROADS", BLUE),
                 (760, 484.12, "ROBOTS SHARE WAREHOUSES", ORANGE),
                 (1100, 485.9, "DRONES SHARE INFO", TEAL),
                 (1440, 487.46, "HUMANS + AI", PURPLE)]
        for x, t0, txt, c in items:
            if t > t0:
                a = ramp(t, t0, 0.5) * p3
                draw_rect(f, x-150, 380, x+150, 500, (30, 38, 52), 0.8*a, width=2, radius=12)
                if "CARS" in txt:
                    draw_rect(f, x-40, 425, x+40, 450, c, 0.8*a, width=2, radius=6)
                    draw_circle(f, x-24, 455, 8, GREY, a); draw_circle(f, x+24, 455, 8, GREY, a)
                elif "ROBOTS" in txt:
                    robot_icon(f, x, 440, t, t0, ORANGE, 14, alpha=p3)
                elif "DRONES" in txt:
                    drone_icon(f, x, 440, t, t0, 13, alpha=p3)
                else:
                    human_icon(f, x-20, 440, 20, t, t0, WHITE, alpha=p3)
                    robot_icon(f, x+26, 440, t, t0+0.1, PURPLE, 10, alpha=p3)
                draw_text(f, txt, x, 535, 19, WHITE, 0.9*a)
        if t > 490.0:
            chip(f, "ONE SHARED ENVIRONMENT", 960, 680, t, 490.0, BLUE, 26, alpha=p3*ramp(t, 490.0, 0.5))

    # ---- PHASE 4: final question (496.6 - 506.1) ----
    if t > 496.64:
        a = ramp(t, 496.64, 0.6)
        chip(f, "MORE INTELLIGENCE", 620, 600, t, 496.64, BLUE, 26)
        chip(f, "OR", 960, 600, t, 496.9, GREY, 24)
        chip(f, "BETTER COORDINATION", 1300, 600, t, 498.1, GOLD, 26)
        if t > 499.48:
            a2 = ramp(t, 499.48, 0.5)
            glow(f, 960, 780, 20, GOLD, 0.4*a2)
            draw_circle(f, 960, 780, 15, GOLD, 0.9*a2)
            draw_text(f, "FUTURE SYSTEMS", 960, 860, 24, WHITE, 0.9*a2)
        if t > 505.0:
            a3 = ramp(t, 505.0, 0.5)
            brain_icon(f, 850, 780, 24, t, 505.0, PURPLE)
            draw_arrow(f, (900, 780), (1000, 780), GREEN, 4, a3, head=14)
            draw_arrow(f, (1060, 780), (990, 780), BLUE, 4, a3, head=14)
            chip(f, "SMART + COOPERATIVE", 960, 900, t, 505.2, GREEN, 26)

# ============ SCENE 16: TEAM GAME EXAMPLE (506.2 - 548.8) ============
def sc_teamgame(f, t, A):
    a = ramp(t, 506.16, 0.6)
    draw_rect(f, 420, 280, 1500, 920, (30, 40, 60), 0.5*a, width=2.5, radius=16)
    grid_world(f, 420, 280, 1500, 920, 12, t, 506.3, 0.3*a)
    chip(f, "TEAM GAME EXAMPLE", 960, 200, t, 506.16, GOLD, 30)
    # 3 agents left, opponent right, objective
    ag = [(600, 480, BLUE, "AGENT 1"), (600, 700, TEAL, "AGENT 2"), (600, 880, PURPLE, "AGENT 3")]
    for i, (x, y, c, nm) in enumerate(ag):
        agent_node(f, x, y, t, 508.68+i*0.18, c, 17)
        draw_text(f, nm, x, y+44, 20, WHITE, 0.9)
    # opponent
    if t > 509.38:
        agent_node(f, 1340, 560, t, 509.38, RED, 19)
        draw_text(f, "OPPONENT", 1340, 620, 20, RED, 0.9)
    # objective flag right-bottom
    if t > 510.76:
        flag(f, 1400, 840, t, 510.76, GOLD, 30)
        draw_text(f, "OBJECTIVE", 1400, 890, 20, GOLD, 0.9)
    # A1 observes 511.96
    if t > 511.96:
        view_cone(f, 600, 480, np.arctan2(560-480, 1340-600), 0.5, 380, t, 511.96, BLUE, 0.25)
        chip(f, "OBSERVE", 820, 430, t, 512.1, BLUE, 22)
    # A2 safe route 513.62
    if t > 513.62:
        pth = [(640, 700), (900, 760), (1100, 880), (1330, 850)]
        draw_polyline(f, pth, TEAL, 4, 0.8, dash=18)
        chip(f, "SAFE ROUTE", 950, 790, t, 513.8, TEAL, 22)
    # A3 objective 515.12
    if t > 515.12:
        draw_arrow(f, (660, 880), (1330, 850), PURPLE, 3.5, ramp(t, 515.12, 0.6), head=15)
        chip(f, "COMPLETE OBJECTIVE", 990, 930, t, 515.3, PURPLE, 22)
    # independent mess 517.86
    if t > 517.86 and t < 522.66:
        a2 = fade(t, 517.86, 523.2, 0.4, 0.4)
        for i, (x, y, c, nm) in enumerate(ag):
            ang = (t-517.86)*(1.1+i*0.3) + i*2.1
            mx = x + 140*np.cos(ang); my = y + 90*np.sin(ang)
            agent_node(f, mx, my, t, 508.68+i*0.18, c, 13)
            draw_line(f, (x, y), (mx, my), c, 2, 0.4*a2)
        if t > 520.02:
            cross(f, 960, 600, 24, t, 520.02, RED, 6)
            chip(f, "DUPLICATION + CONFUSION", 960, 340, t, 520.02, RED, 26)
    # roles 522.66
    if t > 522.66:
        roles = [("OBSERVER", BLUE), ("PLANNER", TEAL), ("EXECUTOR", PURPLE)]
        for i, (nm, c) in enumerate(roles):
            chip(f, nm, 600, 448 + (0 if False else 0) + i*0, t, 522.66+i*0.2, c, 20) if False else None
        chip(f, "OBSERVER", 850, 390, t, 522.66, BLUE, 20)
        chip(f, "PLANNER", 890, 620, t, 522.86, TEAL, 20)
        chip(f, "EXECUTOR", 790, 960, t, 523.06, PURPLE, 20)
        chip(f, "ROLE-BASED POLICIES", 1180, 300, t, 522.7, GREEN, 26)
    # info share 526.38
    if t > 526.38:
        a3 = ramp(t, 526.38, 0.4)
        for k in range(3):
            p = ((t-526.38)*0.8+k/3) % 1
            draw_circle(f, 640+p*220, 560+p*60, 6, BLUE, 0.85)
        chip(f, "INFO SHARED", 880, 500, t, 526.5, BLUE, 20)
    if t > 528.04:
        for k in range(3):
            p = ((t-528.04)*0.8+k/3) % 1
            draw_circle(f, 640+p*220, 760+p*40, 6, TEAL, 0.85)
        chip(f, "ROUTE PLANNED", 880, 700, t, 528.2, TEAL, 20)
    if t > 529.94:
        # A3 executes -> objective
        ax3 = L(t, 529.94, 1.6, 660, 1330)
        ay3 = L(t, 529.94, 1.6, 880, 840)
        agent_node(f, ax3, ay3, t, 508.68+2*0.18, PURPLE, 14)
        if t > 531.6:
            pulse_ring(f, 1400, 840, t, 531.6, GOLD, 22, 100, 1.0)
            chip(f, "EXECUTED", 1330, 930, t, 529.94, GREEN, 22)
    # support triangle 538.4
    if t > 538.4:
        a4 = ramp(t, 538.4, 0.6)
        pairs = [(0, 1), (1, 2), (2, 0)]
        for p1, p2 in pairs:
            x1, y1 = ag[p1][:2]; x2, y2 = ag[p2][:2]
            draw_arrow(f, (x1+24, y1), (x2-24, y2), GREEN, 2.5, 0.55*a4, head=12)
        chip(f, "EACH SUPPORTS THE OTHERS", 960, 1010, t, 538.6, GREEN, 24)
    # feedback chips 546.92
    if t > 546.92:
        chip(f, "INFO SHARED  +1", 480, 340, t, 546.92, GREEN, 20)
        chip(f, "NO COLLISION  +1", 760, 340, t, 547.2, GREEN, 20)
        chip(f, "GOOD TIMING  +1", 1060, 340, t, 547.5, GREEN, 20)

# ============ SCENE 17: STABILITY (548.8 - 589.9) ============
def sc_stability(f, t, A):
    chip(f, "LEARNING STABILITY", 960, 190, t, 548.78, ORANGE, 30)
    # two policy curves
    if t > 552.02:
        pts1, pts2 = [], []
        for i in range(120):
            x = 420 + i*9
            y1 = 500 - i*1.1*ramp(t, 552.02, 2.0) + 26*np.sin(i*0.14 + (t-552)*1.2)
            pts1.append((x, y1))
            if t > 554.56:
                y2 = 560 - i*0.9*ramp(t, 554.56, 2.0) + 26*np.sin(i*0.12 + (t-554.56)*1.1 + 2.0)
                pts2.append((x, y2))
        draw_polyline(f, pts1, BLUE, 4.5, 0.95)
        draw_text(f, "AGENT A POLICY", 420, 420, 22, BLUE, 0.9, anchor="lm")
        if t > 554.56:
            draw_polyline(f, pts2, TEAL, 4.5, 0.95)
            draw_text(f, "AGENT B POLICY (ALSO UPDATING)", 820, 560, 22, TEAL, 0.9, anchor="lm")
    if t > 558.9:
        a = ramp(t, 558.9, 0.4)
        cross(f, 1420, 470, 18, t, 558.9, RED, 5)
        chip(f, "TODAY'S BEST BEHAVIOR FAILS", 1130, 340, t, 558.9, RED, 24)
    # driver route example 560.74
    if t > 560.74:
        a = ramp(t, 560.74, 0.6)
        roads = [((480, 480), (1440, 480)), ((480, 700), (1440, 700)), ((480, 900), (1440, 900))]
        for p1, p2 in roads:
            draw_line(f, p1, p2, (60, 68, 82), 16, 0.9*a)
        draw_circle(f, 500, 590, 14, WHITE, 0.95*a)
        draw_text(f, "DRIVER", 500, 640, 20, WHITE, 0.9*a)
        # all choose same route 563.92
        if t > 563.92:
            a2 = ramp(t, 563.92, 0.8)
            for k in range(9):
                xx = 560 + k*95 + 8*np.sin((t-563.92)*3+k)
                draw_circle(f, xx, 700, 11, BLUE, 0.85*a2)
            chip(f, "ALL SAME ROUTE", 960, 760, t, 563.9, BLUE, 22)
        if t > 565.36:
            a3 = ramp(t, 565.36, 0.5)
            draw_line(f, (480, 700), (1440, 700), RED, 16, 0.55*a3)
            chip(f, "SLOW", 1300, 760, t, 565.5, RED, 24)
        if t > 568.9:
            # pattern shifts
            a4 = ramp(t, 568.9, 0.8)
            for k in range(5):
                p = ((t-568.9)*0.4 + k*0.2) % 1.0
                xx = 480 + 960*p
                draw_circle(f, xx, 480, 10, TEAL, 0.8*a4)
                draw_circle(f, xx, 900, 10, ORANGE, 0.8*a4)
            chip(f, "TRAFFIC PATTERN CHANGES AGAIN", 960, 1020, t, 568.9, ORANGE, 24)
    if t > 576.18:
        a = ramp(t, 576.18, 0.5)
        draw_rect(f, 300, 560, 560, 640, (24, 30, 42), 0.9*a, width=2, radius=10)
        draw_text(f, "FIXED RULES", 430, 585, 22, GREY, 0.9*a)
        draw_line(f, (330, 610), (530, 590), RED, 4, a)
        cross(f, 430, 600, 14, t, 576.5, RED, 4)
    if t > 580.38:
        a = ramp(t, 580.38, 0.5)
        # uncertainty fog
        for k in range(5):
            x = 900 + k*90
            draw_circle(f, x, 620, 46, GREY, 0.14*a)
        chip(f, "UNCERTAINTY", 1120, 620, t, 580.5, GREY, 24)
    if t > 583.02:
        a = ramp(t, 583.02, 0.5)
        chip(f, "ADAPT", 960, 500, t, 583.02, GREEN, 26)
        draw_arrow(f, (900, 540), (1020, 540), GREEN, 4, a, head=16)
    if t > 584.84:
        a = ramp(t, 584.84, 0.4)
        chip(f, "OPPONENT MODELING", 960, 950, t, 584.84, PURPLE, 24)
    if t > 586.02:
        a = ramp(t, 586.02, 0.5)
        for i in range(6):
            x = 1200 + i*60
            draw_arrow(f, (x, 980), (x, 920+18*i % 40), GOLD, 3, 0.7*a, head=11)
        chip(f, "POPULATION TRAINING", 1400, 1030, t, 586.2, GOLD, 22)

# ============ SCENE 18: COMM DESIGN (589.9 - 634.5) ============
def sc_comm(f, t, A):
    chip(f, "COMMUNICATION", 960, 180, t, 589.88, TEAL, 32)
    ag = [(520, 560, BLUE), (900, 460, TEAL), (900, 700, PURPLE), (1300, 560, ORANGE)]
    for i, (x, y, c) in enumerate(ag):
        agent_node(f, x, y, t, 590.3+i*0.12, c, 16)
    # message flood 592.92
    if t > 592.92 and t < 602.0:
        a = fade(t, 592.92, 602.4, 0.3, 0.5)
        rng = np.random.default_rng(3)
        if not hasattr(sc_comm, "_msgs"):
            sc_comm._msgs = rng.uniform([480, 320], [1360, 820], (26, 2))
        for i, (x, y) in enumerate(sc_comm._msgs):
            aa = ramp(t, 593.0+i*0.05, 0.25)
            draw_rect(f, x-30, y-16, x+30, y+16, RED, 0.3*aa, width=1.5, radius=8)
            draw_circle(f, x, y, 4, RED, 0.7*aa)
        if t > 594.0: chip(f, "UNLIMITED = NOISY", 960, 950, t, 594.0, RED, 26)
        if t > 598.64:
            clock_icon(f, 340, 560, 26, t, 598.64, frac=0.2, color=RED)
            chip(f, "SLOW", 340, 640, t, 598.7, RED, 22)
    # filters 602.46
    if t > 602.46:
        labels = [("WHEN?", 640, 300), ("TO WHOM?", 960, 300), ("WHAT?", 1280, 300)]
        for i, (txt, x, y) in enumerate(labels):
            chip(f, txt, x, y, t, 602.46+i*0.25, GOLD, 26)
        if t > 603.5: chip(f, "AGENTS LEARN TO SEND", 960, 220, t, 603.5, WHITE, 22)
    # warehouse example 608.5
    if t > 608.5:
        a = ramp(t, 608.5, 0.5)
        robot_icon(f, 520, 560, t, 590.3, BLUE, 15)
        chip(f, "POSITION", 640, 480, t, 608.6, GREEN, 22)
        if t > 610.76:
            a2 = 1 - ramp(t, 611.0, 0.4)
            for i, txt in enumerate(["SENSOR 1", "SENSOR 2", "SENSOR 3"]):
                chip(f, txt, 660, 600+i*56, t, 610.76, GREY, 18)
                if t > 611.2: cross(f, 728, 600+i*56, 12, t, 611.3+i*0.1, RED, 3)
        # one packet moves
        p = ((t-609.2)*0.7) % 1.0
        if t > 609.2 and t < 612.5:
            px = L(t, 609.2, 1.0, 560, 1260); py = 540
            glow(f, px, py, 8, GREEN, 0.6); draw_circle(f, px, py, 6, GREEN, 0.95)
    # drone confidence 614.08
    if t > 614.08:
        drone_icon(f, 900, 460, t, 590.6, 14)
        chip(f, "TARGET + CONFIDENCE", 960, 380, t, 614.2, TEAL, 22)
    if t > 616.28:
        chip(f, "SELECTIVE COMMUNICATION", 960, 950, t, 616.28, GREEN, 26)
        if t > 621.36:
            chip(f, "RIGHT INFO AT RIGHT TIME", 960, 900, t, 621.36, GOLD, 22)
    # late message 624.14
    if t > 624.14:
        a = ramp(t, 624.14, 0.4)
        px = L(t, 624.2, 0.8, 700, 1240); py = 820
        draw_circle(f, min(px, 1240), py, 7, GREY, 0.8*a)
        cross(f, 1300, 820, 12, t, 624.6, RED, 4)
        chip(f, "LATE = MISSED DECISION", 960, 1020, t, 624.3, RED, 22)
    if t > 626.82:
        a = ramp(t, 626.82, 0.4)
        draw_rect(f, 700, 720, 800, 760, RED, 0.4*a, width=2, radius=6)
        draw_text(f, "WRONG", 750, 740, 16, RED, 0.9*a)
        if t > 627.2: cross(f, 750, 686, 12, t, 627.3, RED, 4)
        chip(f, "WRONG DATA DISTURBS POLICY", 1240, 660, t, 626.9, RED, 20)
    if t > 630.3:
        a = ramp(t, 630.3, 0.5)
        shield_icon(f, 960, 640, 36, t, 630.3, GREEN)
        chip(f, "TRUST + VERIFY + COST", 960, 740, t, 630.5, GREEN, 24)

# ============ SCENE 19: EXPLORATION (634.5 - 676) ============
def sc_explore(f, t, A):
    chip(f, "EXPLORATION vs EXPLOITATION", 960, 180, t, 636.22, GOLD, 30)
    # fork
    if t > 636.6:
        a = ramp(t, 636.6, 0.6)
        draw_circle(f, 420, 620, 16, WHITE, 0.95*a)
        draw_text(f, "AGENT", 420, 680, 20, WHITE, 0.9*a)
        # known path
        pts1 = [(450, 610), (700, 560), (1000, 560), (1240, 560)]
        draw_polyline(f, pts1, GREEN, 5, 0.85*a)
        check(f, 1330, 560, 18, t, 637.4, GREEN)
        draw_text(f, "KNOWN", 1150, 520, 22, GREEN, 0.9*a)
        # new path
        pts2 = [(450, 640), (700, 760), (1000, 820), (1240, 840)]
        draw_polyline(f, pts2, GOLD, 5, 0.6*a, dash=16)
        draw_text(f, "?", 1330, 840, 52, GOLD, 0.95*a, glow=True)
        draw_text(f, "NEW", 1150, 900, 22, GOLD, 0.9*a)
    if t > 641.58: chip(f, "EXPLORE = TRY NEW ACTION", 700, 320, t, 641.58, GOLD, 24)
    if t > 644.56: chip(f, "EXPLOIT = USE KNOWN", 1260, 320, t, 644.56, GREEN, 24)
    # multi-agent exploration harder 650.02
    if t > 650.02:
        a = ramp(t, 650.02, 0.6)
        for i, (x, y, c) in enumerate([(560, 480, BLUE), (560, 640, TEAL), (560, 800, PURPLE)]):
            agent_node(f, x, y, t, 650.2+i*0.12, c, 13)
            pts = [(x+24, y), (x+180, y-40), (x+360, y+30)]
            draw_polyline(f, pts, c, 3, 0.5*a, dash=12)
        chip(f, "MULTI-AGENT: HARDER", 960, 400, t, 650.02, ORANGE, 24)
    if t > 653.84:
        a = ramp(t, 653.84, 0.5)
        # ripple on others
        for r in range(3):
            p = ((t-653.84)*0.7 + r*0.33) % 1.0
            draw_circle(f, 760, 640, 30+p*180, BLUE, 0.25*(1-p), width=2.5)
        chip(f, "ONE ROBOT'S EFFECT SPREADS", 1200, 740, t, 653.9, BLUE, 22,
             alpha=1 - ramp(t, 661.6, 0.8)) if t < 662.4 else None
    # team dips 657.34
    if t > 657.34:
        a = ramp(t, 657.34, 0.5)
        pts = []
        for i in range(100):
            x = 420+i*11
            y = 480 - i*0.6 + 90*np.exp(-((i-58)**2)/180.0)
            pts.append((x, y))
        draw_polyline(f, pts, RED, 4, 0.85*a)
        draw_text(f, "TEAM RESULT TEMPORARILY WEAK", 1000, 640, 22, RED, 0.9*a, anchor="lm")
    # safe exploration 662.64
    if t > 662.64:
        a = ramp(t, 662.64, 0.5)
        draw_circle(f, 560, 800, 60, GREEN, 0.2*a, width=3)
        robot_icon(f, 560, 800, t, 662.8, BLUE, 13)
        chip(f, "SAFE EXPLORATION", 700, 920, t, 662.7, GREEN, 24)
    if t > 669.38:
        a = ramp(t, 669.38, 0.4)
        draw_line(f, (900, 760), (1300, 760), GREY, 3, 0.7*a)
        draw_line(f, (900, 880), (1300, 880), GREY, 3, 0.7*a)
        chip(f, "SAFETY LIMITS", 1100, 720, t, 669.4, WHITE, 20)
    if t > 670.18:
        human_icon(f, 1100, 820, 22, t, 670.18, WHITE)
        chip(f, "HUMAN SUPERVISION", 1100, 930, t, 670.3, PURPLE, 20)
    if t > 675.06:
        a = ramp(t, 675.06, 0.4)
        pts2 = []
        for i in range(80):
            x = 420+i*8
            pts2.append((x, 500 - i*0.5 + 4*np.sin(i*0.3)))
        draw_polyline(f, pts2, GREEN, 4, 0.8*a)
        chip(f, "POLICY STABLE -> DEPLOY", 1180, 440, t, 675.06, GREEN, 24)
    if t > 677.84:
        a = ramp(t, 677.84, 0.5)
        draw_text(f, "SIM", 480, 950, 28, BLUE, 0.9*a)
        draw_arrow(f, (560, 950), (760, 950), WHITE, 4, a, head=16)
        draw_text(f, "REAL WORLD (CAREFULLY)", 1000, 950, 24, GREEN, 0.9*a, anchor="lm")

# ============ SCENE 20: EVALUATION (676 - 721.4) ============
def sc_eval(f, t, A):
    chip(f, "EVALUATION", 960, 170, t, 679.92, GOLD, 32)
    # win/loss not enough 682.06
    if t > 682.06:
        a = ramp(t, 682.06, 0.5)
        meter(f, 420, 320, 360, "WIN / LOSS", 0.75, t, 682.06, BLUE, 22)
        if t > 684.0: cross(f, 850, 330, 14, t, 684.0, RED, 4)
    # more meters
    items = [(687.14, "COORDINATION QUALITY", 0.8, GREEN, 420, 430),
             (691.76, "AVERAGE SPEED", 0.7, BLUE, 420, 530),
             (692.54, "WAITING TIME", 0.35, ORANGE, 420, 630),
             (693.64, "EMERGENCY RESPONSE", 0.9, RED, 420, 730)]
    for t0, txt, v, c, x, y in items:
        if t > t0: meter(f, x, y, 520, txt, v, t, t0, c, 22)
    # warehouse metrics
    items2 = [(698.06, "COLLISIONS", 0.12, RED, 1100, 430),
              (699.04, "ENERGY USE", 0.5, TEAL, 1100, 530),
              (708.10, "FAIRNESS", 0.85, GREEN, 1100, 630)]
    for t0, txt, v, c, x, y in items2:
        if t > t0: meter(f, x, y, 460, txt, v, t, t0, c, 22)
    # task imbalance 703.1
    if t > 703.1 and t < 710.0:
        a = fade(t, 703.1, 710.5, 0.4, 0.4)
        box_icon(f, 1160, 760, 22, t, 703.2, ORANGE)
        draw_text(f, "HARD TASKS", 1240, 760, 20, WHITE, 0.9*a, anchor="lm")
        box_icon(f, 1160, 850, 12, t, 704.82, GREY)
        draw_text(f, "EASY TASKS", 1240, 850, 20, WHITE, 0.9*a, anchor="lm")
        robot_icon(f, 1080, 760, t, 703.3, BLUE, 12)
        robot_icon(f, 1080, 850, t, 704.9, TEAL, 12)
    if t > 705.0 and t < 710.5:
        chip(f, "TOTAL REWARD OK", 1560, 800, t, 705.2, BLUE, 20)
    if t > 708.1:
        chip(f, "BUT TEAM NOT FAIR", 1330, 700, t, 708.1, RED, 22)
    # different numbers of agents 710.52
    if t > 710.52:
        for i, n in enumerate(["2", "5", "10"]):
            chip(f, f"{n} AGENTS", 500+i*220, 900, t, 710.52+i*0.2, BLUE, 24)
        if t > 712.98:
            # surprise pop
            px = 1380
            a = ramp(t, 712.98, 0.3)
            pulse_ring(f, px, 900, t, 712.98, RED, 12, 60, 0.7)
            chip(f, "UNEXPECTED SITUATIONS", px, 970, t, 713.0, RED, 22)
    if t > 715.62:
        a = ramp(t, 715.62, 0.5)
        shield_icon(f, 960, 1000, 30, t, 715.62, GREEN)
        chip(f, "ROBUST IN UNSEEN CONDITIONS", 1240, 1000, t, 715.7, GREEN, 22, pad=10)

# ============ SCENE 21: FUTURE (721.4 - 779.4) ============
def sc_future(f, t, A):
    chip(f, "FUTURE OF MARL", 960, 170, t, 721.44, GOLD, 32)
    # horizon glow
    if t > 721.8:
        a = ramp(t, 721.8, 1.0)
        glow(f, 960, 900, 260, BLUE_D, 0.20*a, scale=1.6)
    # five domain icons arc 727.9
    domains = [(500, 620, "FACTORIES", 727.9), (730, 520, "AUTONOMOUS CARS", 729.02),
               (960, 480, "HEALTHCARE", 730.44), (1190, 520, "DISASTER RESPONSE", 731.98),
               (1420, 620, "ENERGY GRIDS", 733.9)]
    for x, y, txt, t0 in domains:
        if t > t0 and t < 760.5:
            a = ramp(t, t0, 0.5, "back") * (1 - ramp(t, 759.5, 1.0))
            draw_rect(f, x-70, y-56, x+70, y+56, (30, 38, 52), 0.85*a, width=2.5, radius=12)
            cx, cy = x, y-14
            if "FACTORIES" in txt:
                draw_rect(f, cx-34, cy-6, cx+34, cy+30, BLUE, 0.3*a, width=2, radius=3)
                draw_rect(f, cx-10, cy-30, cx+2, cy-6, BLUE, 0.5*a, width=0)
            elif "CARS" in txt:
                draw_rect(f, cx-36, cy, cx+36, cy+18, BLUE, 0.35*a, width=2, radius=6)
                draw_circle(f, cx-18, cy+22, 8, GREY, a); draw_circle(f, cx+18, cy+22, 8, GREY, a)
            elif "HEALTH" in txt:
                draw_line(f, (cx, cy-20), (cx, cy+20), GREEN, 6, a)
                draw_line(f, (cx-20, cy), (cx+20, cy), GREEN, 6, a)
            elif "DISASTER" in txt:
                draw_poly_fill(f, [(cx, cy-24), (cx+18, cy+12), (cx-18, cy+12)], RED, 0.5*a)
                draw_text(f, "!", cx, cy+1, 18, WHITE, a)
            else:
                draw_polyline(f, [(cx+6, cy-24), (cx-10, cy+2), (cx+4, cy+2), (cx-6, cy+24), (cx+14, cy-4), (cx+0, cy-4)], GOLD, 3.5, a)
            draw_text(f, txt, x, y+82, 19, WHITE, 0.9*a)
    # agents web 736.3
    if 736.32 < t < 760.5:
        a = ramp(t, 736.32, 0.7) * (1 - ramp(t, 759.5, 1.0))
        for i in range(len(domains)-1):
            x1, y1 = domains[i][:2]; x2, y2 = domains[i+1][:2]
            draw_line(f, (x1, y1+10), (x2, y2+10), BLUE, 1.5, 0.4*a, dash=10)
        chip(f, "MANY AI AGENTS WORKING TOGETHER", 960, 340, t, 736.4, BLUE, 24)
    # responsibility 739.54
    if 739.54 < t < 760.5:
        a = ramp(t, 739.54, 0.5) * (1 - ramp(t, 759.5, 1.0))
        shield_icon(f, 960, 700, 40, t, 739.54, GREEN)
        chip(f, "RESPONSIBILITY", 960, 780, t, 739.6, GREEN, 26)
    if 742.06 < t < 760.5:
        a = 1 - ramp(t, 759.5, 1.0)
        lock_icon(f, 700, 900, 18, t, 742.06, PURPLE)
        draw_text(f, "PRIVACY", 700, 956, 20, PURPLE, 0.9*a)
    if 743.86 < t < 760.5:
        a = 1 - ramp(t, 759.5, 1.0)
        draw_line(f, (960-40, 890), (960+40, 890), WHITE, 3, ramp(t, 743.86, 0.4)*a)
        draw_circle(f, 960, 878, 6, WHITE, ramp(t, 743.86, 0.4)*a)
        draw_text(f, "FAIRNESS", 960, 956, 20, WHITE, 0.9*a)
    if 744.68 < t < 760.5:
        a = 1 - ramp(t, 759.5, 1.0)
        human_icon(f, 1220, 900, 20, t, 744.68, WHITE)
        draw_text(f, "HUMAN RULES", 1220, 956, 20, WHITE, 0.9*a)
    # wrong objective 748.36
    if 748.36 < t < 755.68:
        a = fade(t, 748.36, 755.68, 0.4, 0.5)
        # wrong goal flag left, fast arrows into it
        flag(f, 420, 560, t, 748.4, RED, 26)
        for k in range(3):
            p = ((t-748.6)*0.7+k/3) % 1.0
            px = 900 - 400*p
            draw_arrow(f, (px+30, 560), (px, 560), RED, 3, 0.7*a, head=10)
        chip(f, "WRONG GOAL = EFFICIENTLY WRONG", 960, 395, t, 750.5, RED, 26)
    # better goals 755.68
    if 755.68 < t < 760.5:
        a = ramp(t, 755.68, 0.5) * (1 - ramp(t, 759.6, 0.9))
        flag(f, 420, 560, t, 755.7, GREEN, 26)
        draw_arrow(f, (900, 560), (480, 560), GREEN, 4, a, head=14)
        chip(f, "BETTER GOALS", 700, 470, t, 755.8, GREEN, 24)
    if 756.46 < t < 760.5:
        a = 1 - ramp(t, 759.6, 0.9)
        chip(f, "TRANSPARENT FEEDBACK", 1140, 470, t, 756.46, BLUE, 22)
    if 758.3 < t < 760.5:
        a = 1 - ramp(t, 759.6, 0.9)
        human_icon(f, 1240, 420, 22, t, 758.3, WHITE)
        draw_text(f, "HUMAN OVERSIGHT", 1240, 480, 22, WHITE, 0.9*a)
    # final message 760.78
    if t > 760.78:
        a = ramp(t, 760.78, 0.8)
        brain_icon(f, 700, 540, 30, t, 761.0, PURPLE)
        for i, (x, y) in enumerate([(1000, 460), (1060, 580), (960, 660)]):
            agent_node(f, x, y, t, 761.4+i*0.15, BLUE, 13)
            draw_line(f, (740, 540), (x-16, y), PURPLE, 2, 0.5*a)
        chip(f, "COORDINATION IS PART OF INTELLIGENCE", 960, 1010, t, 762.72, GOLD, 26)
    # shared world globe 766.1
    if t > 766.1:
        a = ramp(t, 766.1, 0.8)
        draw_circle(f, 960, 580, 110, BLUE_D, 0.25*a, width=3)
        draw_circle(f, 960, 580, 110, BLUE, 0.12*a)
        for k in range(6):
            ang = k*np.pi/3 + (t-766.1)*0.3
            x = 960 + np.cos(ang)*140
            y = 580 + np.sin(ang)*85
            agent_node(f, x, y, t, 766.3+k*0.1, BLUE if k % 2 == 0 else TEAL, 9)
    if t > 771.76:
        a = ramp(t, 771.76, 0.6)
        chip(f, "SMART IS NOT ENOUGH", 960, 250, t, 771.76, WHITE, 28)
    if t > 777.68:
        a = ramp(t, 777.68, 0.35)
        chip(f, "COOPERATE RESPONSIBLY", 960, 340, t, 777.68, GREEN, 30)
        pulse_ring(f, 960, 580, t, 777.7, GOLD, 130, 220, 1.4)

DRAW_B = [
    (348.08, 370.02, sc_ctde),
    (370.02, 451.50, sc_limits),
    (451.50, 506.14, sc_recap),
    (506.14, 547.88, sc_teamgame),
    (547.88, 589.88, sc_stability),
    (589.88, 634.52, sc_comm),
    (634.52, 678.80, sc_explore),
    (678.80, 721.44, sc_eval),
    (721.44, 779.40, sc_future),
]
