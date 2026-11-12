#!/usr/bin/env python3
import json
import re
import subprocess

html = subprocess.run(["curl", "-sfL", "https://www.nytimes.com/puzzles/spelling-bee"],
                      capture_output=True, text=True, check=True).stdout
start = re.search(r"window\.gameData\s*=\s*", html).end()
today = json.JSONDecoder().raw_decode(html[start:])[0]["today"]
puzzle = {"date": today["printDate"], "centerLetter": today["centerLetter"],
          "outerLetters": today["outerLetters"], "answers": today["answers"],
          "pangrams": today["pangrams"]}

with open("index.html") as f:
    page = f.read()
data = json.dumps(puzzle).replace("<", "\\u003c")
page = re.sub(r'(<script type="application/json" id="puzzle-data">).*?(</script>)',
              lambda m: m[1] + data + m[2], page, count=1, flags=re.DOTALL)
with open("index.html", "w") as f:
    f.write(page)
print(puzzle["date"], puzzle["centerLetter"].upper(), "".join(puzzle["outerLetters"]).upper())
