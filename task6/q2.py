"""
This is a script that reads a csv file of Israel's budget and generates some new data from it.
To activate - place the CSV file in the same folder and call it "national-budget.csv".
You can find the file in: https://next.obudget.org/datapackages/budget/national/original

Author: Avshalom Avraham
"""

import pandas as pd
import numpy as np

# The data frame in which we hold the budget data:
df = pd.read_csv("national-budget.csv")


# Get the education budget for a given year.
# The function filters the dataframe by year, then by program name, then by expenses.
# Return value is the sum of all the expenses spent on education in a given year.
def education_budget(year: int) -> int:
    modified_data = df[(df["שנה"] == year) & \
                       (df["שם תכנית"].str.contains("חינוך")) & \
                       (df["הוצאה/הכנסה"] == "הוצאה")]

    return modified_data["הוצאה נטו"].sum()


# This function calculate the percentage of the security budget in comparison to the whole budget of a given year.
# First we filter the dataframe by year, then by field and by expenses.
# finally we calculate the sum of each budget and return the division between them. (*100 for percentage)
def security_budget_ratio(year: int) -> float:
    yearly_data = df[df["שנה"] == year]
    security_data = yearly_data[(yearly_data["שם סעיף"] == "משרד הבטחון") & \
                                (yearly_data["הוצאה/הכנסה"] == "הוצאה")]

    yearly_budget = yearly_data["הוצאה נטו"].sum()
    security_budget = security_data["הוצאה נטו"].sum()

    return (security_budget / yearly_budget) * 100


# This function finds the year with the biggest budget for a certain office.
# First we filter the dataframe by office name.
# Then, we go through each year and sum up all the expenses of that year.
# We update the max_year and max_budget variables each iteration if needed and return max_year in the end,
def largest_budget_year(office: str) -> int:
    office_data = df[df["שם סעיף"] == office]

    (max_year, max_budget) = (0, -1)
    for year in df["שנה"].unique():
        budget_per_year = office_data[office_data["שנה"] == year]["הוצאה נטו"].sum()
        if (budget_per_year > max_budget):
            (max_year, max_budget) = (year, budget_per_year)

    return max_year


# This function calculates the average security budget in a given year range,
# First we build the year range variable.
# Then we go through each year in range and calculate the sum of expenses and add it to the budgets list.
# Finally, we return the average of all budgets with numpy.mean() function.
def security_budget_average(start_year: int, end_year: int) -> float:
    budgets = []
    year_range = range(start_year, end_year) if end_year != start_year else [start_year]

    for year in year_range:
        yearly_data = df[df["שנה"] == year]
        security_data = yearly_data[(yearly_data["שם תחום"] == "בטחון") & \
                                    (yearly_data["הוצאה/הכנסה"] == "הוצאה")]
        budgets.append(security_data["הוצאה נטו"].sum())

    return np.mean(budgets)


if __name__ == '__main__':

    # Education budget test:
    print("The education budget in 1998 is:", education_budget(1998))
    print("The education budget in 2000 is:", education_budget(2000))
    print("The education budget in 2009 is:", education_budget(2009))
    print("The education budget in 2015 is:", education_budget(2015))
    print()

    # Security budget ration test:
    print("The security budget in 1999 was ", round(security_budget_ratio(1999), 2), "% of the whole budget.")
    print("The security budget in 2002 was ", round(security_budget_ratio(2002), 2), "% of the whole budget.")
    print("The security budget in 2005 was ", round(security_budget_ratio(2005), 2), "% of the whole budget.")
    print("The security budget in 2010 was ", round(security_budget_ratio(2010), 2), "% of the whole budget.")
    print()

    # Year with the largest budget test:
    print("The year with the largest budget for Security was: ", largest_budget_year("משרד הבטחון"))
    print("The year with the largest budget for Education was: ", largest_budget_year("משרד התחבורה"))
    print("The year with the largest budget for Health was: ", largest_budget_year("משרד הבריאות"))
    print()

    # Security budget average test:
    print("The average budget in 1999-2002 was:", security_budget_average(1999, 2002))
    print("The average budget in 2003-2015 was:", security_budget_average(2003, 2015))
    print("The average budget in 2010-2020 was:", security_budget_average(2010, 2020))
    print("The average budget in 1997-2010 was:", security_budget_average(1997, 2010))
