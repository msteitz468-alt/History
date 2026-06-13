# Ingestion Campaign — `raw/` Root Queue

Standing order (set 2026-06-12): **process in phase order, targeted depth on reference sets / full on
monographs & primaries, commit-per-cycle + push-per-source, don't check in** except for a genuine fork
(scope decision, corrupt/foreign-language file, or a contradiction needing adjudication). Checkpoints to
git + memory after every source, so the campaign is fully resumable across sessions.

Status key: `[ ]` pending · `[~]` in progress · `[x]` done · `[skip]` unusable/deprioritized

## Not ingestable (verified 2026-06-12)
- [skip] **Cambridge History of China (11-vol set)** — body is in **Chinese** (translated ed.), not English. Cover China via Keay + Spence.
- [skip] **Cambridge History of Ancient China** — 407-line "OCR Test Pages 1–10" stub; broken.
- [skip] **Die Song-Dynasty (Kuhn)** — German + garbled/mirrored OCR.
- [skip] **Guamán Poma, Nueva corónica Tomo I** — Spanish, garbled OCR, partial; conquest-primary need met by Broken Spears + Bernal Díaz.
- [verify] **CAH Vol. 4 / Vol. 3 Pt 2 / Vol. 3 Pt 3 / Vol. 2 Pt 2** — open as "CONTENTS…" stubs (2–4k lines); likely front-matter only. Check before ingest.
- [skip] **PDF Listing.md** — index, not a source.

## Phase A — Finish the Americas (in flight)
- [ ] Berdan, *The Aztecs* (Reaktion, 2021) — full single-pass
- [ ] *The Broken Spears* (Aztec conquest account) — primary, single-pass
- [ ] Bernal Díaz, *The Conquest of New Spain* — primary, single-pass
- [ ] *Popol Vuh* (Tedlock) — Maya primary, single-pass/2 cycles
- [ ] Burkholder & Johnson, *Colonial Latin America* — 3–4 cycles
- [ ] Galeano, *Open Veins of Latin America* — single-pass

## Phase B — Japan (open gap)
- [ ] Mason & Caiger, *A History of Japan* — single-pass spine
- [ ] Sansom, *Japan: A Short Cultural History* — ~3 cycles
- [ ] *The Tale of Genji* (Waley) — primary, single-pass
- [ ] Cambridge History of Japan Vol. 1 (Hall) — targeted
- [ ] CHJ Vol. 3 (Medieval) — targeted
- [ ] CHJ Vol. 4 (Early Modern) — targeted
- [ ] CHJ Vol. 5 (19th c.) — targeted
- [ ] CHJ Vol. 6 (20th c.) — targeted
- [ ] *Early Modern Japan in Asia and the World* (New CHJ 2) — targeted

## Phase C — Ottoman / post-1500 Islamic world (open gap)
- [ ] Imber, *The Ottoman Empire 1300–1650* — single-pass (structural)
- [ ] Finkel, *Osman's Dream* — 2 cycles (narrative spine)
- [ ] Mikhail, *God's Shadow* (Selim I) — single-pass
- [ ] Kinross, *The Ottoman Centuries* — targeted/3–4 cycles
- [ ] Rogan, *The Arabs: A History* — single-pass

## Phase D — China depth (moderate gap)
- [ ] Keay, *China: A History* — single-pass spine
- [ ] Spence, *The Search for Modern China* — 2 cycles
- [ ] Sima Qian, *Records of the Grand Historian* — Qin — primary, single-pass
- [ ] Sima Qian, *Records of the Grand Historian* — Han II — primary, 2–3 cycles

## Phase E — India depth + Mongols (Gap 3 optional)
- [ ] May, *The Mongol Conquest in World History* — single-pass
- [ ] *Baburnama* — primary, single-pass
- [ ] *The Arthashastra* (Kautilya) — primary, 2 cycles
- [ ] Dalrymple, *The Last Mughal* — 2–3 cycles
- [ ] Cambridge History of India Vol. 3 — targeted (massive)
- [ ] Cambridge History of India Vol. 4 (Burn) — targeted (massive)
- [ ] Cambridge History of India Vol. 5 (British India) — targeted (massive)

## Phase F — Backbone deepening: early-modern Europe + ancient (long tail)
- [ ] Oxford Handbook of Early Modern European History I — targeted
- [ ] Oxford Handbook of Early Modern European History II (Cultures & Power) — targeted
- [ ] New Cambridge Modern History Vol. 1 (Renaissance 1493–1520) — targeted
- [ ] NCMH Vol. 2 (Reformation 1520–59) — targeted
- [ ] NCMH Vol. 3 (Counter-Reformation 1559–1610) — targeted
- [ ] NCMH Vol. 4 (Decline of Spain & Thirty Years War) — targeted
- [ ] NCMH Vol. 5 (Ascendancy of France 1648–88) — targeted
- [ ] NCMH Vol. 6 (Rise of GB & Russia 1688–1715) — targeted
- [ ] NCMH Vol. 7 (Old Regime 1713–63) — targeted
- [ ] NCMH Vol. 8 (American & French Revolutions 1763–93) — targeted
- [ ] Cambridge Modern History Vol. 9 (Napoleon) — targeted
- [ ] NCMH Vol. 10 (Zenith of European Power 1830–70) — targeted
- [ ] NCMH Vol. 11 (Material Progress 1870–98) — targeted
- [ ] NCMH Vol. 12 (Shifting Balance 1898–1945) — targeted
- [ ] NCMH Vol. 13 (Companion Volume) — targeted
- [ ] CAH Vol. 3 Pt 1 (61k) — full large-volume; + any verified short CAH vols

## Phase G — Africa depth (Gap 2 complete; optional)
- [ ] Davidson, *The African Past* — sourcebook, 2–3 cycles

---

**Scale:** ~48 ingestable sources, ~20 of them multi-cycle large volumes → 120+ ingest-cycles; a
multi-week, multi-session campaign. Phases A–D are the high-value core (open gaps); Phase F is the long
tail (European/reference backbone). Progress tracked here and in the per-gap memory files.
