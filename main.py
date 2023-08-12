import flet as ft
import pandas as pd
import numpy as np


entries = pd.DataFrame({
    "Date": [
        "08/11/23", 
        "08/12/23", 
        "08/13/23",
        "08/14/23", 
        "08/15/23", 
        "08/16/23",
        ],
    "Lift Title": [
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        ],
    "Lift": [
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        ],
    "Workout Title": [
        'Scotty Smalls', 
        'Bobby Bills', 
        'Killy Kats',
        'Scotty Smalls', 
        'Bobby Bills', 
        'Killy Kats',
        ],
    "Workout": [
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups', 
        'Bobby Bills', 
        '10 Rounds for Time: 10 Pull Ups, 10 Pushups',
        ]
})
cole = pd.DataFrame({
    "Date": ["08/11/23", "08/12/23", "08/13/23"],
    "Lift Results": ["08/11/23", "08/12/23", "08/13/23"],
    "WOD Results": ["08/11/23", "08/12/23", "08/13/23"]
})


def main(page: ft.Page):
    def page_change(e):
        if len(page.controls) > 0:
            page.controls.clear()
            page.update()
        if page.navigation_bar.selected_index == 0:
            settings_page(e)
            page.update()
        if page.navigation_bar.selected_index == 1:
            date_box, date_text = home_page(ft.Page)
            page.update()
        if page.navigation_bar.selected_index == 2:
            tasks_page(e)
            page.update()

    def settings_page(e):
        s_page_text = ft.Text("This is the settings page")
        page.add(s_page_text)

    def home_page(e):
        page.floating_action_button = ft.FloatingActionButton(text = "Add Entry", icon=ft.icons.ADD, on_click=add_event)


        left_clicker = ft.IconButton(icon = ft.icons.ARROW_LEFT_OUTLINED, on_click=left_click)
        right_clicker = ft.IconButton(icon = ft.icons.ARROW_RIGHT_OUTLINED, on_click = right_click)
        options = [ft.dropdown.Option(i) for i in entries['Date'].unique()]
        date_box = ft.Dropdown(options = options, hint_text=options[-1].key, on_change=date_select, value = options[-1].key)

        row = ft.Row([left_clicker, date_box, right_clicker], alignment='center')
        date_text, workout_text, row2 = workout_card(title = 'Workout Title', workout = 'Workout')
        page.add(row, row2)
        return date_box, date_text

    def tasks_page(e):
        t_page_text = ft.Text("This is the task page")
        page.add(t_page_text)

    def add_event(e):
        print("Clicked")
        page.launch_url("www.crossfit.pages.dev", web_popup_window=True)
        page.update()

    def left_click(e):
        selected_date = date_box.value
        print(selected_date)

        index = int(entries[entries['Date'] == selected_date].index.values)
        print(index)

        if index > 0:
            previous_date = entries['Date'].iloc[index - 1]
            previous_entry = entries['Workout Title'].iloc[index - 1]
            date_box.hint_text = previous_date 
            date_box.value = previous_date
            date_text.value = previous_entry
            page.update()
        else:
            print("No previous date available.")

    def right_click(e):
        selected_date = date_box.value
        print(selected_date)

        index = int(entries[entries['Date'] == selected_date].index.values)
        print(index)
        max_entries = max(entries.index.values)

        if index < max_entries:
            previous_date = entries['Date'].iloc[index + 1]
            previous_entry = entries['Workout Title'].iloc[index + 1]
            date_box.hint_text = previous_date 
            date_box.value = previous_date
            date_text.value = previous_entry
            page.update()
        else:
            print("No previous date available.")



    def date_select(e):
        date = date_box.value
        date_index = int(entries[entries['Date'] == date].index.values)
        print(f"date index {date_index}")
        entry_text = entries['Workout Title'].iloc[date_index]
        date_data = entries['Date'].iloc[date_index]
        print(date_text)
        date_text.value = str(entry_text)
        date_box.value = str(date_data)
        page.update()

    def wod_lb(e):
        lifter_list = ['Cole']*5
        result_list = ['10:00']*5
        dlg_row = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        dlg_container = ft.Container(padding = 50)
        dlg_tbl_rows = []
        for lifter, result in zip(lifter_list, result_list):
            dlg_tbl_rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(lifter)), ft.DataCell(ft.Text(result))]))
        dlg_tbl_columns = [ft.DataColumn(ft.Text("Name")), ft.DataColumn(ft.Text("Result"))]
        dlg_table = ft.DataTable(columns=dlg_tbl_columns, rows = dlg_tbl_rows)
        dlg_container.content = dlg_table
        dlg_row.controls = [dlg_container]
        page.dialog = ft.AlertDialog(
            content=dlg_row
        )
        page.dialog.open = True
        page.scroll = ft.ScrollMode.ALWAYS
        page.update()
    def workout_card(title, workout):
        card = ft.Card(expand = True)
        column = ft.Column(alignment=ft.CrossAxisAlignment.CENTER)
        container = ft.Container(padding = 50)
        date_text = ft.Text(size = 50)
        wod_lb_btn = ft.OutlinedButton(text = 'Scores', on_click = wod_lb)
        workout_text = ft.Text(size = 24)
        column.controls = [date_text, workout_text, wod_lb_btn]
        container.content = column
        card.content = container
        date_text.value = entries[title].iloc[-1]
        workout_text.value = entries[workout].iloc[-1]
        row = ft.Row([card], alignment='center')
        return date_text, workout_text, row
    def lift_card(title, workout):
        card = ft.Card(expand = True)
        column = ft.Column(alignment=ft.CrossAxisAlignment.CENTER)
        container = ft.Container(padding = 50)
        date_text = ft.Text(size = 50)
        wod_lb_btn = ft.OutlinedButton(text = 'Leaderboard', on_click = wod_lb)
        workout_text = ft.Text(size = 24)
        column.controls = [date_text, workout_text, wod_lb_btn]
        container.content = column
        card.content = container
        date_text.value = entries[title].iloc[-1]
        workout_text.value = entries[workout].iloc[-1]
        row = ft.Row([card], alignment='center')
        return date_text, workout_text, row


    page.theme = ft.Theme(color_scheme_seed='#F8931B')
    page.theme_mode = ft.ThemeMode.LIGHT #other options include LIGHT and SYSTEM
    title_text = ft.Text("CrossFit Fairmount")
    page.appbar = ft.AppBar(
    title = title_text,
    center_title = True
    )
    page.scroll = ft.ScrollMode.ALWAYS
    nav1 = ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Data")
    nav2 = ft.NavigationDestination(icon=ft.icons.HOME, label="Home")
    nav3 = ft.NavigationDestination(icon=ft.icons.TASK, label="PR")
    page.navigation_bar = ft.NavigationBar(
    destinations = [nav1, nav2, nav3], #the destingations we created
    selected_index = 1, #home nav
    on_change = page_change #function called when navigation button clicked
    )
    date_box, date_text = home_page(ft.Page)

ft.app(main, ft.WEB_BROWSER)
