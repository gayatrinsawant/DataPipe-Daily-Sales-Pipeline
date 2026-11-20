
from datetime import datetime

import os
from openpyxl import Workbook, load_workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Border,
    Side,
    Alignment
)

from sources import (
    OUTPUT_FILE,
    SALES_COLUMNS,
    REJECTED_COLUMNS,
    HISTORY_COLUMNS
)


# Function to format Excel sheets
def format_sheet(sheet):

    # Header background colour
    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78"
    )

    # Header font
    header_font = Font(
        bold=True,
        color="FFFFFF",
        size=11
    )

    # Border
    thin_border = Border(
        bottom=Side(
            style="thin",
            color="D9E2F3"
        )
    )

    # Format headings
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Format all cells
    for row in sheet.iter_rows():
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(
                vertical="center"
            )

    # Automatically adjust column widths
    for column in sheet.columns:

        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            if cell.value is not None:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        sheet.column_dimensions[column_letter].width = min(
            max_length + 4,
            30
        )

    # Freeze heading row
    sheet.freeze_panes = "A2"

    # Add filters
    if sheet.max_row > 1:
        sheet.auto_filter.ref = sheet.dimensions


def load_data(valid_rows, rejected_rows, rows_read, failed_sources):

    # Open existing workbook or create a new one
    if os.path.exists(OUTPUT_FILE):
        workbook = load_workbook(OUTPUT_FILE)
    else:
        workbook = Workbook()

    # Remove the default empty sheet if present
    if "Sheet" in workbook.sheetnames:
        del workbook["Sheet"]

    # Refresh these sheets on every run
    for sheet_name in ["Sales", "Rejected", "Summary"]:
        if sheet_name in workbook.sheetnames:
            del workbook[sheet_name]

    # Sales sheet
    sales = workbook.create_sheet("Sales", 0)
    sales.append(SALES_COLUMNS)

    for row in valid_rows:
        sales.append([row.get(col, "") for col in SALES_COLUMNS])

    # Rejected sheet
    rejected = workbook.create_sheet("Rejected", 1)
    rejected.append(REJECTED_COLUMNS)

    for row in rejected_rows:
        rejected.append([row.get(col, "") for col in REJECTED_COLUMNS])

    # Summary sheet
    summary = workbook.create_sheet("Summary", 2)

    total_sales = sum(row["amount"] for row in valid_rows)

    summary.append(["Metric", "Value"])
    summary.append(["Total Records", rows_read])
    summary.append(["Valid Records", len(valid_rows)])
    summary.append(["Rejected Records", len(rejected_rows)])
    summary.append(["Total Sales Amount", total_sales])

    # Run History sheet - preserve previous runs
    if "Run_History" not in workbook.sheetnames:
        history = workbook.create_sheet("Run_History")
        history.append(HISTORY_COLUMNS)
    else:
        history = workbook["Run_History"]

    history.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Success" if not failed_sources else "Partial Success",
        rows_read,
        len(valid_rows),
        len(rejected_rows),
        0,
        ", ".join(failed_sources) if failed_sources else "None"
    ])

    # Format all sheets
    for sheet in workbook.worksheets:
        format_sheet(sheet)

    # Currency formatting
    for row in range(2, sales.max_row + 1):
        sales.cell(row, 6).number_format = '"₹"#,##0.00'
        sales.cell(row, 7).number_format = '"₹"#,##0.00'

    summary["B5"].number_format = '"₹"#,##0.00'

    # Save workbook
    workbook.save(OUTPUT_FILE)

    print("\nExcel file updated successfully!")
    print("Total Sales:", total_sales)
    print("Total Valid Records:", len(valid_rows))
    print("Total Rejected Records:", len(rejected_rows))
    print("Total Runs Recorded:", history.max_row - 1)
