# The World Today — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tidy-marten-51/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tidy-marten-51/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page summing up the world's news of Saturday
21 November 2026, drawn programmatically with Python 3 and PIL —
no photos, no network, no external assets. Every illustration is
original flat art drawn in code: a city skyline under attack, a
Danish flag at night, three summit flags, a courtroom, a hospital,
a globe and a protest crowd.

**Lead story:** Russia's retaliation strikes on Ukraine — a strike
on Kryvyi Rih kills 2 and injures 42 including 4 children, Kyiv's
bridges are hit with at least 9 dead, and a Russian missile crashes
in Poland, which Warsaw calls a provocation.

**Also on the page:** Denmark accuses Russian intelligence of
plotting to kill an American Ukrainian on Danish soil; Trump floats
his chief of staff for 2028 after the Shenzhen summit with Xi and
Putin; a US court sentences Nikhil Gupta to 19½ years in the
Pannun murder-for-hire plot; Bolsonaro hospitalised; COP31 crunch
time with no deal in sight; Europe's cost-of-living protests join
forces; plus briefs on Bangladesh arson attacks, the ICJ Myanmar
ruling fallout, and a researcher saying Claude proved the Riemann
Hypothesis.

## Run

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: a deterministic 1024×1024 PNG under 1 MiB. Running it twice
produces byte-identical files.

## Files

- `main.py` — entrypoint: composes the page and writes `entry.png`
- `draw_frontpage.py` — text, rules and all illustration drawing
- `entry.png` — the rendered front page (produced by running `main.py`)

## License

MIT — see `LICENSE`.
