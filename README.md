# Video-fact-check-browser-extension
# 🤖 AI Fact Checker & Summarizer (v1.0)

![Version](https://img.shields.io/badge/Version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-YouTube_Only-red.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📌 Overview
This project is a **Chrome Extension** powered by a **Python (Flask) Backend**. It allows users to summarize and fact-check videos instantly using Google's Gemini AI.

**⚠️ Current Scope (v1.0):**
This version is specifically engineered to work with **YouTube Videos** only. It relies on YouTube's closed captioning (CC) system to fetch data.

## 🚀 Features
- **One-Click Analysis:** Analyze any YouTube video directly from the browser popup.
- **Smart Summarization:** Generates concise 3-point bullet summaries.
- **Auto-Model Selection:** Automatically switches between `gemini-1.5-flash` and other models to ensure uptime.
- **Multi-Key Support:** Handles API limits by rotating keys (if configured).

## 🛠️ Tech Stack
- **Backend:** Python, Flask, YouTube Transcript API
- **AI Engine:** Google Gemini (1.5 Flash)
- **Frontend:** HTML, CSS, JavaScript (Chrome Extension Manifest V3)

## 🔮 Future Roadmap (v2.0 Ideas)
- [ ] Add support for generic websites (News articles, Blogs).
- [ ] Add "Chat with Video" feature.
- [ ] UI improvements for Dark Mode.

AI-Fact-Checker-Project/  (Main Folder)
│
├── server/               (Folder 1: सिर्फ Python फाइलों के लिए)
│   ├── app.py
│   ├── requirements.txt
│   └── (any other python scripts)
│
└── extension/            (Folder 2: सिर्फ Extension फाइलों के लिए)
    ├── manifest.json
    ├── popup.html
    ├── popup.js
    ├── content.js

## 📝 Installation
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API Key in `server/app.py`.
4. Load the `extension` folder in Chrome Developer Mode.

---
*Created by PRASHANT KUMAR*
