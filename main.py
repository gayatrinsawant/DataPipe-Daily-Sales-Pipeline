
from sources import SOURCES
from extract import read_csv_source, read_api_source
from transform import transform_data
from load import load_data


def main():
    all_rows = []
    failed_sources = []

    print("Starting DataPipe pipeline...\n")

    for source in SOURCES:
        if source["type"] == "csv":
            rows = read_csv_source(source)
        else:
            rows = read_api_source(source)

            if rows is None:
                failed_sources.append(source["store"])
                rows = []

        print(source["store"], ":", len(rows), "rows extracted")
        all_rows.extend(rows)

    print("\nCleaning and validating data...")

    valid_rows, rejected_rows = transform_data(all_rows)

    print("Total records:", len(all_rows))
    print("Valid records:", len(valid_rows))
    print("Rejected records:", len(rejected_rows))

    print("\nCreating Excel report...")

    load_data(
        valid_rows,
        rejected_rows,
        len(all_rows),
        failed_sources
    )

    print("\nDataPipe pipeline completed!")


if __name__ == "__main__":
    main()
