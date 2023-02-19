import pandas as pd
import pyautogui as pg
import PySimpleGUI as sg


def main(event, vals, radio_choices):
    # get the target window
    if event in presets['preset'].to_numpy(str):
        look_up(event)

    elif event == 'search':
        search(vals)

    elif event == 'listbox':
        txt = vals['listbox'][0]
        window['s text'].update(txt)
        
    elif event == 'read':
        # get the text from the radio buttons by finding true in the list
        # use the index of the true value to get the text from the radio_choices list
        choice = [i for i, x in enumerate(radio_choices) if vals[i]][0]
        txt = radio_choices[choice]
        write_in_window(txt)
        
    else:
        print(event)


def search(vals):
    choice = vals['s text']
    # find the best match for the search
    txt = presets.loc[presets['preset'].str.contains(choice)]['text'].to_numpy()[
        0]
    write_in_window(txt+' for '+choice)


def look_up(event):
    # look up the text to send to the game
    txt = presets.loc[presets['preset'] == event]['text'].to_numpy()[0]
    write_in_window(txt)


def write_in_window(text):
    #atl + tab to the game window
    pg.hotkey('alt', 'tab')
    # pg.click(gameRegion.left+50, gameRegion.top+10)
    pg.typewrite(text)
    pg.press('enter')
    pg.hotkey('alt', 'tab')


def buttons_from_array(array):
    # make a list of buttons from an array
    # image_filename='buttonStock.png',
    result = [[sg.Button(
        f'{i}',image_size=(50, 25)) for i in array]]
    # add an exit button
    result[0].append(
        sg.Button('Exit', image_size=(50, 25)))
    return result


def add_search_listbox(ui, listbo, radio_choices=['1', '2', '3']):
    
    radio_row = [
                    [sg.Radio(txt, 1) for txt in radio_choices],
                    [sg.Button('teleport', key='read')]
                ]
    ui.append([
        [sg.Text('search a preset: ')],
        [[sg.Button('search', bind_return_key=True, image_size=(50, 25))],
         [sg.InputText(do_not_clear=False, key='s text')]],
        [[sg.Listbox(values=listbo, size=(43, 7), key='listbox',
                    enable_events=True)],radio_row],
        [sg.Multiline('', visible=False, key='debug', text_color='red')]])
    return ui


if __name__ == '__main__':
    # get the presets from the csv file and make a gui for them
    presets = pd.read_csv('Ahk_presets.csv')
    radio_choices = ['::home', '::home2','::di', '::gamble']
    # generate a gui to with n number of presets from the csv file
    layout = buttons_from_array(presets['preset'][0:5].to_numpy())
    # add a text box to the gui, names listbox, and a search button
    layout = add_search_listbox(layout, presets['preset'][5:].to_numpy(),radio_choices)
    # add a scrollable list of the presets to the gui excluding the first 5
    window = sg.Window('presets', layout, resizable=True,
                       finalize=True) # icon='nav-logo-desktop.ico'
    # driver code
    while True:
        events, values = window.Read()
        try:
            if events in ('Exit', None):
                window.Close()
                break
            else:
                main(events, values, radio_choices)
        except Exception as e:
            window['debug'].update(visible=True)
            t = f'{e} {events}'
            window['debug'].update(t)
