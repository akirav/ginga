"""
Test program for trying widgets in the different wrapped toolkits supported
by Ginga.

Usage:
  $ python widgets.py <toolkit-name> <widget-name> [logging options]

Examples:
  $ python widgets.py qt5 gridbox
  $ python widgets.py gtk3 label
  $ python widgets.py pg button
"""
from __future__ import print_function
import sys
import os

from ginga.misc import log
import ginga.toolkit as ginga_toolkit

# decide our toolkit, then import
tkit = sys.argv[1]
wname = sys.argv[2]

ginga_toolkit.use(tkit)
from ginga.gw import Widgets, Viewers, GwHelp  # noqa
from ginga.util.paths import icondir  # noqa

top = None


def quit(*args):
    if top is not None:
        top.delete()
    sys.exit()


def popup_dialog(parent):
    dia = Widgets.Dialog(title="Dialog Title",
                         buttons=[('ok', 0), ('cancel', 1)],
                         parent=parent, modal=True)
    cntr = dia.get_content_area()
    cntr.add_widget(Widgets.Label("My Dialog Content"))
    dia.show()


logger = log.get_logger('test', log_stderr=True, level=20)

app = Widgets.Application(logger=logger)
app.script_imports.append('jqx')
app.add_callback('shutdown', quit)
top = app.make_window("Ginga Wrapped Widgets Example: %s" % (wname))
top.add_callback('close', quit)

vbox = Widgets.VBox()
vbox.set_border_width(2)
vbox.set_spacing(1)

dia = None

if wname == 'label':
    w = Widgets.Label("Hello World label")
    vbox.add_widget(w, stretch=1)

elif wname == 'button':
    w = Widgets.Button("Press me")
    w.add_callback('activated', lambda w: logger.info("button was clicked"))
    w.add_callback('activated', lambda w: popup_dialog(top))
    vbox.add_widget(w, stretch=1)

elif wname == 'textentry':
    w = Widgets.TextEntry()
    w.set_text("Hello, World!")
    vbox.add_widget(w, stretch=1)

elif wname == 'textentryset':
    w = Widgets.TextEntrySet()
    w.set_text("Hello, World!")
    vbox.add_widget(w, stretch=1)

elif wname == 'textarea':
    w = Widgets.TextArea(editable=True)
    w.set_text("Hello, World!")
    vbox.add_widget(w, stretch=1)

elif wname == 'checkbox':
    w = Widgets.CheckBox("Check me")
    vbox.add_widget(w, stretch=1)

elif wname == 'togglebutton':
    w = Widgets.ToggleButton("Toggle me")
    vbox.add_widget(w, stretch=1)

elif wname == 'radiobutton':
    w = Widgets.RadioButton("Option 1")
    vbox.add_widget(w)
    vbox.add_widget(Widgets.RadioButton("Option 2", group=w))
    vbox.add_widget(Widgets.RadioButton("Option 3", group=w))

elif wname == 'combobox':
    w = Widgets.ComboBox()
    for name in ["Larry", "Curly", "Moe"]:
        w.append_text(name)
    vbox.add_widget(w)

elif wname == 'spinbox':
    w = Widgets.SpinBox(dtype=int)
    w.set_limits(-10, 10, incr_value=1)
    w.set_value(4)
    vbox.add_widget(w)

elif wname == 'slider':
    #buttons take in either true or false
    w = Widgets.Slider(orientation='vertical', buttons = 'false')
    w.set_limits(-10, 10,incr_value=1)
    w.set_value(4)
    vbox.add_widget(w)

elif wname == 'scrollbar':
    #buttons take in either true or false
    w = Widgets.ScrollBar(orientation='vertical',buttons = 'false')
    w.add_callback('activated', lambda w, val: logger.info("value is %d" % val))
    vbox.add_widget(w)

elif wname == 'progressbar':
    w = Widgets.ProgressBar(orientation='vertical')
    w.set_value(0.6)
    vbox.add_widget(w)

elif wname == 'statusbar':
    w = Widgets.StatusBar()
    w.set_message("Hello, World! is my status")
    vbox.add_widget(w)

elif wname == 'image':
    w = Widgets.Image()
    w.load_file(os.path.join(icondir, 'ginga-512x512.png'))
    w.add_callback('activated', lambda w: logger.info("Image was clicked"))
    w.set_size(256,256)

    vbox.add_widget(w)

