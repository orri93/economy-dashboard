# Bond Market Status

- Generated at: 2026-05-22T17:10:29.436565+00:00
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

## Signal Evaluation
- **Inverted yield curve**: not present -> Higher recession risk
- **Falling long-term yields during stress**: not obvious -> Growth fear or flight to safety
- **Rising long-term yields**: elevated -> Inflation concern, fiscal concern, or stronger growth expectations
- **Widening credit spreads**: contained -> Rising corporate stress
- **Rising real yields**: elevated -> Valuation pressure on stocks
- **Treasury liquidity stress**: not obvious -> Broader financial-system stress

## OpenAI Assessment
### Executive Summary
Current US bond-market readings (data through 2026-05-20/21) show no inversion in the 2y–10y sector (10y–2y = +0.49 pp), materially positive nominal and real long yields (10y = 4.57%, 30y = 5.11%, 10y real = 2.13%), and contained credit spreads (BofA HY = 2.78% / BAA = 1.59%). Financial-stress and financial-conditions indexes are negative (STLFSI = −0.7404, NFCI = −0.523) and VIX is moderate (16.76). Net: bond-market signals point away from immediate recession alarm and flight-to-safety, but elevated long nominal and real yields create potential valuation pressure and imply market concern about rates/inflation/fiscal or stronger growth expectations.

### Signal-by-Signal Assessment
1. Inverted yield curve -> Higher recession risk  
   - Status: not present.  
   - Evidence: 10y–2y = +0.49 (2026-05-21), 2y = 4.04% (2026-05-20), 10y = 4.57% (2026-05-20).  
   - Confidence: high for the 2y–10y measure.  
   - Caveats: inversion can appear in other tenor pairs (e.g., 3m–10y) not provided here.

2. Falling long-term yields during stress -> Growth fear or flight to safety  
   - Status: not obvious.  
   - Evidence: long yields are elevated (10y 4.57%, 30y 5.11%) while stress gauges are subdued (STLFSI −0.7404, NFCI −0.523, VIX 16.76). No sign of a flight-to-safety drop in long yields in this snapshot.  
   - Confidence: moderate–high.  
   - Caveats: we lack intraday/short-run moves and TIPS/breakeven dynamics that could show transient safe-haven flows.

3. Rising long-term yields -> Inflation concern, fiscal concern, or stronger growth expectations  
   - Status: elevated.  
   - Evidence: 10y = 4.57% and 30y = 5.11% (2026-05-20). These levels are materially positive and, together with a positive term structure, are consistent with upward pressure on long rates.  
   - Confidence: medium.  
   - Caveats: attribution among inflation expectations, term premium, fiscal supply, or growth is not resolvable from the provided series (breakevens and term-premium decompositions are missing).

4. Widening credit spreads -> Rising corporate stress  
   - Status: contained.  
   - Evidence: HY spread = 2.78% (2026-05-21), BAA = 1.59% (2026-05-20). Spreads are not accompanied by elevated STLFSI/NFCI, suggesting limited systemic corporate stress in this snapshot.  
   - Confidence: moderate.  
   - Caveats: a single-level reading cannot detect recent widening episodes or issuer-specific distress; time-series and broader credit-market liquidity metrics are needed.

5. Rising real yields -> Valuation pressure on stocks  
   - Status: elevated.  
   - Evidence: 10y real yield = 2.13% (2026-05-20). Real yields at this level increase discount rates and add valuation pressure for long-duration assets (equities, growth stocks).  
   - Confidence: medium.  
   - Caveats: we do not have a trend series here to confirm recent rise; equity-market sensitivity also depends on earnings growth and risk premia.

6. Treasury liquidity stress -> Broader financial-system stress  
   - Status: not obvious.  
   - Evidence: STLFSI = −0.7404 (2026-05-15) and NFCI = −0.523 (2026-05-15) indicate below-average systemic stress; VIX = 16.76 (2026-05-21) is moderate.  
   - Confidence: moderate–high for absence of broad liquidity stress.  
   - Caveats: measures of dealer balance sheets, repo rates, bid-ask spreads, and on-the-run/off-the-run dislocation metrics are not provided.

### Cross-Asset Implications
- Equities: Elevated real yields (2.13%) and high nominal long yields imply upward pressure on discount rates — negative for long-duration/tech/growth names; contained credit spreads and low stress indexes reduce immediate default tail risk for corporates.  
- Credit: Spreads near current levels (HY 2.78%, BAA 1.59%) are not signaling systemic stress now, but rising long yields can raise refinancing costs and weigh on lower-rated issuers if spreads widen.  
- FX / Rates positioning: Higher US nominal yields relative to other economies (not shown) tend to support USD and could attract carry/duration repositioning; monitor front-end policy path versus longer-term yields for curve trades.  
- Volatility/liquidity: VIX ~16.8 and negative STLFSI/NFCI point to orderly conditions; however, rising real yields could increase equity volatility if growth expectations or inflation signals change.

### Risk Flags To Monitor Next
- 10y–2y spread: watch for move from +0.49 toward zero or negative (current = +0.49 on 2026-05-21).  
- Real yields / TIPS breakevens: need breakeven inflation and term-premium decomposition (not provided). Rising real yields above ~2.5% would further stress equity valuations.  
- Credit spreads: HY > ~4.0% or BAA > ~2.5% would be a noticeable deterioration from current HY 2.78% / BAA 1.59%.  
- Financial-stress / liquidity metrics: a rise in STLFSI from −0.7404 or NFCI from −0.523 toward zero and positive territory, repo stress, or widening bid-ask spreads.  
- Volatility: VIX spikes above 25 would signal a move from moderate to stressed sentiment (current VIX = 16.76).  
- Policy and supply signals: Fed funds path, short rates, and fiscal issuance updates (not included here) — these can push long yields independently of macro growth.

### Confidence And Data Caveats
- Data vintage: yields dated 2026-05-20 and 10y–2y and HY dated 2026-05-21; STLFSI and NFCI are dated 2026-05-15. Snapshot was fetched 2026-05-22. Conclusions apply to this snapshot and may not reflect intraday moves or subsequent developments.  
- Missing items that limit attribution: breakeven inflation, term-premium decompositions, Treasury on-the-run vs off-the-run liquidity metrics, short-end (3m) to long-end spreads, dealer balance-sheet and repo rates. These are needed to separate inflation vs term-premium vs fiscal drivers and to detect transient liquidity stress.  
- No errors reported in payload. Where trend/causation is asserted, I explicitly flag uncertainty — the data support level-based assessments but do not uniquely identify underlying drivers.
