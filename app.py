from flask import Flask, render_template, jsonify
from langchain_community.llms import Ollama
app = Flask(__name__)
llm = Ollama(model="llama3")
@app.route('/model/chat', methods=['POST'])
def recommend(prompt):  # put application's code here
    response = llm.invoke(prompt, stop=['<|eot_id|>'])
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
