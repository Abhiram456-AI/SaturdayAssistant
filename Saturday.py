import pyttsx3
import speech_recognition as sr
import subprocess
import webbrowser
import datetime
import requests

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.85)

# YouTube API setup
from googleapiclient.discovery import build
API_KEY = 'AIzaSyCuaWtIfC94AVI3k1tgIISrVq3WnX0hshA'
youtube = build("youtube", "v3", developerKey=API_KEY)

# OpenWeatherMap API setup
WEATHER_API_KEY = '51e5f7b411ea3c15cd7f73234e8361b4'

# Hugging Face Mistral API setup
HF_TOKEN = "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"
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

initial_prompt_done = False

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    global initial_prompt_done

    if not initial_prompt_done:
        speak("You can type or speak your command.")
        initial_prompt_done = True

    choice = input("Press Enter to use voice input, or type your command below:\n").strip()
    if choice != "":
        print("You typed:", choice)
        return choice.lower()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return ""

def search_youtube(song_name):
    request = youtube.search().list(
        q=song_name,
        part="id,snippet",
        type="video",
        maxResults=1
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

def play_youtube(song_name):
    url = search_youtube(song_name)
    if url:
        speak(f"Opening YouTube to play {song_name}.")
        webbrowser.get("safari").open(url)
        speak("Playing the song now.")
    else:
        speak(f"Sorry, I couldn't find the song {song_name} on YouTube.")

def open_application(app_name):
    try:
        subprocess.run(["open", "-a", app_name])
        speak(f"Opening {app_name}.")
    except Exception:
        speak(f"Could not open {app_name}, please try again.")

def open_website(url):
    try:
        if not url.startswith("https://") and not url.startswith("http://"):
            url = "https://" + url
        webbrowser.open(url)
        speak(f"Opening {url} in your browser")
    except Exception:
        speak(f"Couldn't open {url}, please try again")

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get('cod') != 200:
            return f"Sorry, I couldn't find weather data for {city}."

        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"The current temperature in {city} is {temp}°C with {description}."
    except Exception:
        return "Sorry, I couldn't fetch the weather information right now."

def ask_mistral(prompt):
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    few_shot_prompt = (
        "You are an assistant that answers with only one short, factual sentence.\n\n"
        "Q: What is gravity?\nA: Gravity is the force that attracts objects with mass toward one another.\n"
        "Q: What is photosynthesis?\nA: Photosynthesis is the process by which plants make food from sunlight.\n"
        "Q: What is Formula 1?\nA:"
    )

    # Dynamically insert the user's question
    user_question = prompt.strip().capitalize().rstrip("?")
    full_prompt = few_shot_prompt.replace("What is Formula 1?", f"What is {user_question}?")

    data = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 60,
            "temperature": 0.3,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "stop": ["\n", "Q:"]
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        output = response.json()

        if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
            result = output[0]["generated_text"]
            return result.split("A:")[-1].strip()
        else:
            return "Sorry, I didn't understand the response from the AI."
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "Sorry, I couldn't reach the AI service."
    
def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
    elif "date" in command:
        speak(f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}")
    elif "play" in command and "youtube" in command:
        if "from youtube" in command:
            song_name = command.split("play", 1)[-1].split("from youtube")[0].strip()
        else:
            song_name = command.split("play", 1)[-1].replace("youtube", "").strip()
        play_youtube(song_name)
    elif command.startswith("open"):
        app_name = command[5:].strip().title()
        open_application(app_name)
    elif "open website" in command or "go to" in command or "visit" in command:
        url = command.replace("open website", "").replace("go to", "").replace("visit", "").strip()
        open_website(url)
    elif "weather" in command:
        city = command.replace("weather in", "").strip()
        if not city:
            speak("Which city's weather would you like to check?")
            city = listen()
        weather_info = get_weather(city)
        speak(weather_info)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        # Fallback: treat anything else as a prompt for Mistral AI
        response = ask_mistral(command)
        print("Saturday:", response)
        speak(response)

if __name__ == "__main__":
    speak("Hi!, I am Saturday. How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            process_command(user_command)