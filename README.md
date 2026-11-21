# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/lotyaid/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/lotyaid/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

**Saturday 21 November 2026 — 42 stories on one front page.** Consensus features: Russia's strike of 400 drones and 110 missiles on Ukraine, with missiles and a drone down in Poland (reported by 12 outlets); the AI stock rout that pushed the S&P 500 into correction; the World Court holding Myanmar responsible for genocide against the Rohingya; Hormuz tanker attacks as US–Iran talks stall; Houthi missiles aimed at Riyadh; and Trump defending his ties to Putin and Xi after the Shenzhen trilateral. Numbers strip: 400+ drones, 110 missiles, S&P 500 −3.7%, Nikkei −5.1%, gold −4.6%, Bitcoin $57,850, Brent $89.95, Sensex +2.3%. Plus the daraxonrasib pill that left pancreatic tumours undetectable in 1 in 12 trial patients, and 32 one-line briefs across world, society, science, space, economy, culture and sport — every story drawn from the day's One Turn edition (49 stories and 14 in brief, from 849 headlines). The entry program (main.ts, Node 22, standard library only) copies the image to /output/entry.png; compose.py rebuilds the image from the panel illustrations in assets/.

## What's on the page

- **Lead (illustrated):** the Ukraine–Poland strike, with its sources named (BBC News, PBS NewsHour, France 24).
- **Four illustrated features:** the AI rout, the genocide ruling, the cancer pill, the Shenzhen summit fallout.
- **Consensus band:** the five stories every outlet carried, each with the outlets that reported it.
- **Numbers strip:** eight hard figures from the day's reporting and markets.
- **32 briefs** in three ruled columns — no story invented, none padded.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Rebuild the page from its sources with `python3 compose.py` (deterministic: same inputs, same bytes).

---

<sub>Entered on [make.fun](https://make.fun/?ref=765w942g&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
