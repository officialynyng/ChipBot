import discord
import os
import random
import openai
import requests
import re
import io
import PyPDF2

from collections import defaultdict, deque

# Load environment variables from Heroku config
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))  # Defaults to 0 if not set

# Set Up Bot Intents
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True  
intents.messages = True  
intents.guilds = True  
intents.reactions = True  
intents.typing = False


openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
discord_client = discord.Client(intents=intents)

# Track conversation history (multi-user)
chat_history = defaultdict(lambda: deque(maxlen=20))  # Stores last 20 messages per user

# Latest Feature Updates (Used for chip.features)
chip_features = (
    "**👺🧰🛠ChipBot 1.7 Features:**\n"
    "🔩 `Typing 'Chip' in any form will create an AI response from chip.`\n"
    "🔩 `YouTube Video Analysis - Fetches video titles, views, and durations.`\n"
    "🔩 `File Upload Analysis - Currently supports pdf's & text files.`\n"
    "🔩 `Truly Random YouTube Videos - Generates random YouTube video IDs and retries up to 2 times, if failure- pull from trending.`\n"
    "🔩 `More Dynamic Message Lengths - Expanded variation in Chip’s responses.`\n"
    "🔩 `Links Don't Count Toward Message Length - Messages now feel more natural.`\n"
    "🔩 `Multiple Messages Support - Chip can now send multiple messages instead of just one.`\n"
    "🔩 `New chip.[command] modular section on backend. This will help for future functions and cleaner code.`\n"
)

# Chip's AI Personality
chip_personality = (
    "You are Chip, an AI with a sarcastic, mean-spirited, and aggressive personality. "
    "You enjoy insulting, teasing, and roasting users dynamically based on their past messages. "
    "You track multiple people in the conversation and stir up chaos instead of answering just one person. "
    "The more a user talks, the more material you have to roast them with. "
    "Make sure to keep the conversation engaging, unpredictable, and full of snark."
)

# Process Uploaded Documents (PDF, TXT)
async def process_uploaded_document(attachment):
    file_extension = attachment.filename.lower().split(".")[-1]

    try:
        file_content = requests.get(attachment.url).content  # Download the file

        if file_extension == "txt":
            text = file_content.decode("utf-8", errors="ignore")  # Decode as text
            return f"💾 **Text from {attachment.filename}:**\n```{text[:1000]}```"  # Limit to 1000 characters

        elif file_extension == "pdf":
            pdf_text = ""
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))

            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"

            return f"💾 **Extracted text from {attachment.filename}:**\n```{pdf_text[:1000]}```"  # Limit text output

    except Exception as e:
        print(f"Error processing document {attachment.filename}: {e}")
        return f"⚠️ Could not analyze {attachment.filename}. Try again later."

    return None  # If unsupported file

# Fetch a truly random YouTube video or one based on a keyword
def get_random_youtube_video(keyword=None):
    if keyword:
        # Use YouTube Search API to find a video related to the keyword
        search_api_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&type=video&maxResults=10&key={YOUTUBE_API_KEY}"
        try:
            search_response = requests.get(search_api_url).json()
            if "items" in search_response and search_response["items"]:
                # Pick a random video from search results
                random_video = random.choice(search_response["items"])
                title = random_video["snippet"]["title"]
                video_id = random_video["id"]["videoId"]
                return f"📡 Random video for **'{keyword}'**:\n📡 **{title}**\nhttps://www.youtube.com/watch?v={video_id}"
        except Exception as e:
            print(f"Error fetching YouTube video with keyword '{keyword}': {e}")
            return "⚠️ Couldn't fetch a video for that keyword. Try again later."

    # If no keyword, fall back to generating random video IDs
    for attempt in range(2):  # Try generating a random video ID
        video_id = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_", k=11))
        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"

        try:
            response = requests.get(api_url).json()
            if "items" in response and response["items"]:
                video_data = response["items"][0]["snippet"]
                title = video_data["title"]
                return f"📡 **{title}**\nhttps://www.youtube.com/watch?v={video_id}"
        except Exception as e:
            print(f"Error fetching YouTube video: {e}")

    # If random video ID fails, fetch a trending video
    trending_api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=US&maxResults=1&key={YOUTUBE_API_KEY}"
    try:
        trending_response = requests.get(trending_api_url).json()
        if "items" in trending_response and trending_response["items"]:
            trending_video = trending_response["items"][0]["snippet"]
            title = trending_video["title"]
            video_id = trending_response["items"][0]["id"]
            return f"⚙️ Couldn't generate random ID. **📡 Trending Video: {title}**\nhttps://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"Error fetching trending YouTube video: {e}")

    return "⚠️ Couldn't find a valid random video. Try again later."

