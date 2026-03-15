import os
import re
import nltk
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
import requests

# Load environment variables
load_dotenv()

# Setup external APIs
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="The Pitch Visualizer")

# Templates and static files
templates = Jinja2Templates(directory="templates")
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

def segment_text(text: str) -> List[str]:
    """Break text into sentences using NLTK."""
    try:
        sentences = nltk.sent_tokenize(text)
    except Exception:
        # Fallback simple split
        sentences = re.split(r'(?<=[.!?]) +', text)
    
    # Filter out empty or very short strings
    scenes = [s.strip() for s in sentences if len(s.strip()) > 5]
    return scenes

def refine_prompt(scene_text: str, style: str = "digital art") -> str:
    """Refine a simple sentence into a descriptive image prompt."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
                f"Convert this scene into a highly descriptive, artistic image generation prompt for AI: '{scene_text}'. "
                f"The style should be '{style}'. Focus on lighting, composition, and visual details. "
                "Keep the final output under 50 words and do not include the original text in your response."
            )
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini Refinement Error: {e}")
    
    # Simple fallback template
    return f"A visually striking {style} representation of: {scene_text}, cinematic lighting, detailed background, high resolution."

def generate_image(prompt: str) -> str:
    """Generate image using DALL-E 3 and return URL."""
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        # Return a placeholder if no key
        return f"https://placehold.co/1024x1024?text=Missing+OpenAI+Key"
    
    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"DALL-E Generation Error: {e}")
        return f"https://placehold.co/1024x1024?text=Generation+Error"

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def process_pitch(request: Request, text: str = Form(...), style: str = Form("digital art")):
    if not text:
        raise HTTPException(status_code=400, detail="Text input is required")
    
    # 1. Segmentation
    scenes = segment_text(text)
    if len(scenes) < 3:
        # If too short, we try to split by commas or just repeat for demonstration
        if len(scenes) == 1:
            scenes = [scenes[0], scenes[0], scenes[0]]
        elif len(scenes) == 2:
            scenes.append(scenes[0] + " " + scenes[1])
            
    # 2 & 3. Refinement and Generation
    storyboard = []
    for scene in scenes[:5]: # Limit to 5 scenes for efficiency
        refined = refine_prompt(scene, style)
        image_url = generate_image(refined)
        storyboard.append({
            "original_text": scene,
            "refined_prompt": refined,
            "image_url": image_url
        })
        
    return templates.TemplateResponse("storyboard.html", {
        "request": request,
        "storyboard": storyboard,
        "original_text": text,
        "style": style
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
