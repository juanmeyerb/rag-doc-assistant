from lingua import LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_all_languages().build()


def _detect(text, min_letters):
    letters = sum(1 for character in text if character.isalpha())
    if letters < min_letters:
        return None
    return detector.detect_language_of(text)


def detect_language(text, min_letters):
    language = _detect(text, min_letters)
    if language is None:
        return "unknown"
    return language.iso_code_639_1.name.lower()


def detect_language_name(text, min_letters):
    language = _detect(text, min_letters)
    if language is None:
        return None
    return language.name.capitalize()