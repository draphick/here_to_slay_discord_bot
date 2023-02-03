from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests


class CardDetails(BaseModel):
    """
    Details of card
    """

    card_type: str
    name: str
    link: str
    number_of_cards_in_deck: str
    deck: str


class FullDeck(BaseModel):
    """
    List of all cards in a full deck
    """

    cards: list = CardDetails


def get_cards(soup: str, deck: str, base_url: str) -> FullDeck:
    """
    Get all cards from soup output.
    Returns FullDeck class
    """
    rows = soup.findAll("table")[0].findAll("tr")
    full_deck = []
    card_type = str
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 1:
            # if the row only has 1 column, this must be the card type header
            card_type = cols[0].text.strip("\t\r\n")
            continue
        if len(cols) > 1:
            # if the row has more than 1 column, get the card details using
            # the last type header from the above if
            number_of_cards_in_deck = cols[1].text.strip("\t\r\n")
            for col in cols:
                for link in col.find_all("a", href=True):
                    card_name = link.text.strip()
                    card_link = f"{base_url}{link['href']}"
                    if not len(card_name):  # pylint: disable=use-implicit-booleaness-not-len
                        continue
                    full_deck.append(
                        CardDetails(
                            card_type=card_type,
                            name=card_name,
                            link=card_link,
                            number_of_cards_in_deck=number_of_cards_in_deck,
                            deck=deck,
                        )
                    )
    return full_deck
