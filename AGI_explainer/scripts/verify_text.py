"""verify_text.py — TEXT RULE verifier (v3): every ON-SCREEN string
<= 3 English words (symbols allowed: = ≠ ? · - + × → ✓ ✗ : / . , % ( )).
AST scan: strings passed to text3d/chip/sticky_note/_title + SEQ 'title' values.
Run: python3 verify_text.py"""
import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['specs.py', 'lib_scene.py']
TEXT_FUNCS = {'text3d': 1, 'chip': 1, 'sticky_note': 1, '_title': 2}
ALLOWED = set("=≠?·-+×→✓✗:/.,%() '\"_#[]@!&\n\t-")

def ok(s):
    toks = re.findall(r"[A-Za-z0-9]+", s)
    if len(toks) > 3:
        return False
    return all(c in ALLOWED or c.isalnum() for c in s)

def collect(tree, path, out):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in TEXT_FUNCS:
            i = TEXT_FUNCS[node.func.id]
            if len(node.args) > i and isinstance(node.args[i], ast.Constant) \
                    and isinstance(node.args[i].value, str):
                out.append((path, node.args[i].value))
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == 'title' \
                        and isinstance(v, ast.Constant) \
                        and isinstance(v.value, str):
                    out.append((path, v.value))

def main():
    seen, bad = set(), []
    for fn in FILES:
        with open(os.path.join(HERE, fn), encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=fn)
        found = []
        collect(tree, fn, found)
        for src, s in found:
            if (src, s) in seen:
                continue
            seen.add((src, s))
            if not ok(s):
                bad.append((src, s))
    for src, s in bad:
        print(f'VIOLATION {src}: {s!r}')
    print(f'TEXT RULE: {"PASS" if not bad else "FAIL"} '
          f'({len(seen) - len(bad)}/{len(seen)} on-screen strings)')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
