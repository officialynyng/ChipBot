```💾👺 ChipBot - Discord AI Bot 👺💾

📌 Overview

ChipBot is a Discord bot that interacts dynamically with users, offering sarcasm, analysis of YouTube videos and documents (PDF, TXT), and general conversational responses. It also integrates OpenAI for intelligent responses.

🛠️ Features

Chip AI Responses: Mentioning 'Chip' prompts a sarcastic AI response.

YouTube Video Analysis: Fetches video details (title, views, duration) and provides opinions.

Document Analysis: Processes and extracts text from PDFs and TXT files.

Random YouTube Videos: Generates a random YouTube video based on keywords or trends.

AI-Generated Opinions: Chip provides sarcastic analysis based on extracted text.


💥 Prerequisites

Python 3.10.10

pip (Python package manager)

Discord bot token
OpenAI API key
YouTube Data API key

💥 Clone the Repository

git clone https://github.com/your-repo/chipbot.git
cd chipbot

💥 Install Dependencies

pip install -r requirements.txt

If you encounter ModuleNotFoundError: No module named 'PyPDF2', install it manually:

pip install PyPDF2

🛠️ Setup

Create a .env file or set environment variables:

DISCORD_BOT_TOKEN=your_discord_token
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
DISCORD_CHANNEL_ID=your_channel_id

Run the bot:

python Chip.py

💥 General Commands

chip.analyze [YouTube Link/File] - Analyzes YouTube videos or documents (PDF, TXT).

chip.randomyoutube [optional keyword] - Fetches a random YouTube video.

chip.features - Lists ChipBot's features.

chip.help - Displays available commands.

💥 Example Interactions

🎥 YouTube Analysis

chip.analyze https://www.youtube.com/watch?v=example

Chip responds with:

📡 **Example Video Title**
100,000 views
Duration: 5m30s
https://www.youtube.com/watch?v=example
👺 **Chip’s Opinion:** This video is... well, let’s just say you could’ve picked a better one.

💥Just type Chip to trigger a sarcastic response!💥

👺 Verify API keys are correct.👺

👺 YouTube API Errors👺

Ensure your YouTube API key is valid and has YouTube Data API v3 enabled.

Free-tier API keys have rate limits—check quota usage in Google Cloud Console.

👺 Contributing👺

Pull requests are welcome! If you find a bug or have a feature request, open an issue.


██╗   ██╗███╗   ██╗██╗   ██╗███╗   ██╗ ██████╗ 
╚██╗ ██╔╝████╗  ██║╚██╗ ██╔╝████╗  ██║██╔════╝ 
 ╚████╔╝ ██╔██╗ ██║ ╚████╔╝ ██╔██╗ ██║██║  ███╗
  ╚██╔╝  ██║╚██╗██║  ╚██╔╝  ██║╚██╗██║██║   ██║
   ██║   ██║ ╚████║   ██║   ██║ ╚████║╚██████╔╝
   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
                                               
                                                                                                               
Developer: ynyng - ynyng LLC - ynyng@ynyng.org
