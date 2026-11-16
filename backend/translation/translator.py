
import re

import ctranslate2
import sentencepiece

from utils.logger import get_logger
from utils.config import Config

logger = get_logger("models.translation")


class Translator:
    """NLLB-200 translation engine using CTranslate2 INT8."""

    LANGUAGE_CODES = {
        "nepali": "npi_Deva",
        "ne": "npi_Deva",
        "npi": "npi_Deva",

        "sinhala": "sin_Sinh",
        "si": "sin_Sinh",
        "sin": "sin_Sinh",

        "english": "eng_Latn",
        "en": "eng_Latn",
    }

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load the local CTranslate2 INT8 model."""

        model_path = Config.TRANSLATION_MODEL_PATH

        if not model_path.exists():
            raise FileNotFoundError(
                f"Translation model not found: {model_path}"
            )

        logger.info("Loading CTranslate2 NLLB model...")

        try:
            self.model = ctranslate2.Translator(
                str(model_path),
                device="cpu",
                compute_type="int8",
                inter_threads=1,
                intra_threads=2,
            )

            self.tokenizer = sentencepiece.SentencePieceProcessor(
                model_file=str(model_path / "sentencepiece.bpe.model")
            )

            logger.info("NLLB INT8 model loaded successfully.")

        except Exception:
            logger.exception("Failed to load translation model.")
            raise

    def _get_language_code(self, language):
        """Convert a language name or alias to its NLLB code."""

        if not isinstance(language, str):
            raise ValueError("Language must be a string.")

        language = language.strip()

        code = self.LANGUAGE_CODES.get(language.lower())

        if code:
            return code

        # Also allow explicitly supplied NLLB codes.
        if re.fullmatch(r"[a-z]{3}_[A-Za-z]{4}", language):
            return language

        raise ValueError(f"Unsupported language: {language}")

    def _split_into_chunks(self, text, max_tokens=450):
        """Split long text into manageable SentencePiece token chunks."""

        sentences = re.split(
            r"(?<=[.!?।。！？])\s+|\n+",
            text.strip()
        )

        chunks = []
        current_tokens = []

        for sentence in sentences:
            if not sentence.strip():
                continue

            sentence_tokens = self.tokenizer.encode(
                sentence,
                out_type=str
            )

            if not sentence_tokens:
                continue

            # Split unusually long individual sentences.
            if len(sentence_tokens) > max_tokens:
                if current_tokens:
                    chunks.append(current_tokens)
                    current_tokens = []

                for i in range(0, len(sentence_tokens), max_tokens):
                    chunks.append(
                        sentence_tokens[i:i + max_tokens]
                    )

                continue

            if (
                current_tokens
                and len(current_tokens) + len(sentence_tokens) > max_tokens
            ):
                chunks.append(current_tokens)
                current_tokens = []

            current_tokens.extend(sentence_tokens)

        if current_tokens:
            chunks.append(current_tokens)

        return chunks

    def translate(self, text, source_lang, target_lang):
        """Translate text between supported languages."""

        if not isinstance(text, str):
            raise TypeError("Translation input must be a string.")

        if not text.strip():
            return {
                "translated_text": "",
                "source_language": source_lang,
                "target_language": target_lang,
            }

        src_code = self._get_language_code(source_lang)
        tgt_code = self._get_language_code(target_lang)

        if src_code == tgt_code:
            return {
                "translated_text": text,
                "source_language": source_lang,
                "target_language": target_lang,
            }

        logger.info(
            "Translating %s → %s",
            src_code,
            tgt_code
        )

        try:
            chunks = self._split_into_chunks(text)

            source_tokens = [
                [src_code] + chunk + ["</s>"]
                for chunk in chunks
            ]

            target_prefixes = [
                [tgt_code] for _ in source_tokens
            ]

            results = self.model.translate_batch(
                source_tokens,
                target_prefix=target_prefixes,
                beam_size=4,
                max_decoding_length=512,
            )

            translated_chunks = []

            for result in results:
                output_tokens = result.hypotheses[0]

                output_tokens = [
                    token
                    for token in output_tokens
                    if token not in {
                        src_code,
                        tgt_code,
                        "</s>",
                        "<s>",
                    }
                ]

                translated_chunks.append(
                    self.tokenizer.decode(output_tokens)
                )

            translated_text = "\n".join(translated_chunks)

            logger.info(
                "Translation completed: %d characters",
                len(translated_text)
            )

            return {
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
            }

        except Exception:
            logger.exception("Translation failed.")
            raise

    def batch_translate(self, texts, source_lang, target_lang):
        """Translate multiple text inputs."""

        logger.info("Batch translating %d texts", len(texts))

        return [
            self.translate(text, source_lang, target_lang)
            for text in texts
        ]
