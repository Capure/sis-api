from bs4 import BeautifulSoup

def parse_timetable(html):
    # parse the html file
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    rows = table.find_all("tr")

    # remove the first row (table headers)
    rows = rows[1:]

    # extract the data from the table
    week = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
    }

    ITEM_TYPES = {
        "[W]": "lecture",
        "[C]": "exercise",
        "[L]": "lab",
        "[P]": "project",
    }

    def is_room(txt):
        return txt.startswith("EA") or txt.startswith("NE")

    def get_or_none(lst, idx):
        return lst[idx] if len(lst) > idx else None

    def extract_data_from_cell(cell):
        data = [x.text.strip() for x in cell.children]
        filtered_data = list(filter(lambda x: x != "", data))
        items = []
        items_idx = [i for i, item in enumerate(filtered_data) if is_room(item)]
        for i, idx in enumerate(reversed(items_idx)):
            if i == 0:
                items.append(filtered_data[idx:])
            else:
                items.append(filtered_data[idx:items_idx[-i]])
                filtered_data = filtered_data[:idx]
        items = [{ "room": get_or_none(i, 0), "type": ITEM_TYPES[get_or_none(i, 1)], "subject_name": get_or_none(i, 2), "teacher": get_or_none(i, 3), "notes": get_or_none(i, 4) } for i in items]
        return items

    for row in rows:
        cells = row.find_all("td")
        hour = cells.pop(0).text.strip()
        for i, cell in enumerate(cells):
            if cell.text.strip() != "":
                week[list(week.keys())[i]].append({ "hour": hour, "items": extract_data_from_cell(cell)})

    return week