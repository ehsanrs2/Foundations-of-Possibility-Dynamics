# QuantConnect LEAN — integration decision

**Status (2026-10-26): documented conditional tool choice. No LEAN engine backtest executed or claimed.**

[QuantConnect LEAN](https://github.com/QuantConnect/Lean) is an event-driven trading strategy backtesting and live trading engine in C# and Python, distributed as Apache-2.0 open-source software. It is **not** the similarly named Lean mathematical proof assistant.

## Why LEAN can help

If initial theory and nonfinancial validation later succeed, LEAN can test a *financial-domain transfer* claim about fallback execution and hedging capabilities under market disruptions. It provides event processing, order/portfolio simulation, fee/slippage assumptions and historical data integration. It does NOT provide an independent oracle for dynamic constructive reachability or proof of mathematical novelty.

## Proposed future experiment — NOT YET IMPLEMENTED

E0: bounded execution policy with one channel. E1: optional backup route with activation time, finite budget and explicit costs. E2: halted instruments, liquidity disruptions, fees and correlated shocks. Outcomes should be prespecified functional targets such as whether a cash-raising action can be completed within a time/cost bound, not post-hoc trading profitability.

Use matched data, initial capital, tradable universe and observation information. Compare with standard redundancy, liquidity, diversification and expanded-state reachability, not only against a simplistic benchmark. Predeclare out-of-sample dates, survivorship handling, transaction costs and permissible data.

## Gate before actual engine execution

First pass the mathematical independent-oracle and synthetic P1 gates. Then secure permitted, versioned financial data and a reproducible LEAN Docker image/version, document order-fill/fee/slippage assumptions, and make a read-only backtest manifest. The officially supported LEAN CLI local backtest requires Docker, accessible data and a paid QuantConnect organization tier. Do not request credentials or make any live transactions as part of this study.

Decision: no LEAN runtime dependency in the core test suite; revisit this as a case-study simulator after scientific preregistration.

Sources: [Engine documentation](https://www.quantconnect.com/docs/v2/lean-engine/getting-started) and [LEAN backtest requirements](https://www.quantconnect.com/docs/v2/lean-cli/api-reference/lean-backtest).
