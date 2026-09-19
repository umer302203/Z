#!/usr/bin/env python3
"""Build the word-level EVENT MAP: search transcript for anchor words,
record exact spoken timestamps -> events.json (authoritative sync map)."""
import json, re, unicodedata

TR = "/home/z/my-project/work/marl_video/transcript_hi_words.json"
OUT = "/home/z/my-project/work/marl_video/events.json"

d = json.load(open(TR))
words = d["words"]

def norm(s):
    # strip diacritics/normalize for matching
    return re.sub(r"\s+", "", s)

# search patterns: list of substrings that may appear in a word token
# (Hindi script or romanized English). Returns first match time >= tmin.
def find(pat, tmin=0.0, tmax=1e9, nth=0):
    hits = []
    for w in words:
        if w["start"] < tmin or w["start"] > tmax:
            continue
        if pat in w["word"] or pat in norm(w["word"]):
            hits.append(w)
    return hits[nth] if len(hits) > nth else None

def show(label, *args, **kw):
    w = find(*args, **kw)
    if w:
        print(f"{label:38s} {w['start']:8.2f}  '{w['word']}'")
        return w["start"]
    else:
        print(f"{label:38s}   *** NOT FOUND ***")
        return None

# --- verify key anchors across the whole narration ---
anchors = {}
Q = [
    ("football",        "football", 0, 10),
    ("match",           "match", 0, 10),
    ("ground",          None, 0, 8),          # ग्राउन
    ("rules",           None, 0, 8),          # रूलज
    ("players22",       "भीस", 3, 7),
    ("position",        "position", 5, 9),
    ("teammates",       "teammates", 6, 10),
    ("opponents",       "opponents", 7, 11),
    ("decision",        "decision", 8, 12),
    ("pass",            "पास", 11, 14),
    ("cover",           "कवर", 13, 16),
    ("attack",          "attack", 14, 18),
    ("result",          "result", 16, 20),
    ("imagine",         "एमजन", 19, 23),
    ("computer",        "कम्पुटर", 19, 23),
    ("programs",        "प्रोग्राम", 20, 24),
    ("marl_start",      "multi-agent", 22, 27),
    ("agent_sys",       "agent", 26, 31),
    ("environment1",    "environment", 28, 33),
    ("world",           "दूनिया", 31, 34),
    ("info",            "एनवोवेंश", 35, 38),     # observation (ASR garbled)
    ("choose_action",   "आश्चन", 37, 39),
    ("reward1",         "रिवार्ड", 38, 42),
    ("penalty1",        "पनल्टी", 40, 42),
    ("learn_slowly",    "सीकता", 42, 46),
    ("robot_maze",      "रोबोट", 46, 49),
    ("maze",            "मेज", 46, 49),
    ("exit",            "एकसिट", 47, 50),
    ("wall",            "वोल्ट", 50, 52),
    ("many_agents",     "कई", 50, 54),
    ("marl_word",       "मारल", 55, 58),
    ("observation2",    "अबसूवेश", 58, 61),
    ("policy1",         "पूलिसी", 61, 64),
    ("rule",            "रूल", 64, 66),
    ("others_act",      "अच्छन्स", 69, 72),
    ("env_changing",    "बडल", 72, 75),
    ("walls_roads",     "वूल्स", 74, 78),
    ("intelligent",     "इंटेलज्ट", 78, 81),
    # charging / competition
    ("two_robots",      "रोबाट्स", 91, 94),
    ("charging",        "चार्जिंग", 92, 95),
    ("competition",     "कोमपेटिशन", 94, 96),
    ("routes",          "रोट्स", 96, 99),
    ("delivery",        "दिलिव्रीस", 97, 100),
    ("cooperation",     "कोपरेशन", 98, 101),
    ("common_goal",     "कोमन", 100, 103),
    ("opposite",        "औबजित", 108, 112),
    ("wins",            "जीता", 111, 114),
    ("loses",           "हार्ता", 112, 115),
    ("strategy_game",   "स्थातिजी", 114, 118),
    ("resources",       "रीशुरस", 115, 119),
    # non-stationary
    ("nonstat",         "non-stationary", 127, 132),
    ("strategy_change", "strategy", 131, 136),
    ("defense",         "defense", 136, 139),
    ("attack_change",   "attack", 137, 140),
    ("better_each",     "better", 139, 142),
    ("both_co_comp",    "cooperation", 142, 146),
    # credit assignment
    ("credit1",         "credit", 149, 152),
    ("team_reward",     "reward", 151, 155),
    ("contribution",    "contribution", 154, 158),
    ("four_robots",     "4", 157, 162),
    ("heavy_box",       "box", 158, 162),
    ("box_dest",        "destination", 161, 165),
    ("direction",       "direction", 165, 169),
    ("push",            "push", 166, 171),
    ("clear_path",      "rasta", 169, 173),
    ("fourth_idle",     "4", 171, 174),
    ("same_reward",     "reward", 173, 179),
    ("inactive",        "inactive", 174, 179),
    ("shared_reward",   "shared", 184, 189),
    ("individual_rew",  "individual", 185, 192),
    ("balance",         "balance", 194, 198),
    ("selfish",         "selfish", 196, 201),
    # delayed
    ("delayed",         "delayed", 200, 203),
    ("action_now",      "action", 202, 205),
    ("result_later",    "result", 204, 207),
    ("drone_route",     "drone", 206, 209),
    ("ten_min",         "10", 208, 211),
    ("temporal",        "temporal", 214, 218),
    ("manager",         "manager", 217, 221),
    ("feedback",        "feedback", 218, 223),
    ("reward_signal",   "signal", 228, 233),
    ("subgoals",        "sub", 235, 240),
    # partial observability
    ("partial_obs",     "partial", 239, 243),
    ("hissa",           "hissa", 241, 246),
    ("rescue_robot",    "rescue", 245, 249),
    ("corridor",        "corridor", 246, 250),
    ("hidden_info",     "hidden", 250, 256),
    ("memory_comm",     "memory", 255, 260),
    ("left_corr",       "left", 258, 263),
    # communication
    ("comm_guess",      "guess", 268, 274),
    ("comm_fast",       "communication", 272, 277),
    # applications
    ("real_world",      "real", 281, 286),
    ("traffic_mgmt",    "traffic", 285, 289),
    ("lights",          "lights", 287, 293),
    ("signal_coord",    "coordinate", 293, 297),
    ("jam",             "jam", 298, 303),
    ("smooth_flow",     "flow", 301, 306),
    ("warehouse",       "warehouse", 304, 308),
    ("packages",        "packages", 307, 311),
    ("busy_aisles",     "ais", 310, 315),
    ("task_divide",     "divide", 313, 317),
    ("charging_conf",   "charging", 316, 321),
    ("collision_avoid", "collision", 320, 326),
    ("drones_app",      "drones", 325, 329),
    ("large_area",      "large", 328, 332),
    ("random_route",    "random", 331, 336),
    ("coverage",        "coverage", 335, 342),
    ("detect_object",   "detect", 342, 348),
    # CTDE
    ("centralized",     "centralized", 348, 354),
    ("decentralized",   "decentralized", 348, 354),
    ("training_time",   "training", 353, 358),
    ("coord_seekhna",   "coordination", 357, 361),
    ("local_obs_act",   "local", 359, 366),
    ("training_room",   "training", 364, 370),
    ("sensors",         "sensors", 366, 371),
    # limitations
    ("limitations",     "limitations", 370, 374),
    ("sample_eff",      "sample", 372, 377),
    ("trials",          "trials", 374, 380),
    ("expensive",       "expensive", 379, 384),
    ("simulation",      "simulation", 383, 387),
    ("sim2real",        "sim", 386, 392),
    ("scalability",     "scalability", 391, 395),
    ("interactions",    "interactions", 395, 400),
    ("reward_design",   "reward", 402, 407),
    ("speed_reward",    "speed", 405, 410),
    ("safety_ignore",   "safety", 408, 413),
    ("explainability",  "explain", 412, 417),
    ("why_decision",    "why", 424, 429),
    ("safety_const",    "safety", 436, 441),
    ("narrow_corr",     "narrow", 439, 445),
    # recap 451-506
    ("core_idea",       "core", 451, 456),
    ("shared_env2",     "shared", 453, 459),
    ("policies_act",    "Policies", 458, 462),
    ("rewards_fb",      "rewards", 460, 466),
    ("single_vs_multi", "Single", 471, 476),
    ("cars_share",      "Cars", 482, 488),
    ("robots_share",    "robots", 484, 489),
    ("drones_share",    "drones", 486, 491),
    ("humans_ai",       "Humans", 489, 493),
    ("final_q",         "intelligence", 493, 499),
    ("coordination_q",  "coordination", 495, 500),
    ("future_sys",      "future", 499, 504),
    ("smart_coop",      "cooperate", 503, 507),
    # team game example 506-550
    ("team_game",       "team", 506, 510),
    ("three_agents",    "3", 508, 512),
    ("digital_field",   "digital", 509, 513),
    ("a1_observe",      "observe", 510, 514),
    ("a2_route",        "route", 512, 516),
    ("a3_objective",    "objective", 514, 518),
    ("independent",     "independently", 516, 522),
    ("duplication",     "duplication", 520, 525),
    ("role_policies",   "role", 521, 527),
    ("info_share",      "information", 525, 530),
    ("route_plan",      "route", 527, 531),
    ("execute",         "execute", 528, 532),
    ("role_samjhe",     "role", 534, 539),
    ("support_others",  "support", 536, 541),
    ("reward_fb2",      "feedback", 544, 549),
    # stability 547-590
    ("stability",       "stability", 547, 553),
    ("policy_improve",  "improve", 550, 555),
    ("policies_update", "policies", 552, 557),
    ("today_fails",     "fail", 556, 561),
    ("driver_route",    "driver", 560, 564),
    ("same_route",      "route", 562, 568),
    ("slow_route",      "slow", 565, 569),
    ("traffic_pattern", "pattern", 568, 573),
    ("fixed_rules",     "fixed", 574, 579),
    ("uncertainty",     "uncertainty", 578, 584),
    ("adapt",           "adapt", 581, 586),
    ("opponent_model",  "Opponent", 584, 589),
    ("population",      "population", 585, 590),
    # communication design 590-634
    ("comm_central",    "Communication", 589, 594),
    ("unlimited",       "unlimited", 594, 598),
    ("noisy_slow",      "noisy", 596, 602),
    ("when_whom_what",  "kab", 600, 606),
    ("exact_pos",       "position", 606, 612),
    ("sensor_reading",  "sensor", 609, 614),
    ("drone_conf",      "confidence", 613, 618),
    ("selective",       "selective", 616, 621),
    ("right_time",      "time", 620, 626),
    ("late_msg",        "late", 623, 628),
    ("wrong_msg",       "wrong", 626, 631),
    ("trust_verify",    "trust", 629, 634),
    # exploration 634-676
    ("exploration",     "exploration", 635, 642),
    ("exploitation",    "exploitation", 635, 643),
    ("new_action",      "new", 640, 644),
    ("known_action",    "action", 643, 648),
    ("explore_harder",  "difficult", 647, 652),
    ("affects_others",  "effect", 653, 658),
    ("test_strategy",   "strategy", 658, 662),
    ("team_weak",       "weak", 659, 664),
    ("safe_explore",    "safe", 660, 666),
    ("safety_limits",   "limits", 668, 673),
    ("human_super",     "human", 670, 675),
    ("policy_stable",   "stable", 674, 679),
    ("deploy_real",     "deploy", 676, 681),
    # evaluation 676-721
    ("eval_sys",        "evaluate", 678, 684),
    ("win_loss",        "win", 681, 686),
    ("coord_quality",   "co-ordination", 686, 691),
    ("avg_speed",       "speed", 690, 695),
    ("waiting_time",    "waiting", 691, 696),
    ("emergency",       "emergency", 692, 697),
    ("collisions2",     "collisions", 697, 703),
    ("energy_use",      "energy", 698, 703),
    ("fairness",        "fairness", 701, 707),
    ("hard_tasks",      "difficult", 703, 708),
    ("easy_tasks",      "easy", 704, 709),
    ("team_unfair",     "fair", 707, 711),
    ("num_agents",      "numbers", 709, 714),
    ("unexpected",      "unexpected", 711, 716),
    ("robust",          "Robust", 715, 719),
    ("unseen",          "unseen", 718, 722),
    # future 721-779
    ("future_marl",     "Future", 721, 726),
    ("smart_factory",   "factories", 727, 731),
    ("autonomous_v",    "autonomous", 728, 733),
    ("healthcare",      "healthcare", 730, 735),
    ("disaster",        "disaster", 732, 737),
    ("energy_grid",     "energy", 735, 739),
    ("responsibility",  "responsibility", 738, 743),
    ("privacy",         "privacy", 741, 746),
    ("fairness2",       "fairness", 742, 747),
    ("human_instr",     "human", 743, 748),
    ("wrong_objective", "gulat", 747, 752),
    ("efficient_wrong", "efficiently", 750, 755),
    ("better_goals",    "goals", 753, 758),
    ("transparent",     "transparent", 755, 760),
    ("human_oversight", "oversight", 756, 761),
    ("marl_teaches",    "समझति", 759, 763),
    ("individual_dec",  "individual", 761, 765),
    ("shared_world",    "shared", 766, 771),
    ("coord_intel",     "coordination", 768, 773),
    ("akhir",           "Akhir", 771, 775),
    ("responsibly",     "responsibly", 775, 779),
]

for label, pat, a, b in Q:
    if pat is None:
        continue
    t = show(label, pat, a, b)
    if t is not None:
        anchors[label] = round(t, 3)

json.dump(anchors, open("/home/z/my-project/work/marl_video/anchors_raw.json", "w"), indent=1)
print(f"\n{len(anchors)}/{len(Q)} anchors found")
