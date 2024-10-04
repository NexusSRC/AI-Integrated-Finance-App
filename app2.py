from flask import Flask, render_template, request, jsonify
from langchain_community.llms import Ollama
import pandas as pd
import os

app = Flask(__name__)
llm = Ollama(model="llama3")

# Create uploads directory if it doesn't exist
uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)


def fetch_financial_data(file_path):
    try:
        print(f"Loading data from {file_path}...")
        df = pd.read_excel(file_path)

        # Check if necessary columns exist
        required_columns = [
            'Age',
            'Current Income',
            'Current Expenses',
            'Current Savings',
            'Current Debt',
            'Total Investment',
            'Types of Investments',
            'Savings Goals'
        ]

        print(f"Columns in the Excel file: {df.columns.tolist()}")

        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in the Excel file.")

        # Extract data
        data = {col.lower().replace(' ', '_'): df[col].iloc[0] for col in required_columns}
        print(f"Extracted financial data: {data}")
        return data

    except Exception as e:
        print(f"Error fetching financial data: {str(e)}")
        return {"error": str(e)}


@app.route('/model/chat', methods=['POST'])
def recommend():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['file']
    file_path = os.path.join(uploads_dir, file.filename)
    print(f"Saving uploaded file to {file_path}...")
    file.save(file_path)

    financial_data = fetch_financial_data(file_path)
    os.remove(file_path)

    if "error" in financial_data:
        return jsonify({"error": financial_data["error"]}), 400

    # Prepare the prompt for the language model
    prompt = f"""I would like some advice on reviewing my financial status and would love
              to learn how to improve my finances as per my goals and needs:
              age: {financial_data['age']} 
              current monthly income: {financial_data['current_income']} 
              current monthly expenses: {financial_data['current_expenses']}
              current savings: {financial_data['current_savings']}
              current debt: {financial_data['current_debt']}
              total investment: {financial_data['total_investment']}
              types of investments: {financial_data['types_of_investments']}
              savings goals: {financial_data['savings_goals']}"""

    print(f"Prompt for LLM: {prompt}")

    try:
        response = llm.invoke(prompt, stop=['<|eot_id|>'])
        print(response)
        print(f"Received response from LLM.")
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error invoking LLM: {str(e)}")
        return jsonify({"error": "Failed to get advice from the model: " + str(e)}), 500


@app.route('/')
def index():
    return render_template('index1.html')


if __name__ == '__main__':
    app.run(debug=True)