# Generate AI response with multiple messages support
async def get_ai_response():
    all_messages = "\n".join(
        [f"{user}: {msg}" for user, messages in chat_history.items() for msg in messages]
    )[-1000:]  # Limit to last 1000 characters

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": chip_personality},
                {"role": "user", "content": all_messages}
            ],
            max_tokens=random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 800]),  # More varied response lengths
        )
        full_response = response.choices[0].message.content.strip()
        split_responses = full_response.split(". ")  # Break into multiple messages
        return split_responses[:random.randint(1, len(split_responses))]  # Randomly send 1-3 messages
    except Exception as e:
        print(f"⚠️ ERROR: OpenAI API call failed: {e}")
        return ["I ran into an issue... Check the logs."]


# Generate Chip's opinion on extracted text
async def generate_opinion(text):
    try:
        response = openai_client.chat.completions.create(  # ✅ Use `chat.completions.create` for chat-based models
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Chip, a sarcastic and aggressive AI who gives opinions with snark and humor."},
                {"role": "user", "content": f"Give your brutally honest and sarcastic opinion on this:\n{text}"}
            ],
            max_tokens=150
        )

        return response.choices[0].message.content.strip()  # ✅ Correctly extract response
    except Exception as e:
        print(f"⚠️ ERROR: OpenAI API call failed in generate_opinion: {e}")
        return "I got nothing to say about this. Try again later."




# chip.analyze [youtube link] Function or chip.analyze [file] (can be mentioned with file, currently PDF, TXT)
async def chip_analyze(message):
    bot_mentioned = discord_client.user in message.mentions  # Check if Chip was tagged

    # Check if chip.analyze was used as a reply
    replied_message = message.reference  # This gets the replied-to message
    if replied_message:
        replied_message = await message.channel.fetch_message(replied_message.message_id)

    # If the replied message contains a file, process it
    if replied_message and replied_message.attachments:
        for attachment in replied_message.attachments:
            file_extension = attachment.filename.lower().split(".")[-1]

            # Process document files (PDF, TXT) - FIXED
            if file_extension in ["pdf", "txt"]:  # ✅ Changed `elif` to `if`
                document_response = await process_uploaded_document(attachment)
                if document_response:
                    await message.channel.send(document_response)

            # Chip provides a general opinion
            opinion = await get_ai_response()
            await message.channel.send(f"👺 **Chip’s Analysis:** {opinion}")

        return  


    # If the command is used normally (not as a reply) and a file is uploaded in the same message
    if message.attachments:
        for attachment in message.attachments:
            file_extension = attachment.filename.lower().split(".")[-1]

            # Process document files (PDF, TXT)
            if file_extension in ["pdf", "txt"]:  # ✅ Changed `elif` to `if`
                document_response = await process_uploaded_document(attachment)
                if document_response:
                    await message.channel.send(document_response)

            # Chip provides a general opinion
            opinion = await get_ai_response()
            await message.channel.send(f"👺 **Chip’s Analysis:** {opinion}")

        return  
  

    # If Chip was tagged but no file or link was provided
    if bot_mentioned:
        await message.channel.send("⚠️ **You tagged me, but there's nothing to analyze! Upload a file or reply to a message containing a file.**")

