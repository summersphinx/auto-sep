import PySimpleGUI as sg
from psgtray import SystemTray
import os

import SEP

os.makedirs(f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP', exist_ok=True)
os.chdir(f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP')
# sg.user_settings_delete_filename(filename='settings.json', path=f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP')
sg.user_settings_filename(path=f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP', filename='settings.json')

if sg.user_settings_file_exists(filename='auto-settings.json'):
    sg.user_settings_load(filename='auto-settings.json')
else:
    sg.user_settings_set_entry('id', '')
    sg.user_settings_set_entry('exclude', [])
    sg.user_settings_set_entry('filter_songs', True)
    sg.user_settings_save(filename='auto-settings.json')

settings = sg.UserSettings(path=f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP', filename='auto-settings.json')

def id(wn):
    global settings
    while True:
        wn['output'].Update(value='')
        sg.cprint(f'Current ID: {settings["id"]}')
        sg.cprint('Change? [1] Yes    [2] No')
        event, val = wn.read()

        if event == '1':
            temp = sg.popup_get_text('New Playlist ID ->', '', settings['id'])
            if temp is not None:
                settings['id'] = temp
        elif event == '2':
            break


def run(wn):
    global settings
    while True:
        wn['output'].Update(value='')
        sg.cprint(f'Launch on Startup?: {settings["run"]}')
        sg.cprint('Change? [1] Yes    [2] No')
        event, val = wn.read()

        if event == '1':
            settings['run'] = sg.popup_yes_no('Launch on Startup?') == 'Yes'
        elif event == '2':
            break


def notify(wn):
    global settings
    while True:
        wn['output'].Update(value='')
        sg.cprint(f'Send Notifications?: {settings["notifications"]}')
        sg.cprint('Change? [1] Yes    [2] No')
        event, val = wn.read()

        if event == '1':
            settings['notifications'] = sg.popup_yes_no('Send Notifications?') == 'Yes'
        elif event == '2':
            break


def sett(wn):
    global settings
    while True:
        wn['output'].Update(value='')
        sg.cprint(f'♫ AUTO SEP SETTINGS ♫\n\n')
        keys = list(settings.read().keys())
        for each in range(len(keys)):
            sg.cprint(f'[{each + 1}]   {keys[each]}   ==   {settings[keys[each]]}')
        sg.cprint(f'[0]   Close   ==   Close the settings')
        sg.cprint('Enter the number for what you want to change . . .')
        for i in range(10):
            wn.bind(str(i), str(i))
        event, values = wn.read()

        if event == '1':
            id(wn)
        if event == '2':
            run(wn)
        if event == '4':
            notify(wn)

        if event == '0':
            break
    wn.hide()


def main():
    menu = ['',
            ['Force Run', 'Update Every', ['1 Hour', '1 Day', '1 Month'], '---', 'Settings', 'Exit']]
    tooltip = 'Auto SEP'

    layout = [
        [sg.Multiline('', disabled=True, autoscroll=True, auto_refresh=True, size=(50, 20), reroute_cprint=True,
                      k='output')]
    ]

    window = sg.Window('Window Title', layout, finalize=True, no_titlebar=True)
    window.hide()

    tray = SystemTray(menu, single_click_events=True, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('Auto SEP', 'Auto SEP Started')
    while True:
        event, values = window.read()

        print(event)
        print()
        print(values)

        # IMPORTANT step. It's not required, but convenient. Set event to value from tray
        # if it's a tray event, change the event variable to be whatever the tray sent
        if event == tray.key:
            event = values[event]  # use the System Tray's event as if was from the window
        print(event)

        if event in ['Settings', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED]:
            window.un_hide()
            window.bring_to_front()
            sett(window)

        if event in ['Close']:
            pass

        if event in ['Exit']:
            break

        if event == 'Force Run':
            SEP.run()
            tray.show_message('Auto SEP', 'Auto SEP Finished!')


if __name__ == '__main__':
    pass
    main()
