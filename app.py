import streamlit as st
import numpy as np
import scipy.stats as stats

def calculate_option_vega(spot_price, strike_price, volatility, time_to_expiry, risk_free_rate):
    """
    Compute the vega (volatility sensitivity) of an option
    
    Vega measures how much the option price changes for a 1% change in implied volatility
    """
    d2_numerator = np.log(spot_price / strike_price) + (risk_free_rate - 0.5 * volatility**2) * time_to_expiry
    d2_denominator = volatility * np.sqrt(time_to_expiry)
    d2 = d2_numerator / d2_denominator
    
    vega = strike_price * np.exp(-risk_free_rate * time_to_expiry) * stats.norm.pdf(d2) * np.sqrt(time_to_expiry)
    return vega

def compute_black_scholes_price(option_style, spot_price, strike_price, volatility, time_to_expiry, risk_free_rate):
    """
    Calculate European option price using the Black-Scholes model
    
    Parameters:
    option_style: 'call' or 'put'
    spot_price: Current price of the underlying asset
    strike_price: Option exercise price
    volatility: Annualized standard deviation of returns
    time_to_expiry: Time until expiration in years
    risk_free_rate: Continuously compounded risk-free interest rate
    """
    # Calculate d1 and d2 parameters
    d1_numerator = np.log(spot_price / strike_price) + (risk_free_rate + 0.5 * volatility**2) * time_to_expiry
    d1_denominator = volatility * np.sqrt(time_to_expiry)
    d1 = d1_numerator / d1_denominator
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    
    # Price calculation based on option type
    if option_style.lower() in ['call', 'c']:
        option_value = (spot_price * stats.norm.cdf(d1) - 
                       strike_price * np.exp(-risk_free_rate * time_to_expiry) * stats.norm.cdf(d2))
    elif option_style.lower() in ['put', 'p']:
        option_value = (strike_price * np.exp(-risk_free_rate * time_to_expiry) * stats.norm.cdf(-d2) - 
                       spot_price * stats.norm.cdf(-d1))
    else:
        raise ValueError("Option style must be 'call' or 'put'")
    
    return option_value

def find_implied_volatility(option_style, spot_price, strike_price, initial_vol_guess, 
                           time_to_expiry, risk_free_rate, market_option_price):
    """
    Determine implied volatility using the Newton-Raphson numerical method
    
    Iteratively solves for the volatility that makes the Black-Scholes price 
    match the observed market price
    """
    current_volatility = initial_vol_guess
    convergence_threshold = 1e-10
    iteration_count = 0
    maximum_iterations = 100
    price_discrepancy = float('inf')
    
    while abs(price_discrepancy) > convergence_threshold and iteration_count < maximum_iterations:
        # Calculate current theoretical price and vega
        theoretical_price = compute_black_scholes_price(
            option_style, spot_price, strike_price, current_volatility, 
            time_to_expiry, risk_free_rate
        )
        
        vega_value = calculate_option_vega(
            spot_price, strike_price, current_volatility, 
            time_to_expiry, risk_free_rate
        )
        
        price_discrepancy = theoretical_price - market_option_price
        
        # Avoid division by zero or numerical instability
        if abs(vega_value) < 1e-12:
            current_volatility += 0.01  # Small adjustment to escape flat region
            iteration_count += 1
            continue
        
        # Newton-Raphson update: σ_new = σ_old - (price_error / vega)
        volatility_adjustment = price_discrepancy / vega_value
        current_volatility -= volatility_adjustment
        
        # Ensure volatility stays within reasonable bounds
        current_volatility = max(0.001, min(5.0, current_volatility))
        
        iteration_count += 1
    
    return current_volatility, iteration_count

