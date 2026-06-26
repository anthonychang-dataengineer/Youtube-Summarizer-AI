import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from anthropic import Anthropic
import requests#for transcript api

#set up env and api
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
transcript_api_key = os.getenv("TRANSCRIPT_API_KEY")
app = FastAPI()

class SummarizeRequest(BaseModel):
    youtubeUrl:str

#waits and listens for a request coming in from somewhere over the internet. In this case my phone
@app.post("/api/summarize")
#This is the function that runs when it's called
async def summarize(request: SummarizeRequest):
    #url = "https://www.youtube.com/watch?v=DbD51qxdts8"

    #Fetch transcript
    try:
        #Extract video ID
        if 'youtu.be/' in request.youtubeUrl:#this is using google chrom youtube url on iphone
            video_id = request.youtubeUrl.split('youtu.be/')[1].split('?')[0]
        elif 'youtu.be/' in request.youtubeUrl:#this is using google chrom youtube url on iphone
            video_id = request.youtubeUrl.split('youtu.be/')[1].split('?')[0]
        elif 'v=' in request.youtubeUrl:#this is using a desktop youtube url
            video_id = request.youtubeUrl.split('v=')[1]
        

        #ytt_api = YouTubeTranscriptApi()
        #transcript = ytt_api.fetch(video_id)

        transcript_response = requests.get(
            "https://transcriptapi.com/api/v2/youtube/transcript",
            params={"video_url": video_id}, 
            headers={"Authorization": f"Bearer {transcript_api_key}"}
        )
        #Parse response to json
        transcript_json = transcript_response.json()
        #extract the transcript array
        transcript_array = transcript_json['transcript']
        #print(transcript_array)
        #Print one big string
        full_text = " ".join([item['text'] for item in transcript_array])
        
        prompt = "Summarize this Youtube video transcript in this format: "\
                    "Give it your best guess of the title"\
                    "TDLR at the beginning, including a 'WHY THIS MATTERS TO YOU' section, then a Listicle format highlightng import observations and key points. If it's there's a technical aspect, explain how it was done."\
                    "and at the bottom, the conclusion/takeaway the video ends in (don't bother with things like promotions or advertisements):"\
                    f"\n\n{full_text}"
        #print(prompt)
        #Call Claude API
        client = Anthropic()
        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        summary = message.content[0].text
        return summary
    except Exception as e:
        return {"Error": str(e)}