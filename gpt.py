import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import openai
import pyttsx3
import speech_recognition as sr
import threading
import time

# Set up your OpenAI API credentials
openai.api_key = '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'

# Set up the log file
log_file = open("chat_log.txt", "a")

# Load avatar images
avatar_closed_img = Image.open("maybe1.png")
avatar_open_img = Image.open("maybe2.png")

# Set up the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('volume', 0.8)  # Adjust the volume (default is 1)

# Set up the speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Variable to control speech speed
speech_speed = 150

def recognize_speech():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_message = recognizer.recognize_google(audio)
        return user_message
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def send_message():
    global log_file
    user_message = user_input.get("1.0", tk.END).strip()

    # Append the user message to the chat history
    chat_history.append(user_message)

    # Log the user's input
    log_file.write("User: " + user_message + "\n")

    # Check if the user asked for the chatbot's name
    if user_message.lower() == "what's your name?" or user_message.lower() == "what is your name?":
        reply = "my name is john"
    else:
        # Generate a response from the chatbot
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=' '.join(chat_history),
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )

        # Extract the reply from the response
        reply = response.choices[0].text.strip()

    # Append the chatbot's reply to the chat history
    chat_history.append(reply)

    # Display the chatbot's reply in the conversation area
    conversation_area.insert(tk.END, "Chatbot: " + reply + "\n")

    # Speak the chatbot's reply
    speak(reply)

    # Clear the user input field
    user_input.delete("1.0", tk.END)

def new_chat():
    global log_file
    # Clear the conversation area and user input field
    conversation_area.delete("1.0", tk.END)
    user_input.delete("1.0", tk.END)

    # Reset the chat history
    chat_history.clear()

    # Close the log file
    log_file.close()

    # Open a new log file
    log_file = open("chat_log.txt", "a")

def speak(text):
    # Use the text-to-speech engine to speak the text
    engine.say(text)
    engine.runAndWait()

def handle_voice_input():
    user_message = recognize_speech()
    if user_message:
        user_input.delete("1.0", tk.END)
        user_input.insert(tk.END, user_message)
        send_message()

def listen_and_respond():
    while True:
        user_message = recognize_speech()
        if user_message:
            user_input.delete("1.0", tk.END)
            user_input.insert(tk.END, user_message)
            send_message()

# Create the main window
root = tk.Tk()
root.title("Chatbot")

# Load avatar images
avatar_closed = avatar_closed_img.resize((100, 100))
avatar_closed_tk = ImageTk.PhotoImage(avatar_closed)

avatar_open = avatar_open_img.resize((100, 100))
avatar_open_tk = ImageTk.PhotoImage(avatar_open)

# Create the avatar label
avatar_label = tk.Label(root, image=avatar_closed_tk)
avatar_label.pack()

# Create the conversation area
conversation_area = scrolledtext.ScrolledText(root, width=50, height=20)
conversation_area.pack()

# Create the user input field
user_input = tk.Text(root, width=50, height=3)
user_input.pack()

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Create the new chat button
new_chat_button = tk.Button(root, text="New Chat", command=new_chat)
new_chat_button.pack()

# Create the voice input button
voice_input_button = tk.Button(root, text="Speak", command=handle_voice_input)
voice_input_button.pack()

# Set up the chat conversation
chat_history = []

# Start listening for voice input in a separate thread
threading.Thread(target=listen_and_respond, daemon=True).start()

# Start the Tkinter event loop
root.mainloop()
