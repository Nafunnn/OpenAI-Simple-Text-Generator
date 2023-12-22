import os
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('api_key')
client = OpenAI(api_key=api_key)

chat_history = []

def get_dynamic_system_message(user_input):
    # Your logic to generate or retrieve the dynamic system message based on user input
    # For now, it's a placeholder
    return f"Dynamic system message for user input: {user_input}"

def chat_with_gpt(prompt, system_message):
    messages = [
        {"role": "system", "content": system_message},
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
        chat_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # Dynamically get the system message based on user input
        system_message = get_dynamic_system_message(user_message)

        # Get GPT-3.5 Turbo's response
        gpt_response = chat_with_gpt(user_message, system_message)
        chat_history.append({
            "role": "assistant",
            "content": gpt_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return render_template("index.html", chat_history=chat_history)

@app.route("/clear", methods=["POST"])
def clear_chat():
    global chat_history
    chat_history = []
    print("Chat history cleared")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
