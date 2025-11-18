# Black-Scholes-Option-Pricing
Project Description
This interactive web application implements the Black-Scholes financial model for calculating option prices and determining implied volatility. Built using Streamlit, the tool offers an accessible platform for financial professionals, academic researchers, and students to perform option valuation analysis through an intuitive web interface.

Key Functionality
Compute theoretical option prices using the Black-Scholes mathematical framework

Determine implied volatility from observed market option prices

Support for both call and put option types

Interactive parameter input system

Instant calculation results with clear visual presentation

Setup Instructions
Obtain the project files by cloning the repository to your local system

Change to the project directory in your terminal

Install necessary Python packages:

text
pip install streamlit numpy scipy matplotlib
Launching the Application
Execute the application using the command:

text
streamlit run app.py
Access the application through your web browser using the local address provided in the terminal output, typically http://localhost:8501.

Theoretical Foundation
Black-Scholes Option Pricing Model
The Black-Scholes model represents a groundbreaking mathematical approach to option valuation, developed through collaborative work by financial researchers. This model calculates theoretical prices for European-style options based on several key market assumptions.

Core model assumptions include:

Underlying asset prices follow logarithmic normal distribution patterns

Absence of transaction fees and tax considerations

Stable risk-free interest rates throughout the option period

Non-dividend paying underlying assets

Elimination of arbitrage opportunities

Mathematical Formulation
For call option valuation, the Black-Scholes equation is:

C = S₀N(d₁) - Ke^(-rT)N(d₂)

Variable definitions:

C represents the call option theoretical price

S₀ indicates the current underlying asset price

K denotes the option strike price

r signifies the annual risk-free interest rate

T expresses the time remaining until option expiration

N(x) represents the standard normal cumulative distribution function

d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)

d₂ = d₁ - σ√T

σ symbolizes the underlying asset's volatility

For put option valuation, the corresponding formula is:

P = Ke^(-rT)N(-d₂) - S₀N(-d₁)

Implied Volatility Concept
Implied volatility reflects the financial market's collective prediction of future price variability for a security. This forward-looking metric estimates potential price fluctuations based on current option market prices.

Within the Black-Scholes framework, implied volatility represents the specific volatility value that, when applied to the model equations, produces a theoretical option price matching the observed market price. The application employs the Newton-Raphson numerical method to iteratively solve for this implied volatility value.

Development Contributions
We welcome enhancements and improvements to this project. Interested developers can create their own versions of the repository and propose changes through pull requests.
