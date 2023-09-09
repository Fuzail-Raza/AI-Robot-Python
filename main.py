# import webdriver
import speech_recognition as sr
import win32com.client
import webbrowser
import os
import datetime
import openai
import requests
import json
from api_keys import apikey , weather_api
import geonamescache
import time
import re
import winsound
from win10toast import ToastNotifier
from pytube import YouTube
import vlc
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from api_keys import MongoDBURL
import uuid
import threading



def word_to_number(word):
    word_dict = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "13": 13,
        "14": 14,
        "15": 15,
        "16": 16,
        "17": 17,
        "18": 18,
        "19": 19,
        "20": 20,
        "30": 30,
        "40": 40,
        "50": 50,
        "60": 60,
        "70": 70,
        "80": 80,
        "90": 90,
        "100": 100,
        "1000": 1000
    }

    words = word.lower().split()
    result = 0
    current_num = 0

    for w in words:
        if w in word_dict:
            num = word_dict[w]
            if num == 100 or num == 1000:
                current_num *= num
                result += current_num
                current_num = 0
            else:
                current_num += num

    return result + current_num


def set_reminder(message):

    delay=word_to_number(message)
    unit=""
    if "Hour".lower() in message.lower():
        unit="Hours"
    elif "Minute".lower() in message.lower():
        unit="Minutes"
    elif "Seconds".lower()  in message.lower():
        unit="Seconds"
    elif delay<=0:
        print("Sorry, I couldn't understand the time. Please try again.")
        say("Sorry, I couldn't understand the time. Please try again.")
        return
    else:
        say("No Unit Define...Please Try Again")
        print("No Unit Define...Please Try Again")
        return


    time_start=time.strftime(f"%{unit[0]}")
    print(f"Alarm set for {delay} {unit}")
    say(f"Alarm set for {delay} {unit}")
    while True:
        time_now=int(time.strftime(f"%{unit[0]}"))-int(time_start)
        if(time_now>=delay):
            toaster = ToastNotifier()
            toaster.show_toast("Take Rest", f"Please Take a rest for while you are using laptop for {time_now} {unit} with no break", duration=1)
            frequency = 1000  
            duration = 1000
            winsound.Beep(frequency, duration)
            say(f"Take Rest... Please Take a rest for while you are using laptop for {time_now} {unit} with no break")
            time.sleep(2)
            break




def get_all_cities():
    gc = geonamescache.GeonamesCache()
    cities = [city['name'] for city in gc.get_cities().values() if len(city['name']) > 4]
    return cities

def weather(message):

    cities=get_all_cities()
    messagecity=""
    for city in cities:
        try:
            if city.lower() in message.lower():
                    messagecity=city
                    break
        except:
            pass 
    
    try:
        url=f"http://api.weatherapi.com/v1/current.json?key={weather_api}&q={messagecity}"

        respone=requests.get(url)
        wdict=json.loads(respone.text)
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Voice =  speaker.GetVoices().Item(1)
        print(f"The weather of {city} is {wdict['current']['temp_c']}C and Wind Speed is  {wdict['current']['wind_mph']} km/h")
        speaker.Speak(f"The weather of {city} is {wdict['current']['temp_c']}Celsius and Wind Speed is  {wdict['current']['wind_mph']} km/h")
    except :
        print("City Not Found")
        say("City Not Found")
        return
    while True:
        print("Say yes for full details and No to exit")
        choice=take_command()
        if("yes".lower() in choice.lower()):
            speaker.Speak("Here are the full details : ")

            for key, value in wdict.items():
                take_command()
                print(value)
                speaker.Speak(value)
            break
        elif "no".lower() in choice.lower() :
            print("See u in Next Rain")
            speaker.Speak("See u in Next Rain")
            break
        else:
            print("Incorrect Option")
            speaker.Speak("Incorrect Option")


