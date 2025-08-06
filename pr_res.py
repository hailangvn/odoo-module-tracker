import re


pr_res = [
    re.compile(
        r"[Mm]igrat(ed|ion)\s+(module\s+)?([^:.,*\(]+)\s+to\s"
    ),
    re.compile(
        r"\[([0-9.]*)*\]\s*\[(ADD|MIG|mig)\]\s*[-:]\s*([a-z0-9_]+)"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[ADD\]\s*([Aa]dd\s+)+([^:.,*\(]+)\s[Mm]odule"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[ADD\]\s*\s:*\s*([Aa]dd\s+)+([Mm]odule\s+)*([^:.,*\(]+)"
    ),
    re.compile(
        r"\[([0-9.]*)*\]\s*\[(ADD|MIG|mig)\]\s*([a-z0-9_]+) [Mm]odule"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s*[Aa]dded (a\s+|migrated\s+)*([a-z0-9_]+) [Mm]odule"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s*([Aa]dd\s+)+([^:.,*\(]+)\s+[Mm]odule"
    ),
    re.compile(
        r"\[*ADD\]*\s*\[*[0-9.]*\]*\s+([Aa]dd\s+)([Mm]odule\s+)*([^:.,*\(]+)"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[ADD\]\s*([Mm]odule\s+)+([^:.,*\(]+)"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[*(ADD|MIG|mig)\]*\s*Migrate\s+([a-z0-9_]+)"
    ),
    re.compile(
        r"\[*(ADD|MIG|mig)\]*\s*:*\smigrated\s([^:.,*\(]+)\s+[Mm]odule"
    ),
    re.compile(
        r"\[ADD\]\s*:\s+([Aa]dd\s+)+([^:.,*\(]+)"
    ),
    re.compile(
        r"(ADD|MIG|mig)\s+([^:.,*\(]+)\s+[Mm]odule"
    ),
    re.compile(
        r"\[*(ADD|MIG|mig)\]*\s*([Aa]dd\s+|\[IMP\]\s*)+([^:.,*\(]+)"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[*(ADD|MIG|mig)(\+MIG)*(\+REF)*\]*(\[IMP\])?\s+(\[NEW\]\s*)?([^:.,*\(]+)"
    ),
    re.compile(
        r"\[*[0-9.]+\]*\s*\[*(ADD|MIG|mig)\]*\s*([a-z0-9_]+)"
    ),
    re.compile(
        r"\Backport of ([^:.,*\(]+) to "
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s*\[([0-9.]*)*\]\s*([a-z0-9_]+)"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s*\[*([0-9.]+)\]*\s*:*\s*([^:.,*\(]+)"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\[([^:.,*\(\]]+)\]"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s+([^:.,*\(]+)"
    ),
    re.compile(
        r"\[*([0-9.]*)*\]*\s*\[*(ADD|MIG|mig)\]*(\s*\[[^]]*\])*\s*"
        r" [Mm]igration( of)*\s+([a-z0-9_]+)"
    ),
    re.compile(
        r"\[(ADD|MIG|mig)\]\s*([0-9.]*)-(add|mig)-([a-z0-9_\-]+)"
    ),
    re.compile(
        r"\[([0-9.]*)*\]\s*\[(BPRT)\]\s*([^:]+)"
    ),
]

catchall_res = [
    re.compile(
        r"\[*([0-9.]*)*\]*\s*\[*(ADD|MIG|mig)(\+IMP)*\]*(\s*\[[^]]*\])*\s*"
        r"([Nn]ew\s*)*(module\s*)*([^:*.,\(\[>\-/&…]+) [Mm]igration"
    ),
    re.compile(
        r"\[*([0-9.]*)*\]*\s*\[*(ADD|MIG|mig)(\+IMP)*\]*(\s*\[[^]]*\])*\s*"
        r"([Nn]ew\s*)*(module\s*)*([^:*.,\(\[>\-/&…]+)"
    ),
]
