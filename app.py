import os
import openai
from flask import Flask, request, redirect, render_template, session, url_for
from controller.forget_conversation import forget_conversation

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

RESPONSE_ON_ERROR = 'Oh Sempai! You talk a lot💫'


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        sempai_message = request.form["sempai-message"]
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(sempai_message),
                temperature=1,
                max_tokens=280,
                stop=["Sempai:"]
            )
            response_text = response.choices[0].text
        except openai.error.InvalidRequestError as error:
            with open('error.log', 'a', encoding='utf-8') as file:
                file.write(f'Error: {error}\n')
                forget_conversation()
                response_text = RESPONSE_ON_ERROR

        with open('conversation.txt', 'a', encoding='utf-8') as file:
            file.write(f'{response_text}\n')

        session['result'] = response_text
        return redirect(url_for("index"))

    result = session.get('result')
    return render_template("index.html", result=result)


def generate_prompt(sempai_message):
    with open('nagatoro_profile.txt', 'r', encoding='utf-8') as file:
        nagatoro_profile_text = file.read()

    with open('conversation.txt', 'a', encoding='utf-8') as file:
        file.write(f"Sempai: {sempai_message.capitalize()}\nNagatoro: ")

    with open('conversation.txt', 'r', encoding='utf-8') as file:
        conversation_text = file.read()

    return f"""{nagatoro_profile_text}

{conversation_text}
"""