def openai_call(message):
    openai.api_key = apikey
    response = openai.Completion.create(
            model="text-curie-001",
            prompt= message,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    return response['choices'][0]['text']


def save_MongoDB(data,db,col):
    client = MongoClient(MongoDBURL, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    mydb = client[db]
    mycol = mydb[col]
    unique_id = str(uuid.uuid4())[0:13]
    while True:
        existing_doc = mycol.find_one({"unique_id": unique_id})
        if existing_doc:
            unique_id = str(uuid.uuid4())[0:13]
        else:
            break
    mycol.insert_one({"UID":unique_id,"User":"Fuzail","Time":datetime.datetime.now().strftime("%H:%M:%S"),"Response":data})
    

chatStr = ""
def chat():
    global chatStr
    while True:
        query=take_command()
        if "Quit" in query and chatStr :
            current_directory=os.getcwd()
            chatStr+='\n'+datetime.datetime.now().strftime("%H:%M:%S")
            if not os.path.exists(f"{current_directory}\Chatresponses"):
                os.mkdir(f"{current_directory}\Chatresponses")
            with open(f"{current_directory}\Chatresponses\myfile.txt","w") as s:
                s.write(chatStr)
                db = "Employee_Login"
                col = "AI_Chatting"
                save_MongoDB(chatStr,db,col)
               
    
            return
        chatStr += f"Fuzail: {query}\n Jarvis: "
        response=openai_call(chatStr)
        current_chat=""
        current_chat += f"Fuzail: {query}\n Jarvis: "
        
        # todo: Wrap this inside of a  try catch block
        chatStr += f"{response}\n"
        current_chat += f"{response}\n"
        print(current_chat)
        time.sleep(3)
        say(response)





def chatresponse(message):

    openai.api_key = (apikey)
    text=f"Response for Prompt : {message} \n ******************************************************\n\n"
    response = openai_call(message)
    text+=response
    current_directory=os.getcwd()
    if not os.path.exists(f"{current_directory}\AIresponses"):
        os.mkdir(f"{current_directory}\AIresponses")
    with open(f"{current_directory}\AIresponses\{''.join(message.lower().split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(text)
        
        db = "Employee_Login"
        col = "AI_Responses"
        save_MongoDB(text,db,col)
        
    
    return response

def play_Youtube_video():
    say("Enter the URL of the Youtube Video")
    url=input("Enter the URL of the Youtube Video")
    try:
        youtube = YouTube(url)

        video_stream = youtube.streams.get_highest_resolution()

        player = vlc.MediaPlayer(video_stream.url)
        print("Playing...")
        say("Playing...")
        player.play()
        while True:
            state = player.get_state()
            if state == vlc.State.Ended:
                break
    except :
        say("URL Error Occurrs")
        print("URL Error Occurrs")
        



def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Voice =  speaker.GetVoices().Item(1)
    speaker.Speak(text)

i=0
def take_command():
    global i
    # i=i+1
    if(i>3):
        return "Quit"
    return input()
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold=1
        print("Listining...")
        audio=r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You say : {query}")
            return query
        except Exception as e:
            return "Some error Occured.Sorry From Jarvis"

def bye():
    hour=time.strftime("%H")
    if int(hour)>=6 and int(hour)<=12  :
        print("Good Bye Sir... Have a Nice Day!")
        say("Good Bye Sir... Have a Nice Day!")
    elif int(hour)>12 and int(hour)<=18:
        print("Good Bye Sir... Have a Nice Evening!")
        say("Good Bye Sir... Have a Nice Evening!")
    elif  int(hour)>18 or int(hour)<6:
        print("Good Bye Sir... Good Night!")
        say("Good Bye Sir... Good Night!")


if __name__=="__main__":
    say("Welcome to Jarvis AI")
    while True:
        text=take_command()
        print(f"You say : {text}")
        say(f"You say : {text}")
        sites=[["Youtube","https://www.youtube.com"],["Wikipedia","https://www.wikipedia.org"],["google","https://www.google.com"],["instagram","https://www.instagram.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])
                time.sleep(10)

        if "Open Music".lower() in text:
            musicpath="G:\F\abc.xyz"
            os.system(f"start {musicpath}")
        elif "time".lower() in text:
            time=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir Time is {time}")
        elif "Intelligence".lower() in text.lower():
            print(chatresponse(text))
        elif "Youtube Video".lower() in text.lower():
            play_Youtube_video()
        elif "Jarvis Quit".lower() in text.lower():
            bye()
            exit()
        elif ("alarm".lower())  in text.lower():
            t1=threading.Thread(target=set_reminder,args=[text])
            t1.start()
            time.sleep(2)
        elif "reset chat".lower() in text.lower():
            chatStr = ""
        elif "weather".lower() in text.lower():
            weather(text.lower())
        elif "chatting".lower() in text.lower():
            print("Chatting...")
            chat()