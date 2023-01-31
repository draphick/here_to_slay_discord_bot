# pylint: disable=no-member too-few-public-methods no-name-in-module missing-module-docstring no-name-in-module
import csv
from pydantic import BaseModel
from bs4 import BeautifulSoup
from apioutput import apiOutput # pylint: disable=import-error unused-import
import requests

BASEURL = "http://unstablegameswiki.com"
webPages = [
    "Here_To_Slay_Base_Deck_-_Inventory_List",
    "Here_To_Slay_Dragon_Sorcerer_Expansion_-_Inventory_List",
    "Here_To_Slay_Monster_Expansion_-_Inventory_List",
    "Here_To_Slay_Dragon_Warrior_and_Druid_Expansion_-_Inventory_List",
    "Here_To_Slay_Dragon_Berserkers_and_Necromancers_Expansion_-_Inventory_List",
    "Here_To_Slay_Here_To_Sleigh_Expansion_-_Inventory_List",
]

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


def get_cards(soup: str, deck: str) -> FullDeck:
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
                    card_link = f"{BASEURL}{link['href']}"
                    if not len(card_name): #pylint: disable=use-implicit-booleaness-not-len
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


for webPage in webPages:
    apiUrl = f"{BASEURL}/api.php?action=parse&format=json&page={webPage}"
    resp = requests.get(apiUrl)
    output = resp.json()["parse"]["text"]["*"]
    bs = BeautifulSoup(output, "html.parser")
    # bs = BeautifulSoup(apiOutput["parse"]["text"]["*"], 'html.parser')

    all_cards = get_cards(soup=bs, deck=webPage)
    with open(f"{webPage}.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["card_type", "name", "link", "number_of_cards_in_deck", "deck"]
        )
        writer.writeheader()
        for card in all_cards:
            line = [card.dict()]
            writer.writerows(line)
