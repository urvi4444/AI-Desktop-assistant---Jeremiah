# Desktop Voice Assistant

A Python-based desktop voice assistant similar to Siri and Alexa. This assistant can perform various tasks through voice commands.

## Features

- Voice recognition and text-to-speech capabilities
- Wikipedia searches
- YouTube video playback
- Web browsing
- Time information
- Weather updates
- Google searches
- Natural conversation interface

## Setup Instructions

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. For weather functionality, you'll need to:
   - Sign up for a free API key at OpenWeatherMap (https://openweathermap.org/api)
   - Replace `YOUR_API_KEY` in the code with your actual API key

3. Run the assistant:
   ```
   python assistant.py
   ```

## Voice Commands

Here are some example commands you can use:
- "Wikipedia [topic]" - Searches Wikipedia for the given topic
- "Open YouTube" - Opens YouTube in your default browser
- "Open Google" - Opens Google in your default browser
- "What's the time" - Tells you the current time
- "Weather in [city]" - Gives you the weather information for the specified city
- "Play [song name]" - Plays the specified song on YouTube
- "Search [query]" - Performs a Google search
- "Goodbye" or "Exit" - Closes the assistant

## Requirements

- Python 3.7 or higher
- Internet connection
- Microphone
- Speakers