def main():
    """Main application function for the Implied Volatility Calculator"""
    
    st.set_page_config(
        page_title="Options Analytics: Implied Volatility Calculator",
        page_icon="📊",
        layout="wide"
    )
    
    # Application header
    st.title("📊 Options Analytics: Implied Volatility Calculator")
    st.markdown("""
    Calculate the implied volatility of European options using the Black-Scholes model 
    and Newton-Raphson numerical method.
    """)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Market Parameters")
        
        # User input section
        spot_price = st.number_input(
            "Current Stock Price ($S_0$)", 
            value=100.0, 
            step=1.0,
            help="Current price of the underlying asset"
        )
        
        strike_price = st.number_input(
            "Strike Price ($K$)", 
            value=120.0, 
            step=1.0,
            help="Price at which the option can be exercised"
        )
        
        risk_free_rate = st.number_input(
            "Risk-free Interest Rate ($r$)", 
            value=0.05, 
            step=0.01,
            format="%.3f",
            help="Annual continuously compounded risk-free rate"
        )
        
        time_to_expiry = st.number_input(
            "Time to Expiration ($\\tau$, years)", 
            value=1.0, 
            step=0.1,
            min_value=0.01,
            help="Time until option expiration in years"
        )
    
    with col2:
        st.header("Option Details")
        
        option_style = st.selectbox(
            "Option Type",
            ["call", "put"],
            format_func=lambda x: "Call Option" if x == "call" else "Put Option"
        )
        
        market_option_price = st.number_input(
            "Market Option Price", 
            value=2.0, 
            step=0.1,
            help="Observed market price of the option"
        )
        
        initial_vol_guess = st.number_input(
            "Initial Volatility Estimate", 
            value=0.25, 
            step=0.01,
            min_value=0.01,
            max_value=5.0,
            help="Initial guess for the implied volatility calculation"
        )
        
        st.markdown("---")
        calculate_button = st.button(
            "🚀 Calculate Implied Volatility", 
            type="primary",
            use_container_width=True
        )
    
    # Calculation and results section
    if calculate_button:
        try:
            with st.spinner("Computing implied volatility..."):
                implied_vol, iterations_used = find_implied_volatility(
                    option_style, spot_price, strike_price, initial_vol_guess,
                    time_to_expiry, risk_free_rate, market_option_price
                )
            
            # Display results
            st.success("🎯 Calculation Complete!")
            
            # Results in columns
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.metric(
                    "Implied Volatility", 
                    f"{implied_vol:.4f}", 
                    f"{(implied_vol - initial_vol_guess):+.4f} from initial guess"
                )
            
            with res_col2:
                st.metric("Iterations Required", f"{iterations_used}")
            
            with res_col3:
                validated_price = compute_black_scholes_price(
                    option_style, spot_price, strike_price, implied_vol,
                    time_to_expiry, risk_free_rate
                )
                price_error = abs(validated_price - market_option_price)
                st.metric("Price Validation Error", f"${price_error:.2e}")
            
            # Detailed results
            st.subheader("Detailed Results")
            results_markdown = f"""
            | Parameter | Value |
            |-----------|-------|
            | **Option Type** | {option_style.title()} |
            | **Spot Price ($S_0$)** | ${spot_price:.2f} |
            | **Strike Price ($K$)** | ${strike_price:.2f} |
            | **Time to Expiry ($\\tau$)** | {time_to_expiry:.2f} years |
            | **Risk-free Rate ($r$)** | {risk_free_rate:.2%} |
            | **Market Option Price** | ${market_option_price:.2f} |
            | **Initial Volatility Guess** | {initial_vol_guess:.4f} |
            | **Calculated Implied Volatility** | **{implied_vol:.6f}** |
            | **Iterations to Converge** | {iterations_used} |
            """
            st.markdown(results_markdown)
            
            # Verification section
            st.subheader("🔍 Model Verification")
            verification_price = compute_black_scholes_price(
                option_style, spot_price, strike_price, implied_vol,
                time_to_expiry, risk_free_rate
            )
            
            st.write(f"**Theoretical Price using Implied Volatility:** ${verification_price:.6f}")
            st.write(f"**Market Price:** ${market_option_price:.6f}")
            
            if abs(verification_price - market_option_price) < 1e-8:
                st.success("✅ Excellent match between model and market prices!")
            else:
                st.warning("⚠ Small discrepancy between model and market prices")
                
        except Exception as error:
            st.error(f"❌ Calculation Error: {str(error)}")
            st.info("💡 Tips: Check that all inputs are positive and try adjusting your initial volatility estimate")
    
    # Information sidebar
    with st.sidebar:
        st.header("About This Calculator")
        st.markdown("""
        This tool calculates **implied volatility** - the market's forecast of 
        a stock's future price movements as reflected in option prices.
        
        **Methodology:**
        - Black-Scholes option pricing model
        - Newton-Raphson numerical root finding
        - European-style options only
        
        **Assumptions:**
        - Constant volatility
        - No transaction costs
        - Continuous trading
        - Constant risk-free rate
        - No dividends
        
        Use this for educational and analytical purposes.
        """)
        
        st.header("Input Guidelines")
        st.markdown("""
        - **Spot Price**: Current stock price
        - **Strike Price**: Option exercise price  
        - **Time to Expiry**: In years (e.g., 0.25 = 3 months)
        - **Risk-free Rate**: Annual rate (e.g., 0.05 = 5%)
        - **Initial Volatility Guess**: Start with 0.2-0.3 for most stocks
        """)

if __name__ == "__main__":
    main()