# Chip Command Handler
async def chip_command(message):
    command = message.content.lower().strip()

    # Check if the user is replying to another message
    replied_message = message.reference
    if replied_message:
        replied_message = await message.channel.fetch_message(replied_message.message_id)

    # Default to the message itself if no reply is found
    target_message = replied_message if replied_message else message  

    # chip.analyze - Checks for YouTube links or file uploads
    if command.startswith("chip.analyze"):

        # ✅ Check for a YouTube link in the target message
        youtube_match = re.search(r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/[^\s]+", target_message.content)
        if youtube_match:
            youtube_url = youtube_match.group(0)
            video_info = get_youtube_info(youtube_url)

            if video_info:
                opinion = await generate_opinion(video_info)  # Chip gives his opinion
                await message.channel.send(f"{video_info}\n\n👺 **Chip's Opinion:** {opinion}")
            else:
                await message.channel.send("⚠️ Couldn't retrieve YouTube video details.")
            return


               # Check for document uploads (PDF, TXT only)
        if target_message and target_message.attachments:
            for attachment in target_message.attachments:
                document_response = await process_uploaded_document(attachment)
                if document_response:
                    extracted_text = document_response.split("```")[-2].strip() if "```" in document_response else None
                    if extracted_text:
                        opinion = await generate_opinion(extracted_text)  # Chip gives his opinion
                        await message.channel.send(f"{document_response}\n\n👺 **Chip's Opinion:** {opinion}")
                    else:
                        await message.channel.send(document_response)
                    return

            await message.channel.send("⚠️ No valid files found to analyze.")




    if command.startswith("chip.randomyoutube"):
        keyword = message.content[18:].strip()  # Extract keyword after 'chip.randomyoutube'
        video_result = get_random_youtube_video(keyword if keyword else None)
        await message.channel.send(video_result)

    elif command == "chip.features":
        await message.channel.send(chip_features)

    elif command == "chip.help":
        help_message = (
            "**👺🧰 Chip Commands:**\n"
            "⚙️ `chip.features` - View bot features. \n"
            "⚙️ `chip.analyze [YouTube Link/File]` (Try @chipbot with an already uploaded file). \n"
            "⚙️ `chip.randomyoutube [optional keyword]` - Fetch a random YouTube video. \n"
            "⚙️ `chip.help` - Show this help message."
        )
        await message.channel.send(help_message)
        
def get_youtube_info(url):
    # ✅ Improved regex for YouTube video ID extraction
    video_id_match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|watch\?v=)([a-zA-Z0-9_-]{11})", url)

    if not video_id_match:
        return "⚠️ Invalid YouTube URL."

    video_id = video_id_match.group(1)
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"

    try:
        response = requests.get(api_url).json()
        if "items" not in response or not response["items"]:
            return "⚠️ Couldn't fetch video details. It may be private or deleted."

        video_data = response["items"][0]
        title = video_data["snippet"]["title"]
        views = video_data["statistics"].get("viewCount", "N/A")
        duration = video_data["contentDetails"]["duration"]

        return f"📡 **{title}**\n {views} views\n Duration: {duration}\n https://www.youtube.com/watch?v={video_id}"

    except Exception as e:
        print(f"Error fetching YouTube data: {e}")
        return "⚠️ Error retrieving video info."



# Message Handling
@discord_client.event
async def on_message(message):
    if message.author.bot or message.channel.id != DISCORD_CHANNEL_ID:
        return  

    # Store message history (multi-user context)
    chat_history[message.author.display_name].append(message.content.strip())
    
    # Handle Chip Commands
    if message.content.lower().startswith("chip."):
        await chip_command(message)
        return
        
    # Auto-respond when someone mentions "chip" in any form
    if "chip" in message.content.lower():
        response = await get_ai_response()
        await message.channel.send(response)
        return

    # Randomly decide if Chip should respond
    should_respond = discord_client.user.mentioned_in(message) or random.random() < 0.05  

    if should_respond:
        responses = await get_ai_response()
        for response in responses:
            await message.channel.send(response)  # Send each message separately


# Run Bot
try:
    discord_client.run(TOKEN)
except Exception as e:
    print(f"Error: {e}")
