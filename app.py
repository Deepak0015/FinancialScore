from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Function to calculate score
def calculate_score(row):
    insights = []
    recommendations = []

    # Calculate the Savings Score (25 Points)
    ideal_savings_ratio = 0.2  # Ideal is 20%
    savings_score = min(row['SavingsRatio'] * 125, 25)
    if row['SavingsRatio'] < ideal_savings_ratio:
        points_lost = 25 - savings_score
        insights.append(
            f"Savings-to-Income ratio is {row['SavingsRatio']:.2%}, below the recommended {ideal_savings_ratio:.2%}, reducing your score by {points_lost:.1f} points."
        )
        recommendations.append(
            f"Increase savings by reallocating discretionary spending. Raising SavingsRatio to 0.20 can improve your score by {points_lost:.1f} points."
        )
    else:
        insights.append("Savings Ratio is Good, Keep Saving!")
        recommendations.append("Your savings are within a good range. Maintain this to preserve your score.")

    # Calculate Loan Score (15 Points)
    ideal_loan_ratio = 0.2  # Ideal is 20%
    loan_ratio = min(row['Loan_income_Pct'], 1)  # Cap at 100%
    loan_score = max(0, (1 - loan_ratio) * 15)  # Change the base to 15 points
    loan_score = min(loan_score, 15)  # Ensure loan_score does not exceed 15

    if row['Loan_income_Pct'] > ideal_loan_ratio:
        points_lost = 15 - loan_score
        insights.append(
            f"Loan payments are {row['Loan_income_Pct']:.2%} of income, above the recommended {ideal_loan_ratio:.2%}, reducing your score by {points_lost:.1f} points."
        )
        recommendations.append(
            f"Focus on loan repayment to reduce Loan_income_Pct to below 20%. This can improve your score by {points_lost:.1f} points."
        )
    else:
        insights.append("Loan Ratio is Good, Keep It Up!")
        recommendations.append("Your loan ratio is within the ideal range. Maintain this to preserve your score.")

    # Calculate Credit Score (15 Points)
    ideal_credit_ratio = 0.3  # Ideal is 30%
    credit_score = max(0, (1 - row['CreditSpend_Pct']) * 15)
    credit_score = min(max(0, credit_score), 15)  # Cap credit score to 15

    if row['CreditSpend_Pct'] > ideal_credit_ratio:
        points_lost = 15 - credit_score
        insights.append(
            f"Credit card spending is {row['CreditSpend_Pct']:.2%} of income, exceeding the ideal {ideal_credit_ratio:.2%}, reducing your score by {points_lost:.1f} points."
        )
        recommendations.append(
            f"Reduce credit card usage to bring CreditSpend_Pct to below 30%. This can improve your score by {points_lost:.1f} points."
        )
    else:
        insights.append("Credit Spending Ratio is Good, Keep It Up! ")
        recommendations.append("Your credit card spending is within the ideal range. Maintain this to preserve your score.")

    # Calculate Category Score (15 Points)
    essential_score = max(0, (1 - row['Essential_Spending_Pct']) * 7.5)
    non_essential_score = max(0, (1 - row['NonEssential_Spending_Pct']) * 7.5)
    category_score = essential_score + non_essential_score

    if essential_score < non_essential_score:
        points_lost = 15 - category_score
        insights.append(
            f"Non-essential spending ({row['NonEssential_Spending_Pct']:.2%}) exceeds essential spending ({row['Essential_Spending_Pct']:.2%}), lowering your score."
        )
        recommendations.append(
            f"Reallocate spending to increase essential spending. Reducing non-essential spending by 10% can improve your score by approximately {points_lost:.1f} points."
        )
    else:
        insights.append("Essential Spending Ratio is Good, Keep It Up!")
        recommendations.append("Your essential spending is within the ideal range. Maintain this to preserve your score.")

    # Calculate Monthly Expenses Score (20 Points)
    monthly_expense_score = max(0, (1 - row['Monthly_Expenses_to_Income']) * 20)
    monthly_expense_ratio = 0.5
    if row['Monthly_Expenses_to_Income'] > monthly_expense_ratio:  # Ideal expense ratio is 50%
        points_lost = 20 - monthly_expense_score
        insights.append(
            f"Monthly expenses are {row['Monthly_Expenses_to_Income']:.2%} of income, exceeding the ideal 50%, reducing your score by {points_lost:.1f} points."
        )
        recommendations.append(
            f"Reduce monthly expenses, especially non-essential spending, to below 50% of income. This can improve your score by {points_lost:.1f} points."
        )
    else:
        insights.append(f"Monthly Expenses Spending Ratio is {row['Monthly_Expenses_to_Income']:.2%} it is  Good, Keep It Up!")
        recommendations.append(f"Your Monthly  Expenses  spending  is {row['Monthly_Expenses_to_Income']:.2%} within the ideal range 50%. Maintain this to preserve your score.")

    # Calculate Goal Score (10 Points)
    goal_score = row['GoalsMet'] * 0.1
    print(goal_score)
    if row['GoalsMet'] < 100:
        points_lost = 10 - goal_score
        insights.append(
            f"Only {row['GoalsMet']}% of financial goals met, which affects your score by {points_lost:.1f} points."
        )
        recommendations.append(
            f"Work towards achieving more financial goals. Increasing GoalsMet to 100% can improve your score by {points_lost:.1f} points."
        )
    else:
        insights.append("Goal Score is  Good, Keep It Up!, Increase Goals Meet to increase {points_lost:.f} Points")
        recommendations.append("Your Goalmet percentage  is within the ideal range . Maintain this to preserve your score.")


    # Calculate Total Score (out of 100)
    points = {'Savings Score':savings_score ,'Monthly Expense Score': monthly_expense_score ,'Loan Score': loan_score ,"Credit Score": credit_score ,"Category Score": category_score , 'Goal Score': goal_score }
    total_score = savings_score + monthly_expense_score + loan_score + credit_score + category_score + goal_score
    total_score = min(max(total_score, 1), 100)
    # print(savings_score + monthly_expense_score + loan_score + credit_score + category_score + goal_score)

    # Return the final score, insights, and recommendations
    return points , total_score, " ".join(insights), " ".join(recommendations)
# API Endpoint
@app.route('/score', methods=['POST'])
def score():
    try:
        # Input validation
        data = request.json
        df = pd.DataFrame([data])  # Convert to DataFrame for processing
        result = df.apply(calculate_score, axis=1)
        points ,total_score, insights, recommendations = result.iloc[0]

        return jsonify({
            "Score Board":points,
            "total_score": total_score,
            "insights": insights,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
