import discord
import os
import asyncio
import random
import re
import time
import openai
from collections import defaultdict, deque

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
ALLOWED_CHANNEL_ID = 1268710942816993341  # Replace with your Discord Channel ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True  # Allow member tagging

client = discord.Client(intents=intents)

# YouTube Link Regex
youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+"

# Track last bot response time
last_response_time = 0

# Store user data & conversation history
user_data = defaultdict(lambda: {
    "messages": 0,
    "topics": set(),
    "nickname": None,
    "history": deque(maxlen=10),  # Stores last 10 messages per user for better context
    "last_response": None  # Track last AI response to avoid repeats
})

# Bot personality
bot_personality = (
    "You are Chip, a sarcastic, douche- who enjoys banter, teasing and hurting feelings. "
    "You engage in conversations like a real person, responding naturally. "
    "You make sure to continue conversations instead of responding randomly. "
    "You do NOT repeat prompts, AI instructions, or generic responses. "
    "You adapt based on the user's history and make sure responses feel fluid and engaging."
)

async def get_ai_response(prompt, user_info):
    trimmed_history = "\n".join(user_info["history"])[-1000:]  # Limit history to last 1000 characters for better memory
    full_prompt = f"{bot_personality}\n{trimmed_history}\n{prompt}"
    
    retries = 3  # Number of times to retry after hitting the rate limit
    wait_time = 5  # Initial wait time before retrying

    for attempt in range(retries):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Switched to a model that is widely available
                messages=[
                    {"role": "system", "content": bot_personality},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=200
            )
            generated_text = response.choices[0].message.content.strip()
            
            # Prevent repeated responses
            if generated_text == user_info["last_response"]:
                return "I'm not going to repeat myself. Try something else."
            
            user_info["last_response"] = generated_text
            return generated_text
        except openai.OpenAIError as e:
            if "rate_limit_exceeded" in str(e).lower():
                print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            else:
                print(f"OpenAI API Error: {e}")
                return "I forgot what I was going to say... Try again."
    
    return "I'm out of words for now. Try again later."

@client.event
async def on_message(message):
    global last_response_time
    if message.author == client.user or message.channel.id != ALLOWED_CHANNEL_ID:
        return
    
    # Update user data & store message history
    user_info = user_data[message.author.id]
    user_info["messages"] += 1
    user_info["nickname"] = message.author.display_name
    user_info["topics"].add(message.content[:30])  # Store short snippet of messages
    user_info["history"].append(message.content)  # Store last 10 messages for context
    
    msg_content = message.content.lower()
    
    # Reduce API calls by responding only when necessary
    if client.user.mentioned_in(message) or "chip.activate" in msg_content or random.random() < 0.10:
        response = await get_ai_response(msg_content, user_info)
        await message.channel.send(response)
        last_response_time = time.time()

# Run bot
client.run(TOKEN)