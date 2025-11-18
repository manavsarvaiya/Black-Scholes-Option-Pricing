# Black-Scholes Option Pricing and Implied Volatility Calculator

## Overview
This project implements a comprehensive financial calculator for option pricing and volatility analysis using the Black-Scholes model. The application features an interactive web interface built with Streamlit, enabling users to perform sophisticated financial calculations with ease.

## Features
- Option Pricing: Calculate theoretical prices for European call and put options

- Implied Volatility: Determine market-implied volatility from observed option prices

- Dual Option Support: Full functionality for both call and put options

- Interactive Interface: User-friendly web-based input system

- Real-time Computation: Instant calculation results with detailed outputs

## Installation
1) Download or clone the project files to your local machine

2) Install the required Python packages:

```
pip install streamlit numpy scipy
```
3) Launch the application using Streamlit:
```
streamlit run app.py
```
4) Access the application through your web browser at the provided local address

# Theoretical Foundation
## Black-Scholes Model
The Black-Scholes model represents a foundational framework in financial mathematics for valuing European options. Developed through pioneering work in quantitative finance, this model provides analytical solutions for option pricing under specific market assumptions.

## Core Assumptions
- The model operates under these key premises:

- Asset prices follow geometric Brownian motion with consistent volatility

- Markets function without transaction costs or tax implications

- Risk-free interest rates remain stable over the option period

- Underlying assets generate no dividend income

- Arbitrage opportunities are absent from efficient markets

## Mathematical Formulation
For European call options, the Black-Scholes equation is:

C = S₀N(d₁) - Ke^(-rT)N(d₂)

Where:

- C represents the call option premium

- S₀ indicates the current underlying asset price

- K denotes the option strike price

- r signifies the annual risk-free rate

- T expresses the time remaining until expiration

- N(x) is the standard normal cumulative distribution

- d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)

- d₂ = d₁ - σ√T

- σ represents the annualized volatility

The corresponding put option formula is:

P = Ke^(-rT)N(-d₂) - S₀N(-d₁)

## Implied Volatility Computation
Implied volatility reflects the market's collective expectation of future price variability, derived indirectly from observed option prices rather than historical data.

This metric represents the volatility parameter that, when applied within the Black-Scholes framework, produces a theoretical option value matching the current market price. Our implementation employs the Newton-Raphson numerical method to iteratively solve for this implied volatility value.

## Application Usage
The calculator interface provides intuitive input fields for all required parameters:

- Current underlying asset price

- Option strike price

- Time to expiration

- Risk-free interest rate

- Market-observed option price

- Option type selection

- Initial volatility estimate

## Educational Value
This tool serves as both a practical calculator and educational resource, demonstrating:

- Black-Scholes model implementation

- Implied volatility concepts

- Numerical methods in finance

- Financial application development

