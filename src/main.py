import flet as ft
import requests
from bs4 import BeautifulSoup
import re


def main(page: ft.Page):
    async def button_clicked(e):
        page_html = requests.get(url_input.value).text
        soup = BeautifulSoup(page_html, features="html.parser")
        card_list = soup.find_all("div", class_="badge_card_set_card")
        parsed_data = {
            "have": [],
            "want": [],
        }
        title_str = ""
        for i, card in enumerate(card_list):
            card_name = "".join(
                card.find("div", class_="badge_card_set_title").findAll(
                    string=True, recursive=False
                )
            ).strip()
            if "owned" in card["class"]:
                qty = card.find("div", class_="badge_card_set_text_qty")
                p = re.compile(r"(\d+)")
                card_count = int(p.findall(qty.text)[0])
                if card_count > 1:
                    parsed_data["have"].append((card_name, i + 1))
            elif "unowned" in card["class"]:
                parsed_data["want"].append((card_name, i + 1))

        def parse_card_numbers(card_list):
            return ", ".join([f"{number}" for _name, number in card_list])

        def format_title_string(have_cards, want_cards):
            return f"1:1 [H] {parse_card_numbers(have_cards)} [W] {parse_card_numbers(want_cards)}"

        def format_content_string(have_cards, want_cards):
            have_cards_str = "\n".join([f"[*] {name}" for name, number in have_cards])
            want_cards_str = "\n".join([f"[*] {name}" for name, number in want_cards])
            return (
                "Hello, I want trade cards 1:1 in same set. :steamhappy:"
                "\n\n"
                "[h1]HAVE[/h1]"
                "\n"
                "[list]"
                "\n{0}\n"
                "[/list]"
                "\n\n"
                "[h1]WANT[/h1]"
                "\n"
                "[list]"
                "\n{1}\n"
                "[/list]"
                "\n\n"
                "Thanks"
            ).format(have_cards_str, want_cards_str)

        have_cards = parsed_data["have"]
        want_cards = parsed_data["want"]
        parse_title.value = format_title_string(have_cards, want_cards)
        parse_content.value = format_content_string(have_cards, want_cards)
        page.update()

    url_input = ft.TextField(
        label="Steam trading card page",
        hint_text="Please enter url here",
    )
    parse_title = ft.TextField(label="Title", read_only=True)
    parse_content = ft.TextField(label="Content", read_only=True, multiline=True)
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(url_input, b, parse_title, parse_content)


ft.app(main)
