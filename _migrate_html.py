"""
Migrate all st.markdown(..., unsafe_allow_html=True) calls to st.html()
across the Spotify BI dashboard project.

Handles:
  1. st.markdown(X, unsafe_allow_html=True)
  2. st.markdown(\n    X,\n    unsafe_allow_html=True,\n)
  3. st.sidebar.markdown(X, unsafe_allow_html=True)
  4. col.markdown(X, unsafe_allow_html=True)
  5. <ctx>.markdown(<br>, unsafe_allow_html=True)  -> <ctx>.html("<br>")
  6. st.sidebar.markdown("---") stays as-is (pure markdown, no HTML)
"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "app.py",
    "utils/theme.py",
    "pages/1_Executive_Overview.py",
    "pages/2_Hit_Predictor.py",
    "pages/3_Revenue_Intelligence.py",
    "pages/4_Emerging_Artists_Radar.py",
    "pages/5_Playlist_Curator.py",
]

def migrate(content: str) -> str:
    # ── Strategy ──────────────────────────────────────────────────────────────
    # We process the whole file as a string.  We look for any call of the form:
    #   <prefix>.markdown(<body>, unsafe_allow_html=True <optionally ,> )
    # and convert it to:
    #   <prefix>.html(<body>)
    #
    # The tricky part is that <body> itself can span many lines and contain
    # nested parentheses (e.g. f-strings with function calls).
    # We use a simple state machine: once we find `.markdown(` followed (at some
    # point) by `unsafe_allow_html=True`, we rewrite the whole call.
    # ──────────────────────────────────────────────────────────────────────────

    # Pass 1: tokenise into a list of segments so we can reconstruct later.
    # We scan for occurrences of   SOMETHING.markdown(
    # then walk forward counting parens to find the matching close paren.

    result = []
    i = 0
    n = len(content)

    # Regex to find the start of .markdown( (with optional whitespace after the dot)
    start_re = re.compile(r'\.(markdown)\s*\(', re.DOTALL)

    while i < n:
        m = start_re.search(content, i)
        if m is None:
            result.append(content[i:])
            break

        # Capture everything before this match verbatim
        result.append(content[i:m.start()])

        # Walk forward past the opening paren, counting depth
        depth = 1
        j = m.end()          # position just after the opening '('
        while j < n and depth > 0:
            c = content[j]
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            j += 1
        # j now points to one char after the matching ')'
        # full_call = content[m.start() : j]
        inner = content[m.end() : j - 1]   # everything between ( and )

        # Does this call contain unsafe_allow_html=True ?
        if 'unsafe_allow_html=True' in inner:
            # --- rewrite ---
            # Remove `unsafe_allow_html=True` (with optional leading comma+spaces)
            # and any trailing comma that would be left dangling
            cleaned = re.sub(
                r',?\s*unsafe_allow_html\s*=\s*True\s*,?',
                '',
                inner,
                flags=re.DOTALL,
            )
            # Strip trailing comma/whitespace before the closing paren
            cleaned = cleaned.rstrip()
            if cleaned.endswith(','):
                cleaned = cleaned[:-1].rstrip()
            result.append('.html(' + cleaned + ')')
        else:
            # Leave untouched
            result.append(content[m.start():j])

        i = j

    return ''.join(result)


def process_file(rel_path: str) -> None:
    path = os.path.join(BASE, rel_path)
    with open(path, 'r', encoding='utf-8') as fh:
        original = fh.read()

    migrated = migrate(original)

    if migrated == original:
        print(f"  (no changes) {rel_path}")
        return

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(migrated)

    # Quick count
    before = original.count('unsafe_allow_html=True')
    after  = migrated.count('unsafe_allow_html=True')
    print(f"  ✓ {rel_path}  ({before} → {after} unsafe_allow_html occurrences)")


if __name__ == '__main__':
    print("Migrating st.markdown(html, unsafe_allow_html=True) → st.html(html) …\n")
    for f in FILES:
        process_file(f)
    print("\nDone.")
