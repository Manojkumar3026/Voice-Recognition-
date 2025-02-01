import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import os
import datetime
import sys
import requests
import json
import smtplib
import pyjokes
import time

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Listen to User Voice Input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Network issue. Please check your internet connection.")
        return ""

# Function to Get the Current Time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Function to Get Today's Date
def get_date():
    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today_date}")

# Function to Open Websites
def open_website(command):
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://www.facebook.com"
    }
    for site in sites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(sites[site])
            return

# Function to Search on Wikipedia
def search_wikipedia(command):
    query = command.replace("search", "").strip()
    speak(f"Searching {query} on Wikipedia")
    try:
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found for this search.")

# Function to Play Music
def play_music():
    music_path = "C:\\Users\\YourUsername\\Music\\song.mp3"  # Update with your music file path
    if os.path.exists(music_path):
        speak("Playing music")
        os.system(f"start {music_path}")
    else:
        speak("Music file not found.")

# Function to Handle System Commands
def system_control(command):
    if "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "logout" in command:
        speak("Logging out.")
        os.system("shutdown -l")

# Function to Get Weather Information
def get_weather():
    api_key = "your_openweather_api_key"  # Replace with your OpenWeather API Key
    city = "your_city_name"  # Replace with your city name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    if weather_data["cod"] == 200:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't fetch the weather details.")

# Function to Get News Headlines
def get_news():
    api_key = "your_newsapi_key"  # Replace with your NewsAPI Key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

    response = requests.get(url)
    news_data = response.json()

    if news_data["status"] == "ok":
        articles = news_data["articles"][:5]  # Fetch top 5 headlines
        for article in articles:
            speak(article["title"])
    else:
        speak("Sorry, I couldn't fetch the news.")

# Function to Tell a Joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to Send Email
def send_email():
    try:
        speak("Who do you want to send the email to?")
        recipient = listen()

        speak("What should I say in the email?")
        content = listen()

        sender_email = "your_email@gmail.com"  # Replace with your email
        sender_password = "your_password"  # Replace with your email password

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, content)
        server.close()

        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I was unable to send the email.")

# Function to Set an Alarm
def set_alarm():
    speak("At what time should I set the alarm? Please say in HH:MM format.")
    alarm_time = listen()
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Wake up! Your alarm is ringing.")
            break
        time.sleep(30)

# Function to Process Commands
def process_command(command):
    if "time" in command:
        get_time()
    elif "date" in command:
        get_date()
    elif "open" in command:
        open_website(command)
    elif "search" in command:
        search_wikipedia(command)
    elif "play music" in command:
        play_music()
    elif "weather" in command:
        get_weather()
    elif "news" in command:
        get_news()
    elif "tell me a joke" in command:
        tell_joke()
    elif "send email" in command:
        send_email()
    elif "set alarm" in command:
        set_alarm()
    elif "shutdown" in command or "restart" in command or "logout" in command:
        system_control(command)
    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        sys.exit()
    else:
        speak("Sorry, I didn't understand that command.")

# Main Program Loop
if __name__ == "__main__":
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            process_command(command)
