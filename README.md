Chip - Discord AI Bot - Configured for Heroku

A sarcastic, witty AI bot that remembers user interactions, engages in natural conversations, and provides dynamic responses. 🚀 Features

Conversational Memory: Remembers the last 10 messages per user for better replies.
Adaptive Responses: Adjusts tone based on message history and user activity.
No Repetitions: Avoids repeating itself in conversations.
Rate Limit Handling: Implements retry logic to avoid OpenAI API rate limits.
YouTube Link Detection: Recognizes YouTube links (future feature).

🤖 How It Works

Mention @Chip or type "chip.activate"` to trigger a response.
Chip will randomly reply (10% chance) even when unprompted.
If OpenAI API limits are hit, the bot retries with exponential backoff.
Remembers recent user messages for better engagement.

🛠 Troubleshooting

OpenAI API Rate Limits

The bot automatically waits and retries if it hits rate limits.
If it keeps failing, upgrade your OpenAI plan or reduce API calls.

Bot Not Responding?

Ensure the bot is in the correct Discord channel.



Credits

                                
```██    ██ ███    ██ ██    ██ ███    ██  ██████```  
```██  ██  ████   ██  ██  ██  ████   ██ ██```       
  ```████   ██ ██  ██   ████   ██ ██  ██ ██   ███``` 
   ```██    ██  ██ ██    ██    ██  ██ ██ ██    ██``` 
   ```██    ██   ████    ██    ██   ████  ██████```  
                                               
                                                                                                               
Developer: ynyng - ynyng LLC - ynyng@ynyng.org
Powered by: OpenAI API, Python, and Discord.py
