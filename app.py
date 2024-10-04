from flask import Flask, render_template, jsonify
from langchain_community.llms import Ollama
app = Flask(__name__)
llm = Ollama(model="llama3")

def on_startup():
    recommend(f"""I would like some advice on review of my financial status and would love
              to learn how to improve my finances as per my goals and needs
              age : {age} 
              current income : {current_income} 
              current expenses : {current_expenses}
              current savings : {current_savings}
              current debt : {current_debt}
              total_investment : {investment}
              types of investments : {types_of_investments}
              savings_goals : {savings_goals}""")

@app.route('/model/chat', methods=['POST'])
def recommend(prompt):  # put application's code here
    response = llm.invoke(prompt, stop=['<|eot_id|>'])
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
