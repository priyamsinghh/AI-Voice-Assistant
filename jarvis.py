from time import strftime
import pyttsx3
import datetime
import pyaudio
import speech_recognition as sr
import wikipedia
import smtplib,ssl
from email.message import EmailMessage
import webbrowser as wb
from bs4 import BeautifulSoup
import requests
import subprocess
import os
import pyautogui as pg
import psutil as ps
import pyjokes as pj

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id) #To set male/female voice

voiceRate = 200
engine.setProperty('rate',voiceRate) # Set the speed of voice

def speak(audio): #Function to speak
    engine.say(audio)
    engine.runAndWait()


def time(): #Function to return current time. Use %I for 12hr format and %U for 24hr format
    Time = datetime.datetime.now().strftime("%I:%M:%S") 
    speak("The current time is")
    speak(Time)


def date(): #Function to return current system date
    year = int(datetime.datetime.now().year)
    mon = int(datetime.datetime.now().month)
    Date = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(Date)
    speak(mon)
    speak(year)


def inputVoice(): #Function to take voice input from user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=5)
        print("Listening...")
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio)
        t = response["transcription"]

    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return t


def wishMe(): #Function to wish the user and ask for further instructions
    H = datetime.datetime.now().hour
    if H>=6 and H<12:
        speak("Good Morning Sir!")
    elif H>=12 and H<18:
        speak("Good Afternoon Sir!")
    elif H>=18 and H<24:
        speak("Good Evening Sir!")
    else:
        speak("Good night Sir!")
    speak("Welcome back")
    speak("How can I help you?")


def search(): #Function to perform Wikipedia Search
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=5)
        print("Listening...")
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio)
        speak(wikipedia.summary(response["transcription"], sentences=2))

    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response
        

def sendmail(): #Function to send email to any user
    msg = EmailMessage()
    speak("What will be the conten of the email?")
    content = inputVoice()
    msg.set_content(content)
    msg["Subject"] = "Test Mail"
    msg["From"] = "coursesarchived@gmail.com"
    msg["To"] = "palakkukreja264@gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"], "Archived@Courses123")
        smtp.send_message(msg)

    speak("Email sent successfully!")

    return


def browse(): #Function to open Google Search in Google Chrome
    speak("Opening Google Chrome!")
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    first_url = 'https://www.google.com/'

    command = f"cmd /C \"{chrome_path}\" {first_url} --new-window"

    subprocess.Popen(command)


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def weather(city): #Function to get weather update using BeautifulSoup Library
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location)
    print(time)
    print(info)
    print(weather+"°C")
    speak(location)
    speak(time)
    speak(info)
    speak(weather+"degree Centigrate")


def song(): #Function to play songs
    songs_dir = "D:\music"
    songs = os.listdir(songs_dir)
    os.startfile(os.path.join(songs_dir, songs[0]))
    return


def create_todo(): #Function to Add a TODO
    speak("What do you want to add?")
    todo = inputVoice()
    rem = open("TODO.txt","w")
    rem.write(todo)
    rem.close()


def check_todo(): #Function to Check your TODO list
    rem = open("TODO.txt","r")
    speak("Your TODO list is:")
    speak(rem.read())


def remove_todo():
    d = inputVoice()
    with open("TODO.txt","r") as f:
        data = f.readlines()

    with open("TODO.txt","w") as f:
        for line in data:
            if line.strip("\n") != d:
                f.write(line)

    speak("TODO removed successfully!")


def screenshot(): #Function to take screenshot
    img = pg.screenshot()
    img.save("D:\ss.png")


def cpu_updates(): #Function to get CPU updates
    usage = str(ps.cpu_percent())
    speak("CPU usage percentage is:"+usage+"%")

    battery = ps.sensors_battery()
    speak("Battery percenatage is:")
    speak(battery.percent)
    speak("%")


def jokes(): #Function to check a joke
    speak(pj.get_joke())


def takeCommand(): #Function to take further instructions from user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=5)
        print("Listening...")
        #r.pause_threshold = 1
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio)
        print(response["transcription"])
        trans = response["transcription"]
        if "time" in trans:
            time()
        elif "date" in trans:
            date()
        elif "offline" in trans:
            quit()
        elif "search" in trans:
            speak("What do you want to search?")
            search()
        elif "email" in trans:
            sendmail()
        elif "browser" in trans:
            browse()
        elif "songs" in trans:
            song()
        elif "log out" in trans:
            os.system("shutdown -l")
        elif "shutdown" in trans:
            os.system("shutdown /s /t 1")
        elif "restart" in trans:
            os.system("shutdown /r /t 1")
        elif "weather" in trans:
            speak("Enter the Name of City")
            city = inputVoice()
            city = city+" weather"
            weather(city)
            print("Have a Nice Day:)")
        elif "add a to do" in trans:
            create_todo()
        elif "check my to do" in trans:
            check_todo()
        elif "remove a to do" in trans:
            speak("What do you want to remove?")
            remove_todo()
        elif "take screenshot" in trans:
            screenshot()
            speak("Screenshot saved successfully!")
        elif "CPU" in trans:
            cpu_updates()
        elif "joke" in trans:
            jokes()

    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__": #Main Function
    
    wishMe()

    while True:
        query = takeCommand()