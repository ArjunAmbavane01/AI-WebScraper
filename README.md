# AI Web Scraper

AI Web Scraper is a modern Streamlit application that allows users to scrape websites and analyze content using advanced AI. Unlike traditional tools that rely on remote models, this project uses a local LLM (Ollama) for parsing and analysis.

## 🛠️ Prerequisites

- **Python 3.8+**
- **pip**
- **Google Chrome** browser
- **ChromeDriver**

## 🚀 Setup

Follow these steps to set up and run the AI Web Scraper:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install ChromeDriver:
   - Download the appropriate version of ChromeDriver for your operating system and Chrome browser version from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   - Extract the downloaded file and place the `chromedriver.exe` (Windows) or `chromedriver` (Mac/Linux) in the root directory of the project.

   Note: Make sure the ChromeDriver version matches your installed Chrome browser version.

5. Set up Ollama:
   - Install Ollama by following the instructions at [Ollama Installation](https://github.com/jmorganca/ollama#installation).
   - Pull the required model:
     ```
     ollama pull llama3.1
     ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the application:
   - Enter a website URL in the provided input field.
   - Click "Scrape Site" to fetch the content.
   - Once scraped, enter a description of what you want to parse from the content.
   - Click "Parse Content" to analyze the scraped data using AI.


## Troubleshooting

- If you encounter issues with ChromeDriver, ensure that:
  - The ChromeDriver version matches your Chrome browser version.
  - The `chromedriver.exe` (or `chromedriver`) is in the correct location.
  - You have the necessary permissions to execute ChromeDriver.

- If you face issues with Ollama:
  - Make sure Ollama is properly installed and the required model is pulled.
  - Check if the Ollama service is running in the background.


