# AI-Powered YouTube Summarizer 🎥🤖

An interactive **Streamlit web app** that extracts transcripts from YouTube videos and generates **AI-powered summaries** using the **LangChain + Ollama** framework. This tool helps you quickly understand long videos by condensing their transcripts into concise summaries.

---

## 🚀 Features

* **Transcript Extraction**: Fetch transcripts from YouTube videos (English supported).
* **Smart Summarization**: Generate structured summaries using `llama3.2:1b` through LangChain.
* **Chunked Summarization**: Handles long transcripts by splitting them into chunks for better summarization quality.
* **Interactive UI**: Clean and modern interface built with Streamlit, featuring dark mode styling.
* **Error Handling**: Graceful error messages for videos without captions or invalid URLs.

---

## 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/) – for the interactive web interface
* [LangChain](https://www.langchain.com/) – for LLM-based summarization workflows
* [Ollama](https://ollama.ai/) – local LLM serving (Llama 3.2 1B in this case)
* [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/) – for transcript extraction

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jokhioyousif/youtube-summarizer.git
   cd youtube-summarizer
   ```

2. Create a virtual environment & install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:

   ```txt
   streamlit
   youtube-transcript-api
   langchain
   langchain-ollama
   ```

3. Ensure you have **Ollama** installed and the `llama3.2:1b` model pulled:

   ```bash
   ollama pull llama3.2:1b
   ```

---

## ▶️ Usage

Run the app with:

```bash
streamlit run app.py
```

* Enter a YouTube video URL
* Click **Get Transcript** to view the raw transcript
* Click **Summarize** to generate an AI-powered summary


---

## 💡 Example

Input: YouTube lecture (1 hour long)
Output: Concise summary of key points, reducing reading time drastically.

---

## ⚠️ Limitations

* Works only for videos with available English captions.
* Long transcripts may still take time to process.
* Currently limited to summarization (future enhancements: Q&A, keyword extraction).

---

## 🌟 Future Improvements

* Support for multilingual transcripts.
* Option to export summaries as PDF/Word.
* Integration with more powerful LLMs for detailed notes.

---

## 📜 License

MIT License – Free to use and modify.
