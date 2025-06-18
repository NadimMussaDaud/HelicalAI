from nicegui import ui

with ui.splitter(value=30).classes('w-full h-56') as splitter:
    with splitter.before:
        with ui.tabs().props('vertical').classes('w-full') as tabs:
            mail = ui.tab('Mails', icon='mail')
            alarm = ui.tab('Alarms', icon='alarm')
            movie = ui.tab('Movies', icon='movie')
    with splitter.after:
        with ui.tab_panels(tabs, value=mail) \
                .props('vertical').classes('w-full h-full'):
            with ui.tab_panel(mail):
                ui.label('Mails').classes('text-h4')
                ui.label('Content of mails')
            with ui.tab_panel(alarm):
                ui.label('Alarms').classes('text-h4')
                ui.label('Content of alarms')
            with ui.tab_panel(movie):
                ui.label('Movies').classes('text-h4')
                ui.label('Content of movies')


ui.run(title="Model Workflow v2.0", port=8088)