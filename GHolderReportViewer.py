# By Scott Cardwell
# 5/13/2025
import os
# os: Provides a way to interact with the operating system, such as reading or writing files.
import tkinter as tk
from tkinter import filedialog
# tkinter as tk: Imports the Tkinter library for GUI components.
# need to update this to ttk
from pathlib import Path
# Path from pathlib: Offers an object-oriented approach to handling filesystem paths.

def select_file() -> Path | None:
# Open a file dialog for the user to select a text file.
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt")]
    )
    return Path(file_path) if file_path else None

def read_file_lines(file_path: Path) -> list[str]:
    """Read all lines from the specified file."""
    with file_path.open("r", encoding="utf-8") as file:
        return file.readlines()

def extract_data(lines: list[str]) -> dict:
    """Extract relevant data from the file lines."""
    data = {}
    if lines:
        first_line = lines[0].strip()
        last_line = lines[-1].strip()

        # Extracting data from the first line
        data['holder_name'] = first_line[36:71].strip()
        data['tr_code'] = first_line[0]
        data['tax_id'] = first_line[1:10]
        data['tax_id_ext'] = first_line[10:14]
        data['report_year'] = first_line[14:18]
        data['type'] = first_line[18:19]
        data['report_number'] = first_line[19:21]
        data['report_format'] = first_line[21:22]
        data['sic'] = first_line[22:26]
        data['state_of_inc'] = first_line[26:28]
        data['inc_year'] = first_line[28:32]
        data['inc_month'] = first_line[32:34]
        data['inc_day'] = first_line[34:36]

        # Extracting data from the last line
        data['number_of_records'] = int(last_line[1:7].lstrip('0') or '0')
        data['number_of_properties'] = int(last_line[7:13].lstrip('0') or '0')
        data['amount_reported'] = float(last_line[13:25].strip()) / 100
        data['deducted_amount'] = float(last_line[25:37].strip()) / 100
        data['advertisement_deduction'] = float(last_line[37:49].strip()) / 100
        data['deleted_amount'] = float(last_line[49:61].strip()) / 100
        data['amount_remitted'] = float(last_line[61:73].strip()) / 100
        data['shares'] = float(last_line[73:87].strip()) / 1000
        data['add_shares'] = float(last_line[87:101].strip()) / 1000
        data['del_shares'] = float(last_line[101:115].strip()) / 1000
        data['remitted_shares'] = float(last_line[115:129].strip()) / 1000
    return data

def format_data(data: dict) -> str:
    """Format the extracted data into a readable string."""
    formatted_data = (
        f"Holder Name: {data.get('holder_name', '')}\n"
        f"TR-CODE: {data.get('tr_code', '')}, Record Type: HOLDER\n"
        f"Tax ID: {data.get('tax_id', '')}, Extension: {data.get('tax_id_ext', '')}\n"
        f"Report Year: {data.get('report_year', '')}\n"
        f"Type: {data.get('type', '')}\n"
        f"Report #: {data.get('report_number', '')}\n"
        f"Report Format: {data.get('report_format', '')}\n"
        f"SIC: {data.get('sic', '')}\n"
        f"State of Inc: {data.get('state_of_inc', '')}\n"
        f"Inc Date: {data.get('inc_year', '')}, {data.get('inc_month', '')}, {data.get('inc_day', '')}\n"
        f"Number of Records: {data.get('number_of_records', 0):>23}\n"
        f"Number of Properties: {data.get('number_of_properties', 0):>20}\n"
        f"Amount Reported: ${data.get('amount_reported', 0.00):,.2f}\n"
        f"Deducted Amount: ${data.get('deducted_amount', 0.00):,.2f}\n"
        f"Advertisement Deduction: ${data.get('advertisement_deduction', 0.00):,.2f}\n"
        f"Deleted Amount: ${data.get('deleted_amount', 0.00):,.2f}\n"
        f"Amount Remitted: ${data.get('amount_remitted', 0.00):,.2f}\n"
        f"Shares: {data.get('shares', 0.0000):,.4f}\n"
        f"Add Shares: {data.get('add_shares', 0.0000):,.4f}\n"
        f"Del Shares: {data.get('del_shares', 0.0000):,.4f}\n"
        f"Remitted Shares: {data.get('remitted_shares', 0.0000):,.4f}\n"
    )
    return formatted_data

def display_data(formatted_data: str) -> None:
    """Display the formatted data in a Tkinter window."""
    root = tk.Tk()
    root.title("Extracted Data")

    text_widget = tk.Text(root, wrap='word', padx=10, pady=10)
    text_widget.insert('1.0', formatted_data)
    text_widget.config(state='disabled')  # Make the text widget read-only
    text_widget.pack(expand=True, fill='both')

    root.mainloop()

def main() -> None:
    """Main function to execute the program."""
    file_path = select_file()
    if file_path:
        lines = read_file_lines(file_path)
        data = extract_data(lines)
        formatted_data = format_data(data)
        display_data(formatted_data)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
