# Development Notes — feature/expanded-content

This document summarises the project, the build setup, and all changes made on the `feature/expanded-content` branch.

---

## What this project is

A community completion of **Airline Tycoon Deluxe**, a late-1990s airline management sim by Spellbound Software. BFG released partial source code as a bonus with the GOG edition; this repo fills in the missing pieces to make it fully buildable and playable.

The original game engine is C++ (VC6-era style). The community port replaced DirectDraw/DirectSound/DirectPlay with **SDL2**, added 64-bit support, cross-platform build (CMake), and reimplemented multiplayer over **ENet/RakNet**.

Assets (sprites, audio, data CSVs) are **not** included — you need a GOG copy of Airline Tycoon Deluxe (or First Class / Evolution).

---

## Build setup (VS2026 / x64)

The branch was migrated from VS2019/CMake to **Visual Studio 2026 Community** with a native `.sln`/`.vcxproj` build.

**Quick build:**
- **laptop:** `powershell -Command "& 'C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe' 'AirlineTycoon.sln' /p:Configuration=Release /p:Platform=x64 /m /v:minimal"`
- **pc:** `powershell -Command "& 'C:\Program Files\Microsoft Visual Studio\18\Insiders\MSBuild\Current\Bin\MSBuild.exe' 'AirlineTycoon.sln' /p:Configuration=Release /p:Platform=x64 /m /v:minimal"`

