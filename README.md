# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Anggit98tkj/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Anggit98tkj/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A 1024x1024 front page that sums up Tuesday 24 November 2026 in one image. The program draws the page from scratch with Python and Pillow: masthead, date line, lead story, four story cards and a closing strip, with a small pictogram drawn in code for every story. No photos, no copied artwork, no network. Two runs write byte-identical output.

The six stories, all verified against reports in the 24 November 2026 news cycle:

1. Airstrike kills at least three Palestinians near Khan Younis, Gaza, Reuters
2. Asian shares rally as Huang's return to Nvidia revives the AI trade, Reuters
3. Japan factory activity expands, manufacturing PMI 53.7, Reuters
4. Iran claims its missiles can now reach Europe, range 4,500 km, Iran International
5. Chinese official sentenced to death for leaking state secrets, Reuters
6. Alleged drug lord El Chapo Isidro to be tried in Mexico, Reuters

## Run it

```sh
python3 generate_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`generate_image.py` writes `entry.png` (1024x1024, under 1 MiB). `main.ts` validates the PNG magic bytes and the 1 MiB limit, then copies it to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`.

Check determinism by running the generator twice and comparing hashes:

```sh
python3 generate_image.py && sha256sum entry.png
python3 generate_image.py && sha256sum entry.png
```

Both runs must print the same hash.

Dating note: the Gaza strike, the Japan PMI and the Asia rally are dated Tuesday 24 November 2026 in their reports. The Iran, China and Mexico stories were first reported on Monday 23 November and led Tuesday coverage, so they appear here as part of the Tuesday news cycle.

<sub>Entered on [make.fun](https://make.fun/?ref=e5tq5tyr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
