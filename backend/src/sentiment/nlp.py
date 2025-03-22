import html
import multiprocessing
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup, PageElement
from bs4.element import Comment
from spacy import Language
from collections import Counter
from spacy.tokens import Token
from sentiment.config import config
from sentiment.profilers import sync_profiler


def has_tag(element) -> bool:
    if element.parent is None:
        return False
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
        "noscript",
        "header",
        "iframe",
        "object",
        "embed",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    if element.string.strip() == "":
        return False
    return True


def from_body(body: str) -> str:
    soup = BeautifulSoup(body, "html.parser")
    texts = soup.find_all(string=True)
    visible_texts = filter(has_tag, texts)
    text = " ".join(t.strip() for t in visible_texts).strip()
    return html.escape(text)


def is_token_allowed(token: Token) -> bool:
    allowed = bool(
        token
        and str(token).strip()
        and not token.is_stop
        and not token.is_punct
        and token.pos_ == "NOUN"
        and not token.like_url
        and token.is_alpha
        and len(token.text) > 1
    )
    return allowed


def process_text(args):
    """Process a single text document to extract nouns."""
    nlp, url, text = args
    doc = nlp(text)

    lemma = [word.lemma_.lower() for word in doc if is_token_allowed(word)]

    return {
        "url": url,
        "nouns": dict(Counter(lemma).most_common(config.MOST_COMMON_NOUNS_COUNT)),
    }


@sync_profiler
def compute(
    nlp: Language, data: List[Tuple[str, str]]
) -> Tuple[List[Dict], List[Dict]]:
    """Compute pairwise similarities and extract nouns from texts."""
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        nouns = pool.map(process_text, ((nlp, url, text) for url, text in data))

    docs = list(nlp.pipe((text for _, text in data), batch_size=10))
    similarities = [
        {
            "url_1": data[i][0],
            "url_2": data[j][0],
            "score": round(docs[i].similarity(docs[j]), 2),
        }
        for i in range(len(docs))
        for j in range(i + 1, len(docs))
    ]
    return nouns, similarities
