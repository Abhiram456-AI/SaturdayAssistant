#Saturday - AI Voice Assistant

Saturday is a Python-powered AI voice assistant that listens to your voice or typed commands and helps you with everyday tasks — from playing YouTube videos and checking the weather to answering questions with short, clear responses using the Mistral AI model.

⸻

Features
	•	Voice & Text Input: Interact by speaking or typing commands.
	•	YouTube Playback: Search and play videos quickly.
	•	Weather Updates: Get current weather info for any city worldwide.
	•	Web Browsing: Open any website with a simple command.
	•	AI Answers: Ask questions and receive concise, relevant definitions and explanations powered by the Mistral AI model.
	•	Text-to-Speech: Hear responses spoken aloud for a smooth user experience.

⸻

Getting Started

Prerequisites
	•	Python 3.7 or higher
	•	APIs:
	•	YouTube Data API v3
	•	OpenWeatherMap API
	•	Hugging Face API Token
 
1. Clone the repo:
git clone https://github.com/yourusername/saturday.git
cd saturday

2. python3 -m venv .venv
source .venv/bin/activate  Windows: .venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. check the API keys inside the script (Saturday.py) in the respective variables:
	•	API_KEY for YouTube
	•	WEATHER_API_KEY for OpenWeatherMap
	•	HF_TOKEN for Hugging Face

5. Run the assistant:
python Saturday.py

You will be prompted to type or speak your command.
	•	Try commands like:
	•	“Play Shape of You from YouTube”
	•	“What is the weather in New York?”
	•	“Open website example.com”
	•	“Who is Albert Einstein?”
	•	Say “exit” or “quit” to close the assistant.
