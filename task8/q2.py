from prtpy.packing.bin_completion import *
import gspread


def bin_completions_sheets():
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open("BinCompletion")

    try:
        input_sheet = spreadsheet.worksheet("Input")
        output_sheet = spreadsheet.worksheet("Output")
    except gspread.exceptions.WorksheetNotFound as err:
        if err.__str__() == "Input":
            print("No input worksheet was found")
            return
        if err.__str__() == "Output":
            number_of_examples = len(input_sheet.col_values(1))
            output_sheet = spreadsheet.add_worksheet(title="Output", rows=number_of_examples, cols=100)

    output_row_index = 1
    for example in input_sheet.get_all_values():
        if example[0] == "Index":
            continue

        item_list = [int(item) for item in example[2:] if item]
        bin_completion_result = bin_completion(BinsKeepingContents(), binsize=int(example[1]), items=item_list)

        output_sheet.update_cell(output_row_index, 1, example[0])
        for i in range(bin_completion_result.num):
            bin_data = bin_completion_result.bin_to_str(i)
            output_col_index = i + 2
            output_sheet.update_cell(output_row_index, output_col_index, bin_data)

        output_row_index += 1

        print("Update result for input: ", item_list)


if __name__ == "__main__":
    bin_completions_sheets()

