import flet as ft

def main(page: ft.Page):
    def page_change(e):
        if len(page.controls) > 0:
            page.controls.clear()
            page.update()
        if page.navigation_bar.selected_index == 0:
            settings_page(e)
            page.update()
        if page.navigation_bar.selected_index == 1:
            home_page(e)
            page.update()
        if page.navigation_bar.selected_index == 2:
            tasks_page(e)
            page.update()

    def settings_page(e):
        s_page_text = ft.Text("This is the settings page")
        page.add(s_page_text)

    def home_page(e):
        h_page_text = ft.Text("This is the home page")
        page.add(h_page_text)

    def tasks_page(e):
        t_page_text = ft.Text("This is the task page")
        page.add(t_page_text)

    def add_event(e):
        pass
    
    
    page.theme_mode = ft.ThemeMode.LIGHT #other options include LIGHT and SYSTEM
    title_text = ft.Text("My Fancy Application")
    page.appbar = ft.AppBar(
    title = title_text,
    center_title = True
    )
    nav1 = ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings")
    nav2 = ft.NavigationDestination(icon=ft.icons.HOME, label="Home")
    nav3 = ft.NavigationDestination(icon=ft.icons.TASK, label="Tasks")
    page.navigation_bar = ft.NavigationBar(
    destinations = [nav1, nav2, nav3], #the destingations we created
    selected_index = 1, #home nav
    on_change = page_change #function called when navigation button clicked
    )
    page.floating_action_button = ft.FloatingActionButton(text = "Add Entry", icon=ft.icons.ADD, on_click=add_event)
    page.add(ft.Text(""))
ft.app(main, assets_dir="assets")
