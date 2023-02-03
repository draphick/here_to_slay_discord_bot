# pylint: disable=no-member too-few-public-methods no-name-in-module missing-module-docstring no-name-in-module
import csv
from apioutput import apiOutput  # pylint: disable=import-error unused-import
import requests
from bs4 import BeautifulSoup
from utils.get_wiki import get_cards

BASEURL = "http://unstablegameswiki.com"
decks = [
    "Here_To_Slay_Base_Deck_-_Inventory_List",
    # "Here_To_Slay_Dragon_Sorcerer_Expansion_-_Inventory_List",
    # "Here_To_Slay_Monster_Expansion_-_Inventory_List",
    # "Here_To_Slay_Dragon_Warrior_and_Druid_Expansion_-_Inventory_List",
    # "Here_To_Slay_Dragon_Berserkers_and_Necromancers_Expansion_-_Inventory_List",
    # "Here_To_Slay_Here_To_Sleigh_Expansion_-_Inventory_List",
]


def get_deck_details(deck_inventory_list: list):
    for web_page in deck_inventory_list:
        api_url = f"{BASEURL}/api.php?action=parse&format=json&page={web_page}"
        resp = requests.get(api_url)
        output = resp.json()["parse"]["text"]["*"]
        bs_raw = BeautifulSoup(output, "html.parser")
        # bs_raw = BeautifulSoup(apiOutput["parse"]["text"]["*"], 'html.parser')

        all_cards = get_cards(soup=bs_raw, deck=web_page, base_url=BASEURL)
        with open(f"{web_page}.csv", "w", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=["deck", "card_type", "name", "number_of_cards_in_deck", "link"]
            )
            writer.writeheader()
            for card in all_cards:
                line = [card.dict()]
                writer.writerows(line)


if __name__ == "__main__":
    print("Getting deck details")
    # get_deck_details(deck_inventory_list=decks)
