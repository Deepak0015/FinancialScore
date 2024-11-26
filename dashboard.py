import streamlit as st
import requests
import matplotlib.pyplot as plt

# Streamlit app
st.title("Financial Score Dashboard")
st.markdown("Input your family and financial data to calculate your financial score.")

# Input fields
SavingsRatio = st.number_input("Savings Ratio (0 to 1)", 0.0, 1.0, 0.2)
Loan_income_Pct = st.number_input("Loan-to-Income Percentage (0 to 1)", 0.0, 1.0, 0.2)
CreditSpend_Pct = st.number_input("Credit Spend Percentage (0 to 1)", 0.0, 1.0, 0.3)
Essential_Spending_Pct = st.number_input("Essential Spending Percentage (0 to 1)", 0.0, 1.0, 0.4)
NonEssential_Spending_Pct = st.number_input("Non-Essential Spending Percentage (0 to 1)", 0.0, 1.0, 0.3)
Monthly_Expenses_to_Income = st.number_input("Monthly Expenses-to-Income Ratio (0 to 1)", 0.0, 1.0, 0.5)
GoalsMet = st.number_input("Goals Met (0 to 100)", 0, 100, 80)

# Button to calculate score
if st.button("Calculate Score"):
    payload = {
        "SavingsRatio": SavingsRatio,
        "Loan_income_Pct": Loan_income_Pct,
        "CreditSpend_Pct": CreditSpend_Pct,
        "Essential_Spending_Pct": Essential_Spending_Pct,
        "NonEssential_Spending_Pct": NonEssential_Spending_Pct,
        "Monthly_Expenses_to_Income": Monthly_Expenses_to_Income,
        "GoalsMet": GoalsMet
    }
    # Make API call
    response = requests.post("http://127.0.0.1:5000/score", json=payload)

    if response.status_code == 200:
        result = response.json()

        # Display Total Financial Score
        st.success(f"Your Total Financial Score: {result['total_score']}")

        # Display Score Board Results
        st.write("**Score Board Results:**")
        score_board = result["Score Board"]
        st.table(score_board)

        # Create a bar chart for the score breakdown
        st.write("**Score Breakdown**:")
        categories = list(score_board.keys())
        scores = list(score_board.values())

        # Plot bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(categories, scores, color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Scores')
        plt.title('Financial Score Breakdown')
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)

        # Display Insights
        st.write("**Insights:**")
        st.info(result["insights"])

        # Display Recommendations
        st.write("**Recommendations:**")
        st.warning(result["recommendations"])

    else:
        st.error("Error in API call.")

