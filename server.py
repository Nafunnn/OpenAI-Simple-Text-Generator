import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('api_key')
client = OpenAI(api_key=api_key)

chat_history = []

def chat_with_gpt(prompt):
    messages = [
        {"role": "system", "content": "kamu adalah penulis konten yang hebat. buatkan saya tulisan menjadi 4 bagian untuk instagram saya. 1 pendahuluan, 2 latar belakang, 3 masalah 4 solusi. kamu akan saya berikan topik sebagai acuan."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form["user_message"]
        chat_history.append({"role": "user", "content": user_message})

        # Get GPT-3.5 Turbo's response
        gpt_response = chat_with_gpt(user_message)
        chat_history.append({"role": "assistant", "content": gpt_response})

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
