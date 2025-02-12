from slack_sdk import WebClient
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask,request, jsonify
# import openai
import google.generativeai as genai
import logging

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
client=WebClient(token=os.environ['SLACK_TOKEN'])
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")
# openai.api_key=os.environ['OPEN_AI_API']
# client.chat_postMessage(channel="#bot-messages", text="hello")

app=Flask(__name__)
@app.route("/slack/events", methods=["POST"])
def slack_events():
    try: 
        data = request.json

    # Handle Slack URL verification challenge
        if "challenge" in data:
            return jsonify({"challenge": data["challenge"]})

    # Process events if the request is from Slack
        if "event" in data:
            event_type = data["event"]["type"]

        # Handle messages sent to the channel
            if event_type == "message" and "subtype" not in data["event"]:
            # channel = data["event"]["channel"]
            # user = data["event"]["user"]
                text = data["event"]["text"]
                # print(text)
                prompt=f"Read and validate the following Python function:\n{text}\n\n" \
                        f"Does the function have any errors? If there are any errors specify them.If not, execute it and return only the result of the code."
                try: 
                    response = model.generate_content(prompt)
                    print(response.text)
                except Exception as e:
                    logging.error(f"Error generating content: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
            

            
        
            

    return jsonify({"status": "OK"})


if __name__=="__main__":
    app.run(debug=True)