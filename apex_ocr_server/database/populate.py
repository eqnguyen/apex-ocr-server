import re
from datetime import datetime

import click
import fandom
from apex_ocr_server.config import DATABASE_YML_FILE
from apex_ocr_server.database.api import ApexDatabaseApi
from apex_ocr_server.database.models import Patch, Season
from bs4 import BeautifulSoup
from tqdm import tqdm


@click.command()
@click.option("--seasons", is_flag=True, help="Populate database with Apex seasons")
@click.option("--patches", is_flag=True, help="Populate database with Apex patches")
def populate_db(seasons: bool, patches: bool):
    db_conn = ApexDatabaseApi(config=DATABASE_YML_FILE)

    fandom.set_wiki("apexlegends")

    # Parse fandom Wiki for season information
    if seasons:
        season_page_query = fandom.search("Season", results=1)[0]
        season_page = fandom.page(pageid=season_page_query[1])
        season_content = season_page.content["sections"][0]["content"].split("\n")
        season_strings = [
            f"{season_content[i-1]}: {s}"
            for i, s in enumerate(season_content)
            if "days)" in s
        ]

        season_entries = []
        date_format = "%b %d, %Y"

        for season_str in tqdm(season_strings, desc="Seasons"):
            name_number_str, date_str = season_str.split(":", 1)
            name = name_number_str.split("(", 1)[0]
            match = re.search(r"\d+", name_number_str)
            if match:
                number = int(match.group())
            else:
                number = 0
            date_str = date_str.replace(".", "")
            start_date = datetime.strptime(
                date_str.split(" - ")[0].strip(), date_format
            ).date()
            end_date = datetime.strptime(
                date_str.split(" - ")[1].split("(", 1)[0], date_format
            ).date()

            season_entries.append(
                Season(
                    number=number, name=name, start_date=start_date, end_date=end_date
                )
            )

        db_conn.add_all(season_entries)

    # Parse fandom Wiki for patch information
    if patches:
        version_page_query = fandom.search("Version_History", results=1)[0]
        version_page = fandom.page(pageid=version_page_query[1])

        patch_entries = []
        date_format = "%B %d, %Y"

        for yearly_patches in tqdm(
            version_page.content["sections"][0]["sections"], desc="Patch years"
        ):
            for line in tqdm(
                yearly_patches["content"].split("\n"), desc=yearly_patches["title"]
            ):
                if "Patches" in line:
                    continue

                if "Patch" in (line):
                    page_title = line.split("Patch", 1)[0].strip()
                    date = datetime.strptime(page_title, date_format).date()
                    patch_page_query = fandom.search(page_title, results=1)[0]
                    patch_page = fandom.page(pageid=patch_page_query[1])
                    soup = BeautifulSoup(patch_page.html, "html.parser")
                    tables = soup.find_all("table")

                    for table in tables:
                        rows = table.find_all("tr")
                        for row in rows:
                            cells = row.find_all(["th", "td"])
                            row_data = [cell.get_text(strip=True) for cell in cells]
                            if "Version number" in row_data:
                                version = row_data[1]
                                patch_entries.append(Patch(version=version, date=date))

        db_conn.add_all(patch_entries)


if __name__ == "__main__":
    populate_db()
