#  AI Robot Voice Assistant
## Robot

This project is a voice-controlled AI chatbot implemented in Python. The chatbot utilizes various libraries and APIs to perform tasks such as answering questions, opening websites, setting reminders, playing YouTube videos, providing weather information, and engaging in natural language conversation.

## Features
### Voice recognition:
The chatbot can understand and respond to voice commands using the speech_recognition library.
### Text-to-speech:
The chatbot can respond to user queries by converting text to speech with the win32com.client module.
#### Web browsing:
The chatbot can open websites using the webbrowser module.
### Reminders:
Users can set reminders with specific time units (hours, minutes, or seconds) using the set_reminder function.
### Weather information:
The chatbot can provide real-time weather information for various cities using the WeatherAPI.
### Chatting:
The chatbot uses the OpenAI GPT-3.5 Turbo model to engage in natural language conversation with users.
## Dependencies
Python 3.6+   
speech_recognition   
win32com.client   
webbrowser   
os   
datetime    
openai   
requests   
json   
geonamescache   
time   
re   
winsound   
win10toast    
pytube    
vlc  
## How to Use
1. Install the required dependencies by running the following command:
#### pip install -r requirements.txt
2. Obtain an API key from OpenAI and WeatherAPI and place them in the respective files (apikey.py and weatherapi.py).

3. Run the main.py script to start the voice assistant:
#### python main.py
Start interacting with the AI robot by speaking your queries. The robot will respond to your voice commands accordingly.
## Commands
"Open YouTube" - Opens YouTube in a web browser.  
"Open Wikipedia" - Opens Wikipedia in a web browser.  
"Open Google" - Opens Google in a web browser.   
"Open Instagram" - Opens Instagram in a web browser.  
"Open Music" - Opens a music file path (replace the path in the code).   
"What is the time?" - Returns the current time.  
"Intelligence" - Initiates a natural language conversation with the chatbot using the GPT-3.5 Turbo model.  
"Youtube Video" - Plays a YouTube video. Enter the URL when prompted.  
"Jarvis Quit" - Exits the voice assistant.  
"Set a reminder for 1 hour" - Sets a reminder for the specified time unit (hours, minutes, or seconds).  
"Weather in city_name" - Provides real-time weather information for the specified city.  
"Reset chat" - Clears the chat history.  
"Chatting" - Initiates an extended conversation with the chatbot.  
## Contributions
Contributions to this project are welcome. If you find any issues or want to add new features, feel free to open an issue or submit a pull request.
#### owner-mail:fuzailraza161@gmail.com

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
Special thanks to the developers and contributors of the open-source libraries and APIs used in this project. Their work made this project possible.