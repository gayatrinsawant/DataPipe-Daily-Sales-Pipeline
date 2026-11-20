
import csv
import requests


def read_csv_source(source):
    rows = []

    with open(source["path"], newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["store"] = source["store"]
            rows.append(row)

    return rows


def read_api_source(source):
    try:
        response = requests.get(
            source["url"],
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        # Extract orders from API dictionary
        rows = data["orders"]

        for row in rows:
            row["store"] = source["store"]

        return rows

    except requests.RequestException as error:
        print(f"Error fetching {source['store']}: {error}")
        return None

    except (KeyError, TypeError) as error:
        print(f"Invalid API response from {source['store']}: {error}")
        return None
    
if __name__ == "__main__":
    from sources import SOURCES

    for source in SOURCES:
        if source["type"] == "csv":
            rows = read_csv_source(source)
        else:
            rows = read_api_source(source)

        print(source["store"], ":", len(rows), "rows")

        if rows:
            print("First record:", rows[0])