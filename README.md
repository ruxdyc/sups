# Sales Scraper to Google Sheets

This repository contains a Python script `wb_sales_to_google.py` that opens a web page in Google Chrome, scrapes sales information, and appends it to a Google Spreadsheet.

## Requirements

- Python 3.7+
- Google Chrome and `chromedriver` installed
- Python packages:
  - `selenium`
  - `bs4`
  - `gspread`
  - `google-auth`

Install dependencies with:

```bash
pip install selenium bs4 gspread google-auth
```

## Google Sheets Setup

1. Create a Google Cloud project and enable the **Google Sheets API**.
2. Create a **service account** and download its JSON credentials file.
3. Share the target spreadsheet with the service account email.

## Usage

```bash
python wb_sales_to_google.py <URL> <SPREADSHEET_ID> <CREDENTIALS_JSON>
```

- `<URL>` – link to the page containing sales data.
- `<SPREADSHEET_ID>` – the ID of the Google Spreadsheet (found in the URL).
- `<CREDENTIALS_JSON>` – path to the service account credentials.

The page should contain a table with the following columns in order:

1. Дата продажи
2. Название товара
3. Артикул продавца
4. Количество
5. Цена
6. Стоимость WB
7. Комиссия
8. Валюта
9. Тип операции

All rows from the table will be appended to the first sheet of the specified spreadsheet.
