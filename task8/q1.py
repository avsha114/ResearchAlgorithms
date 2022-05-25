"""
    This program gets a table of members of the knesset from the knesset server.
    Then it creates the same table on a local DB file.

    DB origin: http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Person

    Author: Avshalom Avraham
"""

import logging
import sqlite3
import requests
import xmltodict


# This function gets a key and returns the value of that key
def get_value(data: dict, key: str):
    # Email can be null so we need to check it
    if key == 'd:Email':
        try:
            if data[key]['@m:null'] == 'true':
                return None
        except:
            pass

    # some fields have '#text' key and some not:
    try:
        return data[key]['#text']
    except:
        return data[key]


# This function gets the DB from the knesset server and copy it to a local file
def duplicate_db():
    response = requests.get("http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Person")
    assert response.status_code == 200 # SUCCESS

    # The response is in XML formal. We parse it to a dictionary.
    data_dict = xmltodict.parse(response.content)

    # Create a new local DB:
    db = sqlite3.connect('knesset.db')
    cursor = db.cursor()
    try:
        cursor.execute('''
            CREATE TABLE KNS_Person(
                PersonID INTEGER,
                LastName TEXT,
                FirstName TEXT,
                GenderID  INTEGER,
                GenderDesc TEXT,
                Email TEXT,
                IsCurrent INTEGER,
                LastUpdatedDate TEXT)
        ''')
    except sqlite3.OperationalError as err:
        # if table already exist - skip the error and continue as usual
        # for any other error - return
        if err.__str__() != 'table KNS_Person already exists':
            return

    for entry in data_dict['feed']['entry']:
        data = entry['content']['m:properties']

        person_id = int(get_value(data=data, key='d:PersonID'))  # Convert to INTEGER
        last_name = get_value(data=data, key='d:LastName')  # TEXT
        first_name = get_value(data=data, key='d:FirstName')  # TEXT
        gender_id = int(get_value(data=data, key='d:GenderID'))  # Convert to INTEGER
        gender_desc = get_value(data=data, key='d:GenderDesc')  # TEXT
        email = get_value(data=data, key='d:Email')  # TEXT or None
        is_current = get_value(data=data, key='d:IsCurrent').upper()  # SQLite can get 'TRUE' or 'FALSE' instead INTEGER
        last_updated_date = get_value(data=data, key='d:LastUpdatedDate') # SQLite can handle formatted text as dates

        values = [person_id, last_name, first_name, gender_id, gender_desc, email, is_current, last_updated_date]

        # Try to insert each entry:
        try:
            cursor.execute('''
                        INSERT INTO KNS_Person(PersonID, LastName, FirstName, GenderID, GenderDesc, Email, IsCurrent, LastUpdatedDate)
                        VALUES(?,?,?,?,?,?,?,?)
                        ''', values)
        except sqlite3.InterfaceError as err:
            # Let the user know which entry had the error:
            logging.info(f"ERROR inserting: {values} due to {err.__str__()}")

    # print the top 20 entries as examples:
    cursor.execute('''
                SELECT * FROM KNS_Person LIMIT 20
                ''')
    for entry in cursor:
        print(entry)


if __name__ == "__main__":
    duplicate_db()
