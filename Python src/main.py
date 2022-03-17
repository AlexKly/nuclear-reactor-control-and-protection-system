# Import libraries and params:
import tkinter as tk
import os
import pandas as pd
import numpy as np
from scipy import interpolate
from inspect import getsourcefile
from os.path import abspath

# Path to datatable:
PATH_DATATABLE = 'table/'
LIST_SHEETS = ['Лист1', 'Лист2']
LIST_COLUMNS = ['Столбец 1', 'Столбец 2']

# Main params:
NAME_WINDOW = "Interpolation"
SIZE_WINDOW = "200x350"
NAME_INSIDE_BOX = "Select a sheet"
NAME_COLUMN = 'Select a column'
MAIN_TITLES = {
    'name_window': NAME_WINDOW,
    'size_window': SIZE_WINDOW,
    'name_inside': NAME_INSIDE_BOX,
    'name_column': NAME_COLUMN,
}

# Button's titles:
TITLE_BUTTON_CALC_FIELD = 'Perform interpolation'
TITLE_BUTTON_GET_VALUE = 'Get value'
TITLE_BUTTON_SUBMIT_SHEET = 'Submit'
TITLES_BUTTONS = {
    'calc_field': TITLE_BUTTON_CALC_FIELD,
    'get_value': TITLE_BUTTON_GET_VALUE,
    'submit_params': TITLE_BUTTON_SUBMIT_SHEET
}

# Field's labels:
LABELS = ['Input value -->', 'Input column -->', 'Output column <--']

global X, Y
global TABLE_SHEET


def mainActivity() -> None:
    root = tk.Tk()
    root.title(MAIN_TITLES['name_window'])
    root.geometry(MAIN_TITLES['size_window'])
    root.resizable(width=False, height=False)
    root.attributes('-toolwindow', True)

    # List for choosing sheet in excel doc:
    value_inside = tk.StringVar(root)
    value_inside.set(MAIN_TITLES['name_inside'])
    list_box = tk.OptionMenu(root, value_inside, *LIST_SHEETS)
    list_box.pack(side=tk.TOP)
    b1 = tk.Button(root, text=TITLES_BUTTONS['submit_params'], command=lambda: chooseSheet(value=value_inside))
    b1.pack(side=tk.TOP, padx=5, pady=5)

    # Create the fields to input:
    entries = makeForm(root=root, fields=LABELS, name_column=MAIN_TITLES['name_column'], list_params=LIST_COLUMNS)

    # Create filed to output result:
    text = tk.Text(root, height=1, width=52)
    text.pack(side=tk.TOP, padx=5, pady=5)

    # Buttons:
    b2 = tk.Button(root, text=TITLES_BUTTONS['calc_field'], command=lambda: calcField())
    b3 = tk.Button(root, text=TITLES_BUTTONS['get_value'], command=lambda: getValue(text_win=text,
                                                                                    entries=entries,
                                                                                    name_columns=LIST_COLUMNS))
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3.pack(side=tk.LEFT, padx=5, pady=5)

    # Start processing main window:
    root.mainloop()


def makeForm(root: tk.Tk, fields: list, name_column: str, list_params: list) -> dict:
    entries = {}
    ind = 0
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=5,
                 pady=5)
        lab.pack(side=tk.TOP)
        if ind == 0:
            ent = tk.Entry(row)
            ent.insert(0, "0")
            ent.pack(side=tk.RIGHT,
                     expand=tk.YES,
                     fill=tk.X)
            entries[field] = ent
        else:
            value_inside = tk.StringVar(root)
            value_inside.set(name_column)
            list_box = tk.OptionMenu(root, value_inside, *list_params)
            list_box.pack(side=tk.TOP,
                          expand=tk.YES,
                          fill=tk.X,
                          padx=5,
                          pady=5)
            entries[field] = value_inside
        ind = ind + 1

    return entries


def calcField() -> None:
    global X, Y
    global TABLE_SHEET
    files = os.listdir(abspath(getsourcefile(lambda: 0))[:-7] + PATH_DATATABLE)
    df = pd.read_excel(abspath(getsourcefile(lambda: 0))[:-7] + PATH_DATATABLE + files[0],
                       sheet_name=TABLE_SHEET,
                       dtype=np.float64)
    X = np.array(df.index)
    Y = np.array(df.values)


def getValue(text_win: tk.Text, entries: dict, name_columns: list) -> None:
    global X, Y
    # Step 1: Read input and output columns and input value:
    y_input = float(entries[LABELS[0]].get())
    y_column_input = chooseColumn(value=entries[LABELS[1]].get(), list_columns=name_columns)
    y_column_output = chooseColumn(value=entries[LABELS[2]].get(), list_columns=name_columns)

    # Step 2: Calc values for the input and output columns:
    f_input = interpolate.interp1d(X, Y[:, y_column_input], kind='cubic')
    f_output = interpolate.interp1d(X, Y[:, y_column_output], kind='cubic')

    # Step 3: Add x vector with a small step:
    x_scaling = np.linspace(X[0], X[-1], 10000)
    y_scaling = f_input(x_scaling)

    # Step 4: Find the nearest value in y vector to x:
    min_diff = abs(y_input - y_scaling[0])
    index_min_diff = 0
    for i in range(y_scaling.shape[0]):
        if np.abs(y_input - y_scaling[i]) < min_diff:
            min_diff = np.abs(y_input - y_scaling[i])
            index_min_diff = i

    y_output = f_output(x_scaling[index_min_diff])

    text_win.delete(1.0, tk.END)
    text_win.insert(tk.END, "{:.4f}".format(y_output))


def chooseSheet(value: tk.StringVar) -> None:
    global TABLE_SHEET
    TABLE_SHEET = value.get()


def chooseColumn(value: str, list_columns: list) -> int:
    return list_columns.index(value)


def main() -> None:
    mainActivity()


if __name__ == '__main__':
    main()
