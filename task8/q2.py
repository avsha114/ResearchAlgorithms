"""
    This program gets an input from a Google spreadsheet and apply BinCompletion algorithm on it.
    Google account should be in 'credential.json'.
    The Input should be in a spreadsheet called 'BinCompletion' in a worksheet called 'Input'.
    See screenshots for details.
    The result is saved in a worksheet called Output in the same spreadsheet.

    Author: Avshalom Avraham
"""

from prtpy.packing.bin_completion import *
import gspread


def bin_completions_sheets():
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open("BinCompletion")

    try:
        input_sheet = spreadsheet.worksheet("Input")
        output_sheet = spreadsheet.worksheet("Output")
    except gspread.exceptions.WorksheetNotFound as err:
        # if no 'Input' sheet was found - return:
        if err.__str__() == "Input":
            print("No input worksheet was found")
            return
        # if no 'Output' sheet was found - create it:
        if err.__str__() == "Output":
            number_of_examples = len(input_sheet.col_values(1))
            output_sheet = spreadsheet.add_worksheet(title="Output", rows=number_of_examples, cols=100)

    # worksheet index starts with 1
    output_row_index = 1

    for example in input_sheet.get_all_values():
        # if this is the first row - continue
        if example[0] == "Index":
            continue

        # list values index starts with 0 as usual
        # first cell is the title - 'Example_x'
        # second cell is the binsize
        # third cell to end are the items
        item_list = [int(item) for item in example[2:] if item]

        # apply the algorithm and get the result:
        bin_completion_result = bin_completion(BinsKeepingContents(), binsize=int(example[1]), items=item_list)

        # add the title "Example_x" to the first cell of the current output_row_index:
        output_sheet.update_cell(output_row_index, 1, example[0])

        # add each bin to a cell in the following way:
        # for bin i (0-end) : add the bin contents to cell i+2
        # that's because the worksheet index start with 1 instead of 0, and the first cell is the title "Example_x"
        # so bin0 -> cell2, bin1 -> cell3 etc.
        for i in range(bin_completion_result.num):
            bin_data = bin_completion_result.bin_to_str(i)
            output_col_index = i + 2
            output_sheet.update_cell(output_row_index, output_col_index, bin_data)

        output_row_index += 1

        print("Updated result for input: ", item_list)


if __name__ == "__main__":
    bin_completions_sheets()

