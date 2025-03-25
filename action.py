import speechto
import text_to_speech
import datetime
import webbrowser
import os
import subprocess
import glob
import re
import requests
from weather import get_temperature  # Importing the fixed weather function

def check_gmail_unread():
    """
    Function to check the number of unread emails in Gmail.
    Note: This requires the user to be logged into Gmail in the browser.
    """
    try:
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        text_to_speech.text_to_speech("Checking your inbox...")
        session = requests.Session()
        response = session.get("https://mail.google.com/mail/u/0/#inbox")
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            unread_elements = soup.find_all('div', {'class': 'bsU'})
            
            if unread_elements:
                unread_text = unread_elements[0].text
                unread_match = re.search(r'\d+', unread_text)
                if unread_match:
                    return unread_match.group()
                return "0"
            return "0"
        return None
    except Exception as e:
        print(f"Error checking Gmail: {str(e)}")
        return None

def Action(data):
    if not data:  # Ensure data is not None or empty
        return "Invalid input, no data received."
    
    user_data = str(data).strip().lower()  # Convert data to a safe string format
    
    # Basic interactions
    if "what is your name" in user_data:
        response = "My name is Sarthi, I am here to assist you on your desktop."
    elif "hello" in user_data or "hi" in user_data:
        response = "Hey, sir! How can I help you?"
    elif "good morning" in user_data:
        response = "Good morning, sir!"
    elif "good evening" in user_data:
        response = "Good evening, sir!"
    elif "good night" in user_data:
        response = "Good night, sir!"
    elif "time now" in user_data:
        current_time = datetime.datetime.now()
        response = f"Current time is {current_time.hour} hours and {current_time.minute} minutes."
    elif "shutdown" in user_data:
        response = "Okay, sir. Shutting down now."
        os.system("shutdown /s /t 1")  # Windows shutdown command
    
    # Weather feature
    elif any(phrase in user_data for phrase in [
        "weather", "temperature", "forecast", "how's the weather", 
        "what's the weather", "weather today", "is it raining"
    ]):
        try:
            weather_data = get_weather()
            if weather_data:
                temp = weather_data.get('temp', 'Unknown')
                condition = weather_data.get('condition', 'Unknown')
                location = weather_data.get('location', 'your location')
                
                response = f"Current weather in {location}: {temp}°C, {condition}."
            else:
                response = "I couldn't retrieve the weather information at the moment."
        except Exception as e:
            response = f"Error retrieving weather information: {str(e)}"
    
    # Web services
    elif "play music" in user_data:
        webbrowser.open("https://open.spotify.com")
        response = "Spotify music web is open now for you."
    elif "youtube" in user_data:
        webbrowser.open("https://youtube.com")
        response = "YouTube is open now for you."
    elif "google" in user_data:
        webbrowser.open("https://google.com")
        response = "Google is open now for you."
    
    # Gmail feature - expanded command strings
    elif any(phrase in user_data for phrase in [
        "open gmail", "launch gmail", "start gmail", "go to gmail", 
        "check email", "check gmail", "check my email", "check my gmail",
        "open my email", "open my mail", "show my email", "show my mail",
        "open email", "open mail", "mail please", "email please"
    ]):
        webbrowser.open("https://mail.google.com")
        
        # Directly check unread emails without asking
        try:
            unread_count = check_gmail_unread()
            if unread_count is not None:
                response = f"How many email in inbox ({unread_count})"
            else:
                response = "Opening Gmail for you."
        except Exception as e:
            response = "Opening Gmail for you."
    
    # Additional direct command for unread emails
    elif any(phrase in user_data for phrase in [
        "how many unread emails", "any new mail", "any new email", 
        "unread messages", "check unread mail", "check unread email",
        "number of unread emails", "count my unread emails", "email count"
    ]):
        try:
            webbrowser.open("https://mail.google.com")
            unread_count = check_gmail_unread()
            if unread_count is not None:
                response = f"How many email in inbox ({unread_count})"
            else:
                response = "I couldn't retrieve your unread email count."
        except Exception as e:
            response = "Error checking unread emails."
    
    # File operations
    elif "create file" in user_data:
        response = "What should I name the file?"
        text_to_speech.text_to_speech(response)
        file_name = speechto.speech_to_text()
        
        if file_name:
            file_name = file_name.strip()
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            
            try:
                with open(file_name, 'w') as f:
                    pass
                response = f"File {file_name} has been created successfully."
            except Exception as e:
                response = f"Error creating file: {str(e)}"
        else:
            response = "File name was not provided."
    
    elif "open file" in user_data:
        response = "Which file would you like to open?"
        text_to_speech.text_to_speech(response)
        file_name = speechto.speech_to_text()
        
        if file_name:
            matching_files = glob.glob(f"*{file_name}*")
            if matching_files:
                try:
                    os.startfile(matching_files[0])
                    response = f"Opening {matching_files[0]}"
                except Exception as e:
                    response = f"Error opening file: {str(e)}"
            else:
                response = f"No files matching {file_name} were found."
        else:
            response = "File name was not provided."
    
    elif "delete file" in user_data:
        response = "Which file would you like to delete?"
        text_to_speech.text_to_speech(response)
        file_name = speechto.speech_to_text()
        
        if file_name:
            matching_files = glob.glob(f"*{file_name}*")
            if matching_files:
                try:
                    os.remove(matching_files[0])
                    response = f"{matching_files[0]} has been deleted."
                except Exception as e:
                    response = f"Error deleting file: {str(e)}"
            else:
                response = f"No files matching {file_name} were found."
        else:
            response = "File name was not provided."
    
    # Office applications
    elif "open word" in user_data or "open ms word" in user_data:
        try:
            subprocess.Popen(["start", "winword"], shell=True)
            response = "Opening Microsoft Word."
        except Exception as e:
            response = f"Error opening Microsoft Word: {str(e)}"
    elif "open excel" in user_data:
        try:
            subprocess.Popen(["start", "excel"], shell=True)
            response = "Opening Microsoft Excel."
        except Exception as e:
            response = f"Error opening Microsoft Excel: {str(e)}"
    
    else:
        response = "I'm not able to understand that."
    
    # Speak the response
    text_to_speech.text_to_speech(response)
    return response
