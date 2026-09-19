#!/usr/bin/env python3
"""P4 spelling sweep (VIDEO_RULES §3): extract screen-text literals from scene
modules via AST (strings passed to draw/text/chip helpers), check spelling."""
import ast, re, sys
from spellchecker import SpellChecker

FILES = ["/home/z/my-project/scripts/scenes_a.py", "/home/z/my-project/scripts/scenes_b.py"]
DRAW_FUNCS = {"draw_text", "chip", "draw_chip", "label", "text", "draw_label", "pill", "tag", "title", "draw_title"}

# domain whitelist: MARL/RL terms, tech words, names used on screen
WHITELIST = {
    "marl", "rl", "mdp", "q", "qlearning", "policy", "policies", "reward", "rewards",
    "agent", "agents", "multi", "observation", "observations", "action", "actions",
    "state", "states", "env", "environment", "coop", "comp", "cooperation", "competition",
    "nonstationary", "stationary", "credit", "assignment", "reward", "sparse", "delayed",
    "exploration", "exploitation", "epsilon", "greedy", "softmax", "gradient", "gradients",
    "ppo", "dqn", "qmix", "vdn", "commnet", "tarMAC".lower(), "maddpg", "ctde",
    "centralized", "decentralized", "training", "inference", "rollout", "rollouts",
    "episode", "episodes", "timestep", "timesteps", "trajectory", "trajectories",
    "warehouse", "drones", "drone", "robots", "robot", "soccer", "traffic", "grid",
    "sensor", "sensors", "lidar", "gps", "bandwidth", "latency", "protocol", "protocols",
    "scalability", "sample", "efficiency", "explainability", "interpretability",
    "reward", "design", "hacking", "specification", "game", "games", "optimization",
    "coordination", "coverage", "swarm", "formation", "planning", "reasoning", "memory",
    "verify", "verified", "trust", "cost", "late", "missed", "selective", "communication",
    "token", "tokens", "batch", "gpu", "cpu", "async", "sync", "parallel", "envs",
    "selfplay", "self", "play", "opponent", "opponents", "nash", "equilibrium",
    "minimax", "arena", "tournament", "elo", "league", "openai", "deepmind", "alphastar",
    "alphago", "zeroplayer", "zero", "sum", "coopetition", "emergent", "emergence",
    "curriculum", "prioritized", "replay", "buffer", "target", "network", "networks",
    "nn", "mlp", "cnn", "rnn", "lstm", "attention", "transformer", "gnn", "gnns",
    "hyperparams", "hyper", "params", "tune", "tuning", "seed", "seeds", "eval", "evals",
    "test", "tests", "train", "val", "validation", "overfit", "underfit", "loss", "losses",
    "entropy", "baseline", "baselines", "advantage", "advantages", "critic", "actor",
    "value", "func", "function", "approximation", "bellman", "backup", "bootstrapping",
    "dispatch", "router", "routing", "message", "messages", "msg", "mailbox", "inbox",
    "broadcast", "unicast", "multicast", "topology", "graph", "graphs", "node", "nodes",
    "edge", "edges", "decentralised", "decentralized", "fairness", "privacy", "safety",
    "human", "rules", "responsibility", "healthcare", "factories", "energy", "grids",
    "cars", "autonomous", "disaster", "response", "prediction", "predictions", "forecast",
    "sensor", "noisy", "noise", "partial", "observability", "pomdp", "belief", "beliefs",
    "hidden", "state", "latent", "embedding", "embeddings", "encoder", "decoder",
}

def screen_strings(path):
    out = []
    tree = ast.parse(open(path).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func.id if isinstance(node.func, ast.Name) else (
                 node.func.attr if isinstance(node.func, ast.Attribute) else "")
            if fn.lower() in DRAW_FUNCS:
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        out.append((path.split("/")[-1], node.lineno, arg.value))
    return out

def looks_like_screen_text(s):
    if len(s) < 2 or len(s) > 60: return False
    if any(c in s for c in "/\\_.py#:{}[]<>") or "\n" in s: return False
    if not re.search(r"[A-Za-z]{2,}", s): return False
    words = re.findall(r"[A-Za-z']+", s)
    if not words: return False
    upperish = sum(1 for w in words if w.isupper() or w.istitle() or w.lower() in WHITELIST)
    return upperish >= max(1, len(words) - 1)

spell = SpellChecker()
issues, checked = [], 0
for path in FILES:
    for f, ln, s in screen_strings(path):
        if not looks_like_screen_text(s): continue
        checked += 1
        for w in re.findall(r"[A-Za-z']+", s):
            wl = w.lower().strip("'")
            if wl in WHITELIST or len(wl) <= 2: continue
            if wl not in spell:
                issues.append((f, ln, s, w))

print(f"screen-text strings checked: {checked}")
if issues:
    print("SUSPECTS:")
    for f, ln, s, w in issues:
        print(f"  {f}:{ln}  word={w!r}  in={s!r}")
else:
    print("P4 PASS: no misspellings")
