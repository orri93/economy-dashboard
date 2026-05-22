# Bond Market Status

- Generated at: 2026-05-22T18:49:17.378883+00:00
- Source: FRED

## Latest Indicators
- **yield_curve_10y_2y**: 0.49 (series `T10Y2Y`, date 2026-05-21)
- **yield_2y**: 4.04 (series `DGS2`, date 2026-05-20)
- **yield_10y**: 4.57 (series `DGS10`, date 2026-05-20)
- **yield_30y**: 5.11 (series `DGS30`, date 2026-05-20)
- **real_yield_10y**: 2.13 (series `DFII10`, date 2026-05-20)
- **high_yield_spread**: 2.78 (series `BAMLH0A0HYM2`, date 2026-05-21)
- **baa_10y_spread**: 1.59 (series `BAA10Y`, date 2026-05-20)
- **financial_stress_index**: -0.7404 (series `STLFSI4`, date 2026-05-15)
- **financial_conditions_index**: -0.523 (series `NFCI`, date 2026-05-15)
- **market_volatility_proxy**: 16.76 (series `VIXCLS`, date 2026-05-21)

## One-Year Trend Context (Daily Resolution)
- **yield_curve_10y_2y**: 30d change=-0.02, 1y change=None, 1y percentile=13.2, samples=250
- **yield_2y**: 30d change=0.25, 1y change=None, 1y percentile=98.8, samples=249
- **yield_10y**: 30d change=0.28, 1y change=None, 1y percentile=98.8, samples=249
- **yield_30y**: 30d change=0.22, 1y change=None, 1y percentile=98.8, samples=249
- **real_yield_10y**: 30d change=0.17, 1y change=None, 1y percentile=96.0, samples=249
- **high_yield_spread**: 30d change=-0.12, 1y change=-0.4, 1y percentile=14.0, samples=264
- **baa_10y_spread**: 30d change=-0.14, 1y change=None, 1y percentile=1.6, samples=248
- **financial_stress_index**: 30d change=-0.3718, 1y change=None, 1y percentile=19.2, samples=52
- **financial_conditions_index**: 30d change=-0.006, 1y change=None, 1y percentile=32.7, samples=52
- **market_volatility_proxy**: 30d change=-2.73, 1y change=-2.42, 1y percentile=40.3, samples=258

## Signal Evaluation
- **Inverted yield curve**: not present -> Higher recession risk
- **Falling long-term yields during stress**: not obvious -> Growth fear or flight to safety
- **Rising long-term yields**: elevated -> Inflation concern, fiscal concern, or stronger growth expectations
- **Widening credit spreads**: contained -> Rising corporate stress
- **Rising real yields**: elevated -> Valuation pressure on stocks
- **Treasury liquidity stress**: not obvious -> Broader financial-system stress

## OpenAI Assessment
### Executive Summary
- Snapshot time: 2026-05-22T18:49:17Z (payload generated). Key read: the U.S. yield curve (10y–2y) remains positively sloped (0.49), while nominal and real long-term yields have risen over the past 30 days and sit near the top of the past-year distribution. Credit spreads are tight and trending slightly tighter. Financial-stress and volatility metrics show no acute market-wide liquidity stress. Net read: rates-driven tightening and elevated real yields are the dominant bond-market signal; recession-signals from inversion or widening credit stress are not present in the payload.  

### Signal-by-Signal Assessment
For each signal below I give the current status, the explicit evidence from the payload (including 30‑day change and 1‑year percentile where available), a confidence level, and key caveats.

1) Inverted yield curve -> Higher recession risk  
- Status: Not present.  
- Evidence: 10y–2y = +0.49 (value dated 2026-05-21). Trend: 30d change = −0.02; 1y percentile = 13.2 (sample_size 250).  
- Confidence: High — spread is positive and materially above zero.  
- Caveats: 1‑year change is null in trend_context; the 10y–2y has flattened slightly over 30 days (−0.02) so inversion remains a risk to watch.

2) Falling long-term yields during stress -> Growth fear / flight to safety  
- Status: Not obvious / not occurring.  
- Evidence: 10y current = 4.57 (2026-05-20) with 30d change = +0.28; financial-stress index current = −0.7404 (2026-05-15), 30d change = −0.3718, 1y percentile = 19.2. VIX = 16.76 (2026-05-21), 30d change = −2.73, 1y percentile = 40.3.  
- Confidence: Medium — long yields have been rising (not falling) while stress/volatility metrics are lowish.  
- Caveats: Stress index and NFCI sample_size are small (52) and the most recent stress index point is 2026-05-15 (not 5/21).

3) Rising long-term yields -> Inflation/fiscal/growth concern (or term‑premium move)  
- Status: Elevated.  
- Evidence: 10y = 4.57 (2026-05-20); 10y 30d change = +0.28; 10y 1y percentile = 98.8 (sample_size 249) — i.e., 10y near the high end of the past year. 30y = 5.11, 30d change = +0.22, 30y 1y percentile = 98.8. 2y = 4.04, 30d change = +0.25, 2y percentile = 98.8.  
- Confidence: High — consistent, broad-based rise in short and long yields and very high percentiles versus the last year.  
- Caveats: The payload does not provide direct decomposition (inflation expectation vs. term premium vs. fiscal risk). 1‑year *change* fields are null for some series.

