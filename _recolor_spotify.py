"""
Recolor the Spotify BI dashboard to match Spotify's actual brand palette.

Spotify brand colors:
  Green  (primary accent)   : #1DB954   rgba(29,185,84,...)
  Blue   (secondary accent) : #509BF5   rgba(80,155,245,...)
  Black  (app background)   : #121212
  Dark   (sidebar/surface)  : #0d0d0d  / #101010
  Surface                   : #181818
  Card                      : #242424  / #282828
  White  (text)             : #ffffff
  Gray   (muted text)       : #b3b3b3
  Dark gray (captions)      : #727272
  Dimmer                    : #535353
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── colour substitution map (order matters — more specific first) ─────────────
REPLACEMENTS = [
    # Accent green   #00e5a0 → #1DB954
    ("#00e5a0",                      "#1DB954"),
    ("rgba(0,229,160,0.30)",         "rgba(29,185,84,0.30)"),
    ("rgba(0,229,160,0.35)",         "rgba(29,185,84,0.35)"),
    ("rgba(0,229,160,0.45)",         "rgba(29,185,84,0.45)"),
    ("rgba(0,229,160,0.55)",         "rgba(29,185,84,0.55)"),
    ("rgba(0,229,160,0.80)",         "rgba(29,185,84,0.80)"),
    ("rgba(0,229,160,0.8)",          "rgba(29,185,84,0.8)"),
    ("rgba(0,229,160,0.25)",         "rgba(29,185,84,0.25)"),
    ("rgba(0,229,160,0.22)",         "rgba(29,185,84,0.22)"),
    ("rgba(0,229,160,0.20)",         "rgba(29,185,84,0.20)"),
    ("rgba(0,229,160,0.18)",         "rgba(29,185,84,0.18)"),
    ("rgba(0,229,160,0.14)",         "rgba(29,185,84,0.14)"),
    ("rgba(0,229,160,0.13)",         "rgba(29,185,84,0.13)"),
    ("rgba(0,229,160,0.10)",         "rgba(29,185,84,0.10)"),
    ("rgba(0,229,160,0.08)",         "rgba(29,185,84,0.08)"),
    ("rgba(0,229,160,0.06)",         "rgba(29,185,84,0.06)"),
    ("rgba(0,229,160,0.055)",        "rgba(29,185,84,0.055)"),
    ("rgba(0,229,160,0.05)",         "rgba(29,185,84,0.05)"),
    ("rgba(0,229,160,0.025)",        "rgba(29,185,84,0.025)"),
    ("rgba(0,229,160,0.0)",          "rgba(29,185,84,0.0)"),

    # Purple/violet  #7b61ff → #509BF5  (Spotify's blue)
    ("#7b61ff",                      "#509BF5"),
    ("rgba(123,97,255,0.30)",        "rgba(80,155,245,0.30)"),
    ("rgba(123,97,255,0.35)",        "rgba(80,155,245,0.35)"),
    ("rgba(123,97,255,0.28)",        "rgba(80,155,245,0.28)"),
    ("rgba(123,97,255,0.20)",        "rgba(80,155,245,0.20)"),
    ("rgba(123,97,255,0.18)",        "rgba(80,155,245,0.18)"),
    ("rgba(123,97,255,0.08)",        "rgba(80,155,245,0.08)"),
    ("rgba(123,97,255,0.07)",        "rgba(80,155,245,0.07)"),
    ("rgba(123,97,255,0.055)",       "rgba(80,155,245,0.055)"),

    # App / chart background  #0a0a0f → #121212
    ("#0a0a0f",                      "#121212"),
    # Sidebar gradient pieces
    ("#070710",                      "#0d0d0d"),
    ("#0d0d1a",                      "#161616"),
    # Config secondary BG
    ("#0f0f1a",                      "#121212"),
    ("#13132b",                      "#181818"),

    # Surfaces
    ("#10101e",                      "#181818"),
    ("#101020",                      "#181818"),
    ("#141430",                      "#242424"),
    ("#151528",                      "#242424"),
    ("#161628",                      "#242424"),

    # Grid / card borders
    ("#2a2a3a",                      "#282828"),

    # Text colours
    ("#e0e0f0",                      "#ffffff"),
    ("#c0c0d8",                      "#e0e0e0"),
    ("#9999cc",                      "#b3b3b3"),
    ("#9999bb",                      "#b3b3b3"),
    ("#7777a0",                      "#b3b3b3"),
    ("#55557a",                      "#727272"),
    ("#44445a",                      "#727272"),
    ("#33334a",                      "#535353"),
    ("#5a5a80",                      "#727272"),
    ("#6666aa",                      "#b3b3b3"),

    # Gradient heading  green→purple → green→spotify-blue
    ("gradient(135deg,#1DB954 0%,#7b61ff 45%,#1DB954 100%)",
     "gradient(135deg,#1DB954 0%,#509BF5 45%,#1DB954 100%)"),

    # Glow pulse keyframe  rgba(0,229,160  already handled above
    # But the explicit hex in keyframe
    ("0 4px 0 0 #00e5a0",            "0 4px 0 0 #1DB954"),
]

FILES = [
    "app.py",
    "utils/theme.py",
    "pages/1_Executive_Overview.py",
    "pages/2_Hit_Predictor.py",
    "pages/3_Revenue_Intelligence.py",
    "pages/4_Emerging_Artists_Radar.py",
    "pages/5_Playlist_Curator.py",
]

def recolor(content: str) -> str:
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    return content


def process(rel_path: str) -> None:
    path = os.path.join(BASE, rel_path)
    with open(path, "r", encoding="utf-8") as fh:
        original = fh.read()
    updated = recolor(original)
    if updated == original:
        print(f"  (no changes)  {rel_path}")
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(updated)
    changes = sum(1 for (o, _) in REPLACEMENTS if o in original)
    print(f"  ✓  {rel_path}  ({changes} substitution types applied)")


# ── update .streamlit/config.toml ────────────────────────────────────────────
TOML_PATH = os.path.join(BASE, ".streamlit", "config.toml")
TOML_NEW = """[theme]
base                     = "dark"
primaryColor             = "#1DB954"
backgroundColor          = "#121212"
secondaryBackgroundColor = "#181818"
textColor                = "#ffffff"
font                     = "sans serif"
"""

if __name__ == "__main__":
    print("Recoloring to Spotify brand palette …\n")
    for f in FILES:
        process(f)

    with open(TOML_PATH, "w", encoding="utf-8") as fh:
        fh.write(TOML_NEW)
    print(f"  ✓  .streamlit/config.toml  (Spotify palette applied)")

    print("\nDone. Restart streamlit to see changes.")