**Machine passkey:** `laptop` = `C:\Games\Airline Tycoon Deluxe\` — `pc` = `D:\Games\Steam\steamapps\common\Airline Tycoon Deluxe\`

The post-build event automatically copies `AT.exe` to the game folder:
- **laptop:** `C:\Games\Airline Tycoon Deluxe\At.exe`
- **pc:** `D:\Games\Steam\steamapps\common\Airline Tycoon Deluxe\At.exe`

**What was fixed to get it building:**
- All `.vcxproj` toolsets updated: v142 → v145, SDK 10.0.19041.0 → 10.0.26100.0
- SDL2 2.32 / SDL2_ttf 2.24 / SDL2_image 2.8 / SDL2_mixer 2.8 added under `cmake/`
- `enet` submodule cloned from github.com/lsalzman/enet and given its own `.vcxproj`
- C++17 added to TeakLibW Release config
- Post-build `xcopy` replaced with `copy /Y`
- SDL fullscreen scaling fixed: removed premature `SDL_GetWindowSurface()` call, added `SDL_RenderSetLogicalSize(640, 480)` so the 640×480 game content scales to any resolution

**Debugger config** (`AT.vcxproj.user`): debugger command points at the game folder (see passkey above) so F5 launches from the game folder where the assets live.

---

## Version string

The main menu (bottom-right, `NewgamePopup.cpp`) shows the current git commit hash at build time:

- Release: `v1.4-<hash>`
- Debug:   `v1.4-DEBUG-<hash>`

A pre-build event in `AT.vcxproj` runs `git rev-parse --short HEAD` and writes `src/git_version.h` (gitignored). The version string is assembled at compile time via C string literal concatenation — zero runtime overhead.

---

## Content expansion

### Cities & routes
- `MAX_CITIES` raised 256 → 320
- `MAX_ROUTES` raised 736 → 1500
- Custom cities added to `data/city.csv` covering additional real-world destinations
- Modding tools added (`tools/`): `xtrle_decode.py` decodes xtRLE-encoded CSVs; `gli_extract.py` extracts GLIB2 sprite libraries to PNG

### Planes
- `MAX_PLANETYPES` raised 80 → 200
- 80 real-world airliners added to `data/planetyp.csv` (turboprops through wide-bodies, 1940s–1990s)
- Museum plane pool extended to include types built up to 1999 (was 1996)

### Staff & names
- Worker pool limit raised; 175 new workers added
- Plane name lists expanded; 760 names added across `pnames1.csv` / `pnames2.csv`

### Economy scaling
- Starting capital and AI thresholds scaled ×5 to match the expanded route/city count
- Debt cap: −1M → −20M DM; game-over threshold: −5M → −100M DM

### Airport expansion
- `MAX_AIRPORT_LEVEL` constant added (value: 69); cheat code expansion cap raised to match

---

## Bug fixes

### Crashes
| Commit | Fix |
|--------|-----|
| `0da1d08` | `SetPixel` access violation when hovering freight orders — added `x/y` bounds guard in `CBitmap.cpp` |
| `e2fc036` | `NetRefill` missing `case 5` for foreign freight — `Delta` left uninitialised, corrupted `AuslandsFRefill` |
| `cdeb3e9` | Crash opening globe after buying museum plane |
| `e2b72f8` | `Rand(0)` crash in `CreateRandomUsedPlane` when A319 (Erstbaujahr=1996) appeared in museum |

### Route map hitbox (RouteBox.cpp)
- Hit radius reduced 10 px → 5 px (10 px was unworkable with 1500 routes on a 415×240 px map)
- Zero-length segments (e.g. Kinshasa/Brazzaville sharing near-identical screen coords) skipped with `if (p1==p2) continue` to prevent division-by-~zero returning distance 0 for all mouse positions

### Diplomacy death spiral (Sim.cpp)
Seven changes (O1–O7) to `UpdateKooperation()`:
- Envy decay trigger moved from Sympathy < 25 → < 0 (50-point buffer before spiral starts)
- Decay rates halved
- Passive recovery +1/day capped at +30
- Alliance bonus +1/day capped at +70
- Severe envy now also requires 2× wealth ratio (prevents cascade past −50)

---

## AI improvements

### Competency fixes (Player.cpp / Editor.cpp)
| ID | Fix |
|----|-----|
| A | Advertising skips routes with >5 consecutive loss days |
| B | Share emission requires positive yesterday balance; buyback guards against insolvency |
| C | Flight departures staggered by existing planes-on-route × 6 hours |
| D | Station buy threshold reduced 10× → 3× daily balance |
| E | Low-occupancy rescue skips chronically losing routes |
| F | Gate trigger replaced dead stub with real gate=−1 flight scan |
| G | AI uses aircraft designer in Free Game — three configs (43-seat/3400 km, 53-seat/8100 km, 81-seat/12500 km) |
| H | Retire planes with condition < 25, sell at 90% market value |
| I | Museum visit also triggered when any plane has condition < 40 |
| J | Designer visit triggered as fallback when money > 20M (1-in-3 chance) |
| K | Target condition raised to min 70 for all planes each planning cycle |
| L | Yield pricing: +15% on full routes, −10% (with cost floor) on near-empty routes |
| M | Broker visit upgrades the worst-scoring plane in order (seats → meals → deco → engines → tires → electronics → safety) |
| N | Route advertising scores by demand × 3 if human competes on that route |

### Rubber-band reduction
Nightly AI bonus pool tiers cut from 100K/200K/400K/800K → 33K/33K/33K/33K (max ~99K/night, down from 2.4M). Difficulty multipliers removed.

### AI salary costs (Player.cpp)
`BookSalary()` previously had an `if (Owner==0)` guard — AI never paid staff. Added `else if (Owner==1)` branch that calculates simulated salary from fleet size (pilots + stewards per plane, using `OriginalGehalt` from global worker pool, deducted at (total + 25% overhead) / 30 per day).

### Route/order hybrid mode
- Route adoption threshold lowered: day 30+ / 7 planes → day 15+ / 4 planes
- Day-25 fallback added so AI no longer waits for human to rent routes first
- In route mode, one order-check slot still runs each morning (alternating daily)
- Net result: orders:routes ratio improved from ≈9:1 to ≈4:7

---

## Museum randomisation (Sim.cpp)
Previously fully deterministic (seed = date + index). Replaced with:
- Age-weighted plane type selection (bell curve: 1980s most common, 1990s less common, pre-1960 rare)
- Per-day pool built from eligible types; deduplication so no type appears twice in the same day's three slots
- Seed uses `StartTime + Date×31 + Index` for per-save variation
- Mid-day refill also deduplicates against already-occupied slots

---

## Morning briefing cards
Stats shown on competitor briefing cards changed from (image%, personnel%, plane condition%) to:
1. Passengers — mission progress / rating
2. Cargo — all-time tonnes
3. Flights — all-time count
4. Image %
5. Personnel satisfaction %

---

## Known remaining issues
- `city.csv` contains some custom cities with extreme map coordinates (far west/south) that produce out-of-bounds line draws in `DrawFrachtTipContents`. The `SetPixel` bounds guard (`0da1d08`) silently clips these — no crash, but the route line on the freight order tip may be partially invisible for affected cities.