elif wname == 'treeview':
    w = Widgets.TreeView(selection='single', sortable=True,
                         use_alt_row_color=True)
    columns = [("Meal", 'meal'), ("Critic 1", 'review1'),
               ("Critic 2", 'review2'), ("Critic 3", 'review3')]
    w.setup_table(columns, 1, 'meal')
    tree = dict(Breakfast=dict(meal='Breakfast', review1="Delish!",
                               review2="Ugh!", review3="Meh"),
                Lunch=dict(meal='Lunch', review1="Gross!",
                           review2="Interesting...", review3="Meh"),
                Supper=dict(meal='Supper', review1="Meh",
                            review2="Meh", review3="Jolly good!"))
    w.set_tree(tree)
    vbox.add_widget(w, stretch=1)

elif wname == 'webview':
    w = Widgets.WebView()
    w.load_url("https://subarutelescope.org/")
    vbox.add_widget(w)

elif wname == 'frame':
    w = Widgets.Frame(title="Frame Title")
    w.set_widget(Widgets.Label("Framed content"))
    vbox.add_widget(w)

elif wname == 'expander':
    w = Widgets.Expander(title="Expander Title")
    w.set_widget(Widgets.Label("Expander content"))
    vbox.add_widget(w)

elif wname == 'hbox':
    w = Widgets.HBox()
    w.add_widget(Widgets.Label("Item 1"), stretch=0)
    w.add_widget(Widgets.Label("Item 2"), stretch=1)
    vbox.add_widget(w)

elif wname == 'vbox':
    w = Widgets.VBox()
    w.add_widget(Widgets.Label("Item 1"), stretch=0)
    w.add_widget(Widgets.Label("Item 2"), stretch=1)
    vbox.add_widget(w)

