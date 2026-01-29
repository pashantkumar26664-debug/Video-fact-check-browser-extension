chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "EXTRACT_CONTENT") {

        const title = document.title;
        const text = document.body.innerText.slice(0, 8000);

        sendResponse({
            title: title,
            text: text
        });
    }
});
