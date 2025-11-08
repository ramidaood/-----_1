# build_stoplist.py
# No external deps needed (pure Python stdlib)

import pathlib, re, collections

DOCS = pathlib.Path("docs")
OUT = pathlib.Path("stoplist_top50.txt")

TOKEN_SPLIT = re.compile(r"[^A-Za-z]+")

def build_stoplist_top50():
    counter = collections.Counter()

    files = sorted(DOCS.glob("*.txt"))
    if not files:
        raise SystemExit("No files found in ./docs. Run fetch_wiki_docs.py first.")

    for p in files:
        txt = p.read_text(encoding="utf-8").lower()
        # drop header line "# TITLE: ..."
        txt = re.sub(r"^# title: .*?\n\n", "", txt, flags=re.IGNORECASE)
        tokens = [t for t in TOKEN_SPLIT.split(txt) if t and (len(t) > 1 or t in ("a", "i"))]
        counter.update(tokens)

    top50 = counter.most_common(50)

    # print
    print("\nTop 50 words across 10 pages:\n")
    for i, (w, c) in enumerate(top50, 1):
        print(f"{i:2d}. {w:15s} {c}")

    # save
    with OUT.open("w", encoding="utf-8") as f:
        f.write("Top 50 words (word\tcount)\n")
        for w, c in top50:
            f.write(f"{w}\t{c}\n")
    print(f"\nSaved: {OUT.resolve()}")

if __name__ == "__main__":
    build_stoplist_top50()