4) Widening credit spreads -> Rising corporate stress  
- Status: Contained / compressing.  
- Evidence: High-yield spread = 2.78 (2026-05-21), 30d change = −0.12, 1y change = −0.40, 1y percentile = 14.0 (sample_size 264). BAA 10y spread = 1.59 (2026-05-20), 30d change = −0.14, 1y percentile = 1.6.  
- Confidence: Medium‑high — both HY and BAA spreads are tighter vs. recent history and moving modestly lower over 30 days.  
- Caveats: Spreads remain a lagging indicator; low percentiles can shift quickly with a stress event.

5) Rising real yields -> Valuation pressure on stocks  
- Status: Elevated.  
- Evidence: Real 10y = 2.13 (2026-05-20), 30d change = +0.17, 1y percentile = 96.0 (sample_size 249).  
- Confidence: High for the mechanical implication (higher real yields increase discount rates).  
- Caveats: The payload does not include equity valuations or returns; the economic driver (higher real growth expectations vs. higher term premium) is not identified here.

6) Treasury liquidity stress -> Broader financial‑system stress  
- Status: Not obvious / absent in the available metrics.  
- Evidence: Financial-stress index (STLFSI4) = −0.7404 (2026-05-15), 30d change = −0.3718, 1y percentile = 19.2 (lower end). NFCI = −0.523 (2026-05-15), 30d change = −0.006, 1y percentile = 32.7. VIX percentile = 40.3. High-yield and BAA spreads are compressed.  
- Confidence: Medium — the included stress indicators and credit spreads show no acute liquidity stress.  
- Caveats: Treasury-liquidity stress can show up in dealer balance-sheet metrics, repo volumes, specialness, or on-the-run/ off-the-run dislocations that are not present in this payload. STLFSI and NFCI sample_size = 52 (weekly) so updates are less frequent.

### Cross-Asset Implications
- Equities: Elevated real yields (real 10y = 2.13; 1y percentile 96.0) imply higher discount rates and therefore greater valuation sensitivity for long-duration equity sectors; but compressed credit spreads (HY 1y percentile 14.0) and subdued VIX (16.76, 30d down) suggest risk appetite remains intact in credit and equity risk premia. Net: valuation pressure is rising, but risk‑taking is still present.  
- Credit: Credit spreads are tighter (HY = 2.78, 30d −0.12; BAA 1.59, 30d −0.14) — corporate funding stress not currently visible in spreads. Rising nominal yields may increase refinancing costs, however, which is a structural headwind for levered borrowers.  
- Macro / Policy: Broad-based, recent increases in both 2y and 10y yields (2y = 4.04, 30d +0.25; 10y = 4.57, 30d +0.28) place upward pressure on borrowing costs across the economy. The positive 10y–2y (~0.49) implies the curve is not signalling immediate recession risk from inversion, but the upward shift in yields could tighten financial conditions (NFCI = −0.523, percentile 32.7) over time.  
- Volatility / Liquidity: VIX and stress indices are not signaling acute dislocation (VIX 16.76, VIX 1y pct 40.3; STLFSI4 near −0.74, low percentile). That lowers the likelihood that recent yield moves are solely flight‑to‑safety episodes.

### Risk Flags To Monitor Next
- 10y–2y spread: watch for a move from +0.49 toward zero and through to inversion (payload 30d flattening = −0.02). An inversion would materially change the recession-risk assessment.  
- Real 10y: further increases above current 2.13 (30d +0.17) — sustained rises would increase valuation pressure on equities and raise the real cost of capital.  
- Credit spreads: a turn higher from current compressed levels (HY 2.78; BAA 1.59) — especially a rapid increase >~1.0 percentage point from here would indicate rising corporate stress. (Payload evidence: HY 1y change = −0.40, indicating recent easing.)  
- Financial-stress / liquidity indicators: spikes in STLFSI, NFCI, or rapid jump in VIX would signal system stress (current STLFSI percentile 19.2; VIX percentile 40.3). Also monitor Treasury‑specific liquidity metrics not included here (repo specialness, dealer inventories, ON‑RRP flows).  
- Decomposition signals: if 10y rises but breakevens fall (not in payload), that would point to higher term premium/fiscal risk rather than inflation expectations — need additional series (TIPS breakeven) to separate drivers.

### Confidence And Data Caveats
- Source & timestamp: all conclusions are drawn solely from the provided payload (generated_at 2026-05-22T18:49:17.378883+00:00; snapshot.fetched_at 2026-05-22T18:49:17.377955+00:00).  
- Trend metrics: I used trend_context fields explicitly (current, change_30d, change_1y when present, percentile_1y). Where change_1y = null I have noted that the one‑year *change* is missing. Percentiles used: 10y/2y/30y/2y percentiles = 98.8; real 10y pct = 96.0; HY pct = 14.0; T10Y2Y pct = 13.2. Sample-size values are shown in trend_context (e.g., sample_size 249/250 for yields, 264 for HY, 52 for stress indices).  
- Date-staleness: some series (STLFSI4, NFCI) are weekly and the latest point in values is dated 2026-05-15; VIX and spreads have later dates (5/20–5/21). This creates slight timing mismatches when comparing very short‑run moves.  
- Missing decomposition: the payload does not include breakeven inflation (TIPS breakeven), dealer repo/specialness, FX or Treasury market microstructure metrics — so attribution (inflation vs term premium vs fiscal risk vs technical supply) cannot be resolved here.  
- No external data used: all statements above are strictly grounded in the payload; external headlines or macro events are not incorporated. If you want attribution (term‑premium vs. inflation expectations) or live liquidity indicators, additional series (TIPS breakevens, dealer positions, repo rates, on‑the‑run/off‑the‑run spreads) should be fetched.
