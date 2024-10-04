from flask import Flask, render_template, jsonify
from langchain_community.llms import Ollama
import pandas as pd
app = Flask(__name__)
llm = Ollama(model="llama3")

def fetch_financial_data(file_path):
    df = pd.read_excel(file_path)
    data = {
        "age": df['Age'].iloc[0],
        "current_income": df['Current Income'].iloc[0],
        "current_expenses": df['Current Expenses'].iloc[0],
        "current_savings": df['Current Savings'].iloc[0],
        "current_debt": df['Current Debt'].iloc[0],
        "investment": df['Total Investment'].iloc[0],
        "types_of_investments": df['Types of Investments'].iloc[0],
        "savings_goals": df['Savings Goals'].iloc[0]
    }
    return data


@app.route('/model/chat', methods=['POST'])
def recommend():
    # Load data from Excel file
    file_path = 'path/to/your/excel/file.xlsx'  # Update this to your file path
    financial_data = fetch_financial_data(file_path)

    # Prepare the prompt
    prompt = f"""I would like some advice on review of my financial status and would love
              to learn how to improve my finances as per my goals and needs
              age : {financial_data['age']} 
              current income : {financial_data['current_income']} 
              current expenses : {financial_data['current_expenses']}
              current savings : {financial_data['current_savings']}
              current debt : {financial_data['current_debt']}
              total_investment : {financial_data['investment']}
              types of investments : {financial_data['types_of_investments']}
              savings_goals : {financial_data['savings_goals']}"""

    response = llm.invoke(prompt, stop=['<|eot_id|>'])
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
