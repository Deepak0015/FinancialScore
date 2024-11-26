
# Financial Scoring Application

## **Overview**
The Financial Scoring Application is designed to evaluate and provide actionable insights into a family's financial health. The project consists of:
1. **A Flask-based API** for calculating financial scores.
2. **A Streamlit-based dashboard** for interactive user input and score visualization.
3. **Jupyter Notebook** for further analysis and visualization of financial data.

This system allows families to input financial metrics, compute their financial scores based on a well-defined scoring mechanism, and receive recommendations for improving financial health.

---

## **Features**
- **Financial Score Calculation**:
  - Evaluates financial health based on various factors, such as:
    - **Savings-to-Income Ratio**
    - **Loan-to-Income Percentage**
    - **Credit Spending Trends**
    - **Essential vs. Non-Essential Spending**
    - **Monthly Expenses-to-Income Ratio**
    - **Goals Met Percentage**
  - Provides a **score breakdown** for better transparency.
  - Offers **insights** and **actionable recommendations** for improvement.

- **Interactive Dashboard**:
  - User-friendly interface for entering financial metrics.
  - Visual representation of scores and actionable insights.

- **API Integration**:
  - Flexible API for calculating scores programmatically.

---

## **Workflow**
### 1. **Input Financial Data**
Users can provide the following details through the Streamlit dashboard or as JSON payloads to the API:
  - `SavingsRatio`: Savings as a percentage of income.
  - `Loan_income_Pct`: Loan payments as a percentage of income.
  - `CreditSpend_Pct`: Credit card spending as a percentage of income.
  - `Essential_Spending_Pct`: Percentage of income spent on essential items.
  - `NonEssential_Spending_Pct`: Percentage of income spent on non-essential items.
  - `Monthly_Expenses_to_Income`: Monthly expenses as a percentage of income.
  - `GoalsMet`: Percentage of financial goals achieved.

### 2. **Score Calculation (Flask API)**
The Flask API uses the `calculate_score` function to:
- Assign weights to various financial metrics.
- Compute scores for each category and the total financial score (0–100).
- Generate detailed insights and improvement recommendations.

### 3. **Interactive Visualization (Streamlit Dashboard)**
The dashboard:
- Sends user input to the API.
- Displays the **total financial score**, a **score breakdown**, insights, and recommendations.
- Allows users to identify improvement areas through clear visualizations.

---

## **Project Structure**
```
Financial Scoring Project/
│
├── app.py              # Flask-based API for score calculation
├── dashboard.py        # Streamlit dashboard for user interaction
├── notebook.ipynb           # Jupyter Notebook for analysis and visualizations
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (this file)
```

---

## **Installation and Setup**

### Prerequisites
- Python 3.8 or later
- Flask, Streamlit, Pandas, Requests (see `requirements.txt`)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Deepak001/financial-scoring.git
   cd financial-scoring
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask API**:
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000/score`.

4. **Run the Streamlit Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```
   Access the dashboard at `http://localhost:8501`.

5. **Optional**: Explore the Jupyter Notebook for additional analysis:
   ```bash
   jupyter notebook nootbook.ipynb
   ```

---

## **Usage**

### **Using the Dashboard**
1. Start the Streamlit app and provide the following inputs:
   - Savings Ratio, Loan-to-Income %, Credit Spending %, etc.
2. Click **"Calculate Score"** to:
   - View the **Total Financial Score**.
   - Get a detailed **Score Board** with breakdowns.
   - Read personalized **Insights** and **Recommendations**.

### **Using the API**
Send a POST request to `http://127.0.0.1:5000/score` with a JSON payload like:
```json
{
  "SavingsRatio": 0.25,
  "Loan_income_Pct": 0.15,
  "CreditSpend_Pct": 0.20,
  "Essential_Spending_Pct": 0.50,
  "NonEssential_Spending_Pct": 0.30,
  "Monthly_Expenses_to_Income": 0.60,
  "GoalsMet": 75
}
```

Example using `curl`:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"SavingsRatio":0.25, "Loan_income_Pct":0.15, "CreditSpend_Pct":0.20, "Essential_Spending_Pct":0.50, "NonEssential_Spending_Pct":0.30, "Monthly_Expenses_to_Income":0.60, "GoalsMet":75}' http://127.0.0.1:5000/score
```

---

## **Score Calculation Logic**
The `calculate_score` function evaluates six categories:

1. **Savings Score (25 Points)**:
   - Higher savings ratios earn more points.
   - Deduction if savings are below 20%.
   - Saving minimum Range 20%

2. **Loan Score (15 Points)**:
   - Rewards low loan-to-income ratios.
   - Penalizes if loans exceed 20% of income.
   - Load Maximum range 20 %

3. **Credit Score (15 Points)**:
   - Encourages keeping credit card spending under 30%.
   - Maximum spending Range is 30% 

4. **Category Score (15 Points)**:
   - Balances essential vs. non-essential spending.

5. **Monthly Expense Score (20 Points)**:
   - Expenses exceeding 50% of income result in deductions.

6. **Goal Score (10 Points)**:
   - Rewards achieving financial goals.

### Total Score:
The sum of all category scores is capped at 100 points.

---

## **Outputs**
### **Example Response from API**
```json
{
  "Score Board": {
    "Savings Score": 20,
    "Monthly Expense Score": 15,
    "Loan Score": 12,
    "Credit Score": 10,
    "Category Score": 10,
    "Goal Score": 8
  },
  "total_score": 75,
  "insights": "Savings-to-Income ratio is below the recommended level...",
  "recommendations": "Reduce discretionary spending by 10% to improve your score."
}
```

---


