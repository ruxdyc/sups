import argparse
from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import gspread
from google.oauth2.service_account import Credentials


SALE_COLUMNS = [
    "Дата продажи",
    "Название товара",
    "Артикул продавца",
    "Количество",
    "Цена",
    "Стоимость WB",
    "Комиссия",
    "Валюта",
    "Тип операции",
]


def scrape_sales(url: str) -> List[List[str]]:
    """Open the given URL in a headless Chrome browser and parse sales data.

    The page is expected to contain a table with the columns listed in
    ``SALE_COLUMNS``. This function returns a list of rows, each represented as
    a list of cell values in the order defined by ``SALE_COLUMNS``.
    """
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        # Give the page time to load dynamic content.
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table")
        if not table:
            raise ValueError("No table found on the page")
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if len(cells) == len(SALE_COLUMNS):
                rows.append(cells)
        return rows
    finally:
        driver.quit()


def update_google_sheet(spreadsheet_id: str, rows: List[List[str]], creds_json: str) -> None:
    """Append rows to the first sheet of the given Google Spreadsheet."""
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds_json, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1
    sheet.append_rows(rows, value_input_option="USER_ENTERED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch sales data and store it in Google Sheets")
    parser.add_argument("url", help="Link to the page with sales data")
    parser.add_argument("spreadsheet_id", help="ID of the target Google Spreadsheet")
    parser.add_argument("credentials", help="Path to Google service account credentials JSON file")
    args = parser.parse_args()

    rows = scrape_sales(args.url)
    if not rows:
        print("No sales data found.")
        return
    update_google_sheet(args.spreadsheet_id, rows, args.credentials)
    print(f"Added {len(rows)} rows to spreadsheet {args.spreadsheet_id}")


if __name__ == "__main__":
    main()
