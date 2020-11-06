# Omnia Portfolio

Omnia Portfolio gives the optimal diversed portfolio given
a investors preference and risk averse.

Given a data of monthly returns for N assets, Omnia Portfolio will search for
the optimal portfolio of n <= N assets.

## Description

### Portfolio constraints

Investor can provide a set of constraints how the portfolio should be
structured:

- Percentages of certain categories that should make up the portfolio i.e.

  - at least 15% green eco-friendly assets
  - at least 10% real estate
  - etc.

- Level of risk

- Expected return

### Search Method

The method uses iterative deepening branch and bound search method.
Each combinations of assets score is calculated giving an upper bound
to prune combinations.

### Score calculation

< To Be Described >

## Usage

< To Be Described >
