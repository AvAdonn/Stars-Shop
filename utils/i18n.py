from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

def create_translator_hub() -> TranslatorHub:
    translator_uk = FluentTranslator(
        locale='uk',
        translator=FluentBundle.from_files(
            locale='uk-UA',
            filenames=['locales/uk/main.ftl']
        )
    )
    
    translator_eu  = FluentTranslator(
        locale='en',
        translator=FluentBundle.from_files(
            locale='en-US',
            filenames=['locales/eu/main.ftl']
        )
    )
    
    hub = TranslatorHub(
        locales_map={
            'uk': ('uk', 'en'),
            'en': ('en', 'en'),
            'ru': ('ru', 'en')
        },
        translators=[translator_uk, translator_eu],
        root_locale='en'
    )
    
    return hub