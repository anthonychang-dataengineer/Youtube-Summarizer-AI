import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from anthropic import Anthropic

#set up env and api
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

url = "https://www.youtube.com/watch?v=DbD51qxdts8"

#Extract video ID
video_id = url.split('v=')[1]

#Fetch transcript
try:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    #Print one big string
    full_text = " ".join([subtitle_line.text for subtitle_line in transcript.snippets])
    
    prompt = f"Summarize this Youtube video transcript in this format: "\
                f"TDLR at the beginning, including a 'WHY THIS MATTERS TO YOU' section, then a Listicle format highlightng import observations and key points. If it's there's a technical aspect, explain how it was done."\
                f"and at the bottom, the conclusion/takeaway the video ends in (don't bother with things like promotions or advertisements):"\
                f"\n\n{full_text}"
    #print(prompt)
    #Call Claude API
    client = Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    print(message.content[0].text)
except Exception as e:
    print(f"Error: {e}")