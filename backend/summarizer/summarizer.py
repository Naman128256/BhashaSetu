
import os
from dotenv import load_dotenv
from google import genai
from utils.logger import get_logger

logger = get_logger("models.summarizer")

load_dotenv()


class Summarizer:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        self.client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 120000}
        )

        self.model_name = "gemini-3.5-flash-lite"

        logger.info("Gemini Flash-Lite client initialized.")

    def summarize(self, text, max_length=150, min_length=30):

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        text = text.strip()

        if not text:
            return {
                "summary": "",
                "method": "gemini_api",
                "compression_ratio": 0.0
            }

        prompt = f"""
        Summarize the following document in clear, natural English.

        Instructions:
        1. Preserve the main ideas and important facts.
        2. Do not invent information.
        3. Avoid unnecessary repetition.
        4. Keep the summary approximately between
           {min_length} and {max_length} words.

        Document:
        {text}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            summary = (response.text or "").strip()

            if not summary:
                raise RuntimeError("Gemini returned an empty summary.")

            return {
                "summary": summary,
                "method": "gemini_api",
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text)
            }

        except Exception:
            logger.exception("Gemini summarization failed.")
            raise
