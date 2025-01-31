import streamlit as st
import pandas as pd

# Inject custom CSS to style the "Calculate ROI" button
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0073E6;  /* NomadGo Blue */
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #005bb5; /* Slightly darker blue on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI

# Create two columns for side-by-side logos
col1, col2 = st.columns([1, 1])

# Display QSR logo on the left
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/McDonald%27s_logo.svg", width=150)

# Display NomadGo logo on the right
with col2:
    st.image("<img src="https://cdn.prod.website-files.com/63464a83595dfc63e7e1662f/64e904bb5806093b06821451_Logo.png", width=150)  # Replace with actual logo

# Centered text below logos
st.markdown("<h1 style='text-align: center;'>We're Just Better Together</h1>", unsafe_allow_html=True)

st.write("Estimate the potential savings and revenue impact of using our automated inventory management.")

# User Inputs
num_locations = st.number_input("Number of Locations", min_value=1, max_value=5000, value=100)
counts_per_location = st.number_input("Inventory Counts per Location per Month", min_value=1, max_value=30, value=5)
manual_time = st.slider("Time to Manually Take Inventory (Minutes)", min_value=5, max_value=120, value=30)
automated_time = st.slider("Time with NomadGo (Minutes)", min_value=1, max_value=30, value=5)
hourly_wage = st.number_input("Hourly Wage of Employees Performing Counts ($)", min_value=10.0, max_value=50.0, value=18.0)
shrinkage_rate = st.slider("Estimated Inventory Shrinkage (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
lost_sales = st.number_input("Average Sales Lost Due to Stockouts ($ per Location)", min_value=1000, max_value=100000, value=10000)

# Function to calculate ROI
def calculate_worksprings_roi(num_locations, counts_per_location, manual_time, automated_time, hourly_wage, shrinkage_rate, lost_sales):
    # Ensure automated time is not greater than manual time
    if automated_time >= manual_time:
        return {
            "Error": "Automated time must be less than manual time for savings to exist."
        }

    # Calculate time saved per count
    time_saved_per_count = manual_time - automated_time  # Minutes saved

    # Convert minutes saved to hours
    total_hours_saved = (num_locations * counts_per_location * time_saved_per_count) / 60  # Convert to hours

    # Calculate labor savings
    labor_savings = total_hours_saved * hourly_wage * 12  # Annual savings

    # Calculate shrinkage reduction savings
    shrinkage_savings = (shrinkage_rate / 100) * lost_sales * num_locations

    # Estimate additional revenue from better inventory tracking
    recovered_sales = (lost_sales * 0.3) * num_locations  # Assume 30% of lost sales can be recovered

    # Total financial impact
    total_savings = labor_savings + shrinkage_savings + recovered_sales

    # **Fix: Investment cost should only be manual labor BEFORE Worksprings**
    manual_labor_cost_before = (num_locations * counts_per_location * manual_time / 60 * hourly_wage * 12)

    # ROI Amount
    roi_amount = total_savings - manual_labor_cost_before

    # ROI Percentage (Fixed)
    roi_percentage = (roi_amount / manual_labor_cost_before) * 100 if manual_labor_cost_before > 0 else 0

    return {
        "Labor Cost Savings": f"${labor_savings:,.2f}",
        "Reduction in Inventory Shrinkage": f"${shrinkage_savings:,.2f}",
        "Recovered Sales": f"${recovered_sales:,.2f}",
        "Total Financial Impact": f"${total_savings:,.2f}",
        "Investment Cost": f"${manual_labor_cost_before:,.2f}",
        "ROI Amount": f"${roi_amount:,.2f}",
        "Estimated ROI (%)": f"{max(roi_percentage, 0):,.2f}%"
    }

# Calculate ROI when user presses button
if st.button("Calculate ROI"):
    results = calculate_worksprings_roi(num_locations, counts_per_location, manual_time, automated_time, hourly_wage, shrinkage_rate, lost_sales)

    # Handle potential errors
    if "Error" in results:
        st.error(results["Error"])  # ✅ Fixed syntax issue
    else:
        # Convert results to DataFrame without an index column
        results_df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])

        # Display results without index
        st.subheader("ROI Results")
        st.table(results_df.style.hide(axis="index"))  # Hide index

        st.success("Calculation Complete! Adjust values to see different scenarios.")

# Footer
st.write("Powered by Worksprings | Streamlining Inventory Management")
