from datetime import datetime, timezone

import yaml
from apex_ocr_server.config import DATABASE_YML_FILE
from apex_ocr_server.database.api import ApexDatabaseApi
from apex_ocr_server.database.models import Season


def populate_db():
    with open(DATABASE_YML_FILE) as db_file:
        db_config = yaml.load(db_file, Loader=yaml.FullLoader)

    dialect = db_config["dialect"]
    username = db_config["username"]
    password = db_config["password"]
    hostname = db_config["hostname"]
    port = db_config["port"]
    database_name = db_config["database_name"]

    db_conn_str = f"{dialect}://{username}:{password}@{hostname}:{port}/{database_name}"

    db_conn = ApexDatabaseApi(db_conn_str)

    seasons = [
        Season(
            number=0,
            name="Preseason",
            start_date=datetime(2019, 2, 4, tzinfo=timezone.utc),
            end_date=datetime(2019, 3, 19, tzinfo=timezone.utc),
        ),
        Season(
            number=1,
            name="Wild Frontier",
            start_date=datetime(2019, 3, 19, tzinfo=timezone.utc),
            end_date=datetime(2019, 7, 2, tzinfo=timezone.utc),
        ),
        Season(
            number=2,
            name="Battle Charge",
            start_date=datetime(2019, 7, 2, tzinfo=timezone.utc),
            end_date=datetime(2019, 10, 1, tzinfo=timezone.utc),
        ),
        Season(
            number=3,
            name="Meltdown",
            start_date=datetime(2019, 10, 1, tzinfo=timezone.utc),
            end_date=datetime(2020, 2, 4, tzinfo=timezone.utc),
        ),
        Season(
            number=4,
            name="Assimilation",
            start_date=datetime(2020, 2, 4, tzinfo=timezone.utc),
            end_date=datetime(2020, 5, 12, tzinfo=timezone.utc),
        ),
        Season(
            number=5,
            name="Fortune's Favor",
            start_date=datetime(2020, 5, 12, tzinfo=timezone.utc),
            end_date=datetime(2020, 8, 18, tzinfo=timezone.utc),
        ),
        Season(
            number=6,
            name="Boosted",
            start_date=datetime(2020, 8, 18, tzinfo=timezone.utc),
            end_date=datetime(2020, 11, 4, tzinfo=timezone.utc),
        ),
        Season(
            number=7,
            name="Ascension",
            start_date=datetime(2020, 11, 4, tzinfo=timezone.utc),
            end_date=datetime(2021, 2, 2, tzinfo=timezone.utc),
        ),
        Season(
            number=8,
            name="Mayhem",
            start_date=datetime(2021, 2, 2, tzinfo=timezone.utc),
            end_date=datetime(2021, 5, 4, tzinfo=timezone.utc),
        ),
        Season(
            number=9,
            name="Legacy",
            start_date=datetime(2021, 5, 4, tzinfo=timezone.utc),
            end_date=datetime(2021, 8, 3, tzinfo=timezone.utc),
        ),
        Season(
            number=10,
            name="Emergence",
            start_date=datetime(2021, 8, 3, tzinfo=timezone.utc),
            end_date=datetime(2021, 11, 2, tzinfo=timezone.utc),
        ),
        Season(
            number=11,
            name="Escape",
            start_date=datetime(2021, 11, 2, tzinfo=timezone.utc),
            end_date=datetime(2022, 2, 8, tzinfo=timezone.utc),
        ),
        Season(
            number=12,
            name="Defiance",
            start_date=datetime(2022, 2, 8, tzinfo=timezone.utc),
            end_date=datetime(2022, 5, 10, tzinfo=timezone.utc),
        ),
        Season(
            number=13,
            name="Saviors",
            start_date=datetime(2022, 5, 10, tzinfo=timezone.utc),
            end_date=datetime(2022, 8, 9, tzinfo=timezone.utc),
        ),
        Season(
            number=14,
            name="Hunted",
            start_date=datetime(2022, 8, 9, tzinfo=timezone.utc),
            end_date=datetime(2022, 11, 1, tzinfo=timezone.utc),
        ),
        Season(
            number=15,
            name="Eclipse",
            start_date=datetime(2022, 11, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 2, 14, tzinfo=timezone.utc),
        ),
        Season(
            number=16,
            name="Revelry",
            start_date=datetime(2023, 2, 14, tzinfo=timezone.utc),
            end_date=datetime(2023, 5, 16, tzinfo=timezone.utc),
        ),
        Season(
            number=17,
            name="Arsenal",
            start_date=datetime(2023, 5, 16, tzinfo=timezone.utc),
            end_date=datetime(2023, 8, 8, tzinfo=timezone.utc),
        ),
        Season(
            number=18,
            name="Resurrection",
            start_date=datetime(2023, 8, 8, tzinfo=timezone.utc),
        ),
    ]

    db_conn.add_all(seasons)


if __name__ == "__main__":
    populate_db()