elif wname == 'splitter':
    #
    #Example on how to use the splitter
    #       |-----------|
    #       |     1     |
    #       |___________|
    #       |  2  | 3   |
    #       |_____|_____|
    #
    #       w = Widgets.Splitter(orientation='horizontal')
    #       w.set_limits('600px','800px')
    #       w.add_widget(Widgets.Label('1'))
    #       w.add_split('vertical')
    #       w.add_widget(Widgets.Label('2'))
    #       w.add_widget(Widgets.Label('3'))
    #

    w = Widgets.Splitter(orientation='horizontal')
    w.set_limits('600px','800px')
    w.add_split('horizontal')

    #w.add_widget(Widgets.Label('Content of Pane 1'))
    v = Widgets.VBox()

    #Add Widgetss in here with the variable set to x
    x = Widgets.Menubar()
    menu = x.add_name('Menu 1')
    menu.add_name('Larry').add_callback('activated',
                                        lambda *args: print("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda *args: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda *args: logger.info("chose Moe"))
    #vbox.add_widget(x)
    menu = x.add_name('Menu 2')
    menu.add_name('Larry').add_callback('activated',
                                        lambda *args: print("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda *args: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda *args: logger.info("chose Moe"))

    v.add_widget(x)
    w.add_widget(v)

    w.add_widget(Widgets.Label('Content of Pane 2'))
    #v = Widgets.Slider(orientation='horizontal', buttons = 'false')
    #v.set_limits(-10, 10,incr_value=1)
    #v.set_value(4)
    #w.add_widget(v)

    w.add_split('vertical')
    w.add_split('horizontal')
    w.add_widget(Widgets.Label('Content of Pane 3'))
    w.add_split('horizontal')
    w.add_widget(Widgets.Label('Content of Pane 4'))
    w.add_widget(Widgets.Label('Content of Pane 5'))
    #w.add_widget(Widgets.Label('Content of Pane 6'))

    v = Widgets.Slider(orientation='vertical', buttons = 'false')
    v.set_limits(-10, 10,incr_value=1)
    v.set_value(4)
    #w.add_widget(vbox.add_widget(v, stretch=1))
    w.add_widget(v)

    vbox.add_widget(w, stretch=1)




elif wname == 'scrollarea':
    w = Widgets.ScrollArea()
    img = Widgets.Image()
    img.load_file(os.path.join(icondir, 'ginga-512x512.png'))
    w.set_widget(img)
    vbox.add_widget(w, stretch=1)

elif wname == 'tabwidget':
    w = Widgets.TabWidget()
    w.add_widget(Widgets.Label('Content of Tab 1'), title='Tab 1')
    w.add_widget(Widgets.Label('Content of Tab 2'), title='Tab 2')
    hbox = Widgets.HBox()
    sbox = Widgets.SpinBox(dtype=int)
    sbox.set_limits(0, 1, incr_value=1)
    sbox.set_value(0)
    sbox.add_callback('value-changed', lambda sbx, val: w.set_index(val))
    hbox.add_widget(sbox)
    vbox.add_widget(w, stretch=1)
    vbox.add_widget(hbox, stretch=0)

elif wname == 'stackwidget':
    w = Widgets.StackWidget()
    w.add_widget(Widgets.Label('Content of Stack 1'))
    w.add_widget(Widgets.Label('Content of Stack 2'))
    #vbox.add_widget(w, stretch=1)
    hbox = Widgets.HBox()
    sbox = Widgets.SpinBox(dtype=int)
    sbox.set_limits(0, 1, incr_value=1)
    sbox.set_value(0)
    sbox.add_callback('value-changed', lambda sbx, val: w.set_index(val))
    hbox.add_widget(sbox)
    vbox.add_widget(w, stretch=1)
    vbox.add_widget(hbox, stretch=0)
    print('check')

elif wname == 'mdiwidget':
    w = Widgets.MDIWidget()
    w.add_widget(Widgets.Label('Content of MDI Area 1'),title='test1')
    w.add_widget(Widgets.Label('Content of MDI Area 2'),title='test2')
    w.add_widget(Widgets.SpinBox(dtype=int), title='test3')
    w.add_widget(Widgets.CheckBox("Check me"), title='test4')
    vbox.add_widget(w, stretch=1)

elif wname == 'gridbox':
    w = Widgets.GridBox(rows=2, columns=2)
    w.add_widget(Widgets.Label('Content of Grid Area 1'), 0, 0)
    w.add_widget(Widgets.Label('Content of Grid Area 2'), 0, 1)
    w.add_widget(Widgets.Label('Content of Grid Area 3'), 1, 0)
    w.add_widget(Widgets.Label('Content of Grid Area 4'), 1, 1)

    #Added for Testing Purposes
    w.add_widget(Widgets.Label('Content of Grid Area 5'), 2, 0)
    w.add_widget(Widgets.Label('Content of Grid Area 6'), 2, 1)
    w.add_widget(Widgets.Button('Test Button'), 3, 0)
    w.add_widget(Widgets.Button('Test Button2'), 3, 1)
    vbox.add_widget(w, stretch=1)
    #

elif wname == 'menubar':
    w = Widgets.Menubar()
    menu = w.add_name('Menu 1')
    menu.add_name('Larry').add_callback('activated',
                                        lambda *args: print("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda *args: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda *args: logger.info("chose Moe"))
    #vbox.add_widget(w)
    menu = w.add_name('Menu 2')
    menu.add_name('Larry').add_callback('activated',
                                        lambda *args: print("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda *args: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda *args: logger.info("chose Moe"))
    vbox.add_widget(w)
    #vbox.add_widget(Widgets.Label("App content"), stretch=1)

elif wname == 'toolbar':
    w = Widgets.Toolbar()
    menu = w.add_menu('Menu Type 1', mtype='tool')
    menu.add_name('Larry').add_callback('activated',
                                        lambda w: logger.info("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda w: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda w: logger.info("chose Moe"))
    menu = w.add_menu('Menu Type 2', mtype='mbar')
    menu.add_name('Frank')
    menu.add_name('Dean')
    menu.add_name('Sammy')
    w.add_widget(Widgets.Button('A Button'))
    w.add_separator()
    w.add_action("Toggle me", toggle=True)
    w.add_action(None, iconpath=os.path.join(icondir, 'hand_48.png'))
    vbox.add_widget(w)
    vbox.add_widget(Widgets.Label("App content"), stretch=1)

elif wname == 'dialog':
    dia = Widgets.Dialog(title="Dialog Title",
                         buttons=[('ok', 0), ('cancel', 1)],
                         parent=top, modal=False)
    dia.add_callback('activated',
                     lambda w, rsp: logger.info("user chose %s" % (rsp)))
    cntr = dia.get_content_area()
    cntr.add_widget(Widgets.Label("My Dialog Content"))

    # add some content to main app widget
    w = Widgets.Label("Hello World label")
    vbox.add_widget(w, stretch=1)
    hbox = Widgets.HBox()
    w = Widgets.Button("Open Dialog")
    w.add_callback('activated', lambda w: dia.show())
    hbox.add_widget(w)
    w = Widgets.Button("Close Dialog")
    w.add_callback('activated', lambda w: dia.hide())
    hbox.add_widget(w)
    vbox.add_widget(hbox)

elif wname == 'test':
    w = Widgets.Splitter()
    w.add_widget(Widgets.Label('Content of Pane 1'))
    w.add_widget(Widgets.Label('Content of Pane 2'))
    w.add_widget(Widgets.Label('Content of Pane 3'))
    vbox.add_widget(w, stretch=1)


else:
    # default to label
    logger.error("Don't understand kind of widget '%s'" % (wname))
    w = Widgets.Label("Hello World label")
    vbox.add_widget(w, stretch=1)

top.set_widget(vbox)

top.show()
top.raise_()

if dia is not None:
    dia.show()

try:
    app.mainloop()

except KeyboardInterrupt:
    print("Terminating viewer...")
    if top is not None:
        top.close()
