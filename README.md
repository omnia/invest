# Omnia Invest

Omnia Invest gives the optimal diversed portfolio given
a investors criteria and risk averse factor.

Given a data of daily returns for N assets, Omnia Invest will search for
the optimal portfolio of n <= N assets.

## Description

### Investor's criteria

Investor can provide a set of constraints how the portfolio should be
structured:

- Percentages of certain categories that should make up the portfolio i.e.

  - at least 15% green eco-friendly assets
  - at least 10% real estate
  - etc.

- Level of risk

- Expected return

### Search Method

The method uses iterative deepening depth first branch and bound search method.
Each combinations of assets score is calculated giving an upper bound to prune combinations.

### Data source

CSV files for N Icelandic stocks from http://www.nasdaqomxnordic.com/shares/historicalprices

### Score calculation

< To Be Described >

## Usage

< To Be Described >
