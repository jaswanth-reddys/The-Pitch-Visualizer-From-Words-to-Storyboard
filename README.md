# The Pitch Visualizer 🎨

The Pitch Visualizer is an AI-powered service that transforms narrative pitch text into a professional, multi-panel visual storyboard. By intelligently segmenting stories and using advanced prompt engineering, it brings abstract concepts to life through generated imagery.

## 🚀 Features

- **Text Segmentation**: Automatically breaks down complex narratives into logical scenes using NLTK.
- **AI-Powered Prompt Engineering**: Uses **Google Gemini 1.5 Flash** to "supercharge" text segments into highly descriptive, visually rich prompts.
- **Dynamic Image Generation**: Integrates with **OpenAI DALL-E 3** to generate unique, high-quality images for each scene.
- **Customizable Visual Styles**: Users can select from various artistic styles (Digital Art, Photorealistic, Sketch, etc.) to maintain consistency.
- **Modern Web UI**: A sleek, responsive dashboard built with **FastAPI** and **Tailwind CSS**.

---

## 🛠️ Setup & Execution

### 1. Prerequisites
- Python 3.9 or higher.
- API Keys for **OpenAI** (for DALL-E 3) and **Google Gemini** (for prompt refinement).

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. API Key Management
Create or update the `.env` file in the root directory with your keys:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 4. Initialize NLTK
Run the setup script to download required linguistic models:
```bash
python setup_nltk.py
```

### 5. Launch the Application
Start the FastAPI server:
```bash
python main.py
```
Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

Open your browser and navigate to `http://localhost:8000`.

---

## 🎨 Methodology & Design Choices

### Narrative Segmentation
We utilize the **NLTK (Natural Language Toolkit)** sentence tokenizer to identify key moments in the pitch. This ensures each panel represents a distinct part of the story while maintaining narrative flow.

### Intelligent Prompt Engineering (Bonus Implementation)
Instead of feeding raw sentences to the image generator, we use a secondary LLM (**Gemini 1.5 Flash**) as a "Creative Director." It translates simple sentences into complex visual descriptions, specifying lighting, composition, and texture. This significantly improves the quality and consistency of the generated storyboard.

### Visual Consistency
By appending a consistent style descriptor (e.g., "Photorealistic Cinematic Lighting") to every refined prompt, we ensure that the storyboard feels like a coherent sequence rather than a collection of random images.

---

## 🧩 Technical Stack

- **Backend**: FastAPI (Python)
- **NLP**: NLTK (Sentence Tokenization)
- **Refinement LLM**: Google Gemini 1.5 Flash
- **Image Generation**: OpenAI DALL-E 3
- **Frontend**: Jinja2 Templates + Tailwind CSS
- **Environment**: python-dotenv

---

*Transform your pitch. Visualize your success.*
