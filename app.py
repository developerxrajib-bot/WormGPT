import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# সরাসরি কী না লিখে এনভায়রনমেন্ট ভ্যারিয়েবল ব্যবহার করুন
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
@app.route('/')
def home():
    return "Llama 3 AI API is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama3-8b-8192", # আপনি চাইলে llama3-70b-8192 ও ব্যবহার করতে পারেন
        )

        reply = chat_completion.choices[0].message.content
        return jsonify({"status": "success", "response": reply})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
