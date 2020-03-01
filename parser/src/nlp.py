import spacy
import time
from collections import Counter
from string import punctuation
from spacy_langdetect import LanguageDetector

en_nlp = spacy.load("en_core_web_sm")
nb_nlp = spacy.load("nb_core_news_sm")
nb_nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)


def get_hotwords(nlp, doc):
    result = []
    pos_tag = ['NOUN']

    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.lemma_)

    return Counter(result).most_common(5)

def analyze(text):
    start = time.time()
    processedText = text.lower()

    nlp = nb_nlp
    doc = nlp(processedText)

    if doc._.language['language'] == "en":
        nlp = en_nlp
        doc = nlp(processedText)

    print(get_hotwords(nlp, doc))
    end = time.time()

    return {
        'hw': get_hotwords(nlp, doc),
        'lang': doc._.language['language'],
        'time': (end - start) * 1000
    }

def analyzeWithLogging(text):
    start = time.time()
    print("-------------------------------------------")
    print(text)
    print("-------------------------------------------")
    processedText = text.lower()

    nlp = nb_nlp
    doc = nlp(processedText)

    print("Detected language: ", doc._.language['language'])
    if (doc._.language['language'] == "en"):
        nlp = en_nlp
        doc = nlp(processedText)

    print()
    print()

    print("HotWords:")
    startHW = time.time()
    print(get_hotwords(nlp, doc))
    endHW = time.time()
    end = time.time()
    print("Analyzed in ", end - start, "s, HW: ", endHW - startHW, "s")
    print("-------------------------------------------")
    print()
    print()

    return {
        'hw': get_hotwords(nlp, doc),
        'lang': doc._.language['language'],
        'time': (end - start) * 1000
    }


texts = [
    "Hei, jeg lurer på når jeg får godkjent dagpengersøknaden min fra NAV? Jeg jobber ikke lengre for Dagbladet, så trenger de snart. Kommer den, eller må jeg sende inn noe mer informasjon?",
    """Aremark Testfamilien har fått generell informasjon om medlemskap i folketrygden ved arbeid i utlandet. Testfamilien er veiledet til søknadsskjemaet på nav.no.

	NAV Oslo""",
    """Aremark Testfamilien har spørsmål om status i sak på innsendt søknad om dagpenger.

Du har fått informasjon om at
- normal saksbehandlingstid er 21 dager fra vi har mottatt en komplett søknad om dagpenger.
- du finner saksbehandlingstiden i ditt fylke på www.nav.no/saksbehandlingstider
- du kan følge med på status i din sak og lese vedtaket ditt på www.nav.no/dittnav""",
    """Aremark Testfamilien har spørsmål om status i sak på innsendt søknad om dagpengar.

Du har fått informasjon om at
- normal sakshandsamingstid er 21 dagar frå vi har fått ein komplett søknad om dagpengar.
- du finn sakshandsamingstida i ditt fylke på www.nav.no/saksbehandlingstider
- du kan følgje med på status i di sak og lese vedtaket ditt på www.nav.no/dittnav""",
    """Aremark Testfamilien has an enquiry regarding the status of an application for unemployment benefits.

You have been informed that:
- standard processing time is 21 days from the date we receive a complete application for unemployment benefits
- you can find processing times in your region at  www.nav.no/saksbehandlingstider
- you will be informed of the result and can read the decision letter at www.nav.no/dittnav"""
]

if __name__ == "__main__":
    for text in texts:
        analyze(text)
