#!conf_env/bin/activate
import asyncio
from telethon import TelegramClient
import re
from gtts import gTTS
import os
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
LDR_PIN = 15  # Example: physical pin 15 (GPIO 22)

# Replace these with your own values from my.telegram.org
API_ID = 20321967
API_HASH = "37cea172df34a5aaa44fa1e47d030545"


def text_to_speech_offline(text):

    tts = gTTS(text, lang='ru')
    tts.save("output.mp3")
    os.system("mpv output.mp3")

    return 0
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty("rate", 100)  # Speed of speech
    engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)

    # Russian voice (if available)
    voices = engine.getProperty("voices")
    for voice in voices:
        print (voice.name.lower())
        if "russian" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    engine.say(text)
    engine.runAndWait()


def clean_text(text):
    # Extract the number following '#'
    hash_number = re.search(r"#(\d+)", text)
    hash_num = hash_number.group(0) if hash_number else ""

    # Remove all hyperlinks (URLs)
    text_no_links = re.sub(r"https?://\S+|\(https?://\S+\)|\[.*?\]", "", text)

    # Remove the extracted hash number from the text if it was found
    if hash_num:
        text_no_links = text_no_links.replace(hash_num, "").strip()

    # Combine the hash number and cleaned text
    result = f"{hash_num} {text_no_links}" if hash_num else text_no_links

    # Clean up any extra spaces
    result = " ".join(result.split())

    result = result.rsplit (' ', 1)[0]
    return result

async def fetch_random_message(client, channel, max_messages=1000):
    # Pick a random offset (1 to 10,000)
    random_offset = random.randint(0, max_messages - 1)
    
    # Fetch a single message at the random offset
    cnt = 0
    async for message in client.iter_messages(channel, limit=1000):
        cnt+=1
        if (cnt == random_offset): 
            return message
    return None


async def main():
    async with TelegramClient("session_name", API_ID, API_HASH) as client:
        # Get channel input from user
        channel_input = -1002058884491

        try:
            channel = await client.get_entity(channel_input)
        except ValueError:
            print("Could not find the channel. Check the input and try again.")
            return

        print(f"\nFetching messages from: {channel.title}\n")

        # Counter for messages
        message_count = 0

        while message_count < 3:
            message = await fetch_random_message(client, channel)
            
            if message:
                print("-" * 50)
                print(f"Random Message (ID: {message.id}):")
                print(f"Date: {message.date}")
                clen_text = clean_text (message.text)
                print(f"Content: {clen_text}\n")
                text_to_speech_offline (clen_text)
                message_count+=1
            else:
                print("No message found at this offset.")

        print(f"Total messages retrieved: {message_count}")

        return 0
        # Iterate through all messages in the channel
        async for message in client.iter_messages(channel):
            message_count += 1
            print(f"Message {message_count}:")
            print(f"Date: {message.date}")
            clen_txt = clean_text(message.text)
            print(f"Content: {clen_txt}\n")
            text_to_speech_offline(clen_txt)
            print("-" * 50 + "\n")
            if message_count >= 2:
                break



if __name__ == "__main__":
    asyncio.run(main())
