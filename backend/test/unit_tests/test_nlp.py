from collections import Counter
import pytest
from bs4 import BeautifulSoup, Comment
from src.sentiment.nlp import (
    has_tag,
    from_body,
    is_token_allowed,
    process_text,
)  # Adjust import according to your code structure
from spacy.tokens import Token
from spacy.lang.en import English
import spacy


@pytest.fixture(scope="session")
def language():
    return spacy.load("en_core_web_sm")


@pytest.mark.parametrize(
    "token_text, expected_result",
    [
        ("quick", False),
        ("run", False),
        ("the", False),  # A stop word (should be filtered out)
        ("", False),  # Empty token (should be filtered out)
        ("!", False),  # Punctuation (should be filtered out)
        ("http://example.com", False),  # URL (should be filtered out)
        ("123", False),  # Non-alphabetic token (should be filtered out)
    ],
)
def test_is_token_allowed(language, token_text, expected_result):
    # Create a token object manually from the text
    token = Token(language.vocab, language(token_text), 0)

    # Call the function and compare the result
    assert is_token_allowed(token) == expected_result


def test_process_text(language):
    # Simulate a small NLP model

    # Test text and URL
    url = "https://example.com"
    text = "The quick brown fox jumps over the lazy dog."

    # Expected output based on the text
    expected_nouns = {
        "fox": 1,
        "dog": 1,
    }

    # Process the text
    result = process_text((language, url, text))

    # Assert that the result contains the URL and nouns
    assert result["url"] == url
    assert result["nouns"] == expected_nouns


# Test the has_tag function
def test_has_tag_with_visible_text():
    # Simulating a visible text node inside the <body> element
    element = BeautifulSoup(
        "<html><body><div>Hello World</div></body></html>", "html.parser"
    ).div
    assert (
        has_tag(element) == True
    )  # This should now return True because the parent is <body>


def test_has_tag_with_comment():
    # Simulating a comment node
    element = Comment("This is a comment")
    assert has_tag(element) == False


def test_has_tag_with_script_tag():
    # Simulating a script tag
    element = BeautifulSoup(
        "<script>console.log('Hello')</script>", "html.parser"
    ).script
    assert has_tag(element) == False


def test_has_tag_with_style_tag():
    # Simulating a style tag
    element = BeautifulSoup(
        "<style>body {background-color: red;}</style>", "html.parser"
    ).style
    assert has_tag(element) == False


def test_has_tag_with_head_tag():
    # Simulating a head tag
    element = BeautifulSoup("<head><title>Title</title></head>", "html.parser").head
    assert has_tag(element) == False


# Test the from_body function
def test_from_body_with_basic_html():
    body = """
    <html>
        <body>
            <div>Visible Text</div>
            <script>Invisible Script</script>
            <style>Invisible Style</style>
            <p>More visible text.</p>
        </body>
    </html>
    """
    result = from_body(body)
    assert result == "Visible Text More visible text."


def test_from_body_with_comment():
    body = """
    <html>
        <body>
            <div>Visible Text</div>
            <p>More visible text.</p>
            <!-- This is a comment -->
        </body>
    </html>
    """
    result = from_body(body)
    assert result == "Visible Text More visible text."


def test_from_body_with_empty_html():
    body = """
    <html>
        <head></head>
        <body></body>
    </html>
    """
    result = from_body(body)
    assert result == ""  # No visible text


def test_from_body_with_no_visible_text():
    body = """
    <html>
        <head></head>
        <body>
            <style>body {font-size: 12px;}</style>
            <script>console.log('nothing visible')</script>
        </body>
    </html>
    """
    result = from_body(body)
    assert result == ""  # No visible text


def test_from_body_with_only_comments():
    body = """
    <html>
        <body>
            <!-- Comment 1 -->
            <!-- Comment 2 -->
        </body>
    </html>
    """
    result = from_body(body)
    assert result == ""  # No visible text


def test_from_body_with_multiple_visible_and_invisible_text():
    body = """
    <html>
        <body>
            <div>Visible Text 1</div>
            <style>Invisible Style</style>
            <div>Visible Text 2</div>
            <script>Invisible Script</script>
        </body>
    </html>
    """
    result = from_body(body)
    assert result == "Visible Text 1 Visible Text 2"


def test_from_body_with_mixed_tags():
    body = """
    <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <div>First Visible Text</div>
            <p>Second Visible Text</p>
            <script>Invisible Script</script>
            <style>Invisible Style</style>
            <div>Third Visible Text</div>
        </body>
    </html>
    """
    result = from_body(body)
    assert result == "First Visible Text Second Visible Text Third Visible Text"


# Test edge cases for from_body with malformed HTML
def test_from_body_with_malformed_html():
    body = "<html><body><div>Visible Text"
    result = from_body(body)
    assert result == "Visible Text"  # It should still handle incomplete HTML correctly
