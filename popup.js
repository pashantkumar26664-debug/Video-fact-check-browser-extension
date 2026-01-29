/*
  popup.js
  This script handles the user interaction in the extension popup.
  It fetches the current tab URL and sends it to our local Python server.
*/

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const statusText = document.getElementById('status');
    const resultText = document.getElementById('result');
    
    // UI Feedback: Show loading state
    statusText.textContent = "Processing... (Connecting to Brain)";
    resultText.textContent = "";

    try {
        // 1. Get the current active tab URL
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        let videoUrl = tab.url;

        // Check if it's actually a YouTube video
        if (!videoUrl.includes("youtube.com/watch")) {
            statusText.textContent = "❌ Please open a YouTube Video first.";
            return;
        }

        // 2. Send the URL to our Python Server (localhost:5000)
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: videoUrl })
        });

        // 3. Handle the response
        const data = await response.json();
        
        statusText.textContent = "✅ Analysis Complete:";
        
        // Show result (Support Markdown-style bullet points if needed, but simple text for now)
        resultText.innerText = data.analysis;

    } catch (error) {
        console.error("Connection Error:", error);
        statusText.textContent = "❌ Error: Is the Python Server running?";
        resultText.textContent = "Make sure you ran 'python app.py' in the terminal.";
    }
});