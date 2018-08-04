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
    w = Widgets.Slider(orientation='horizontal')
    w.set_limits(-10, 10, incr_value=1)
    w.set_value(4)
    vbox.add_widget(w)

elif wname == 'scrollbar':
    w = Widgets.ScrollBar(orientation='horizontal')
    w.add_callback('activated', lambda w, val: logger.info("value is %d" % val))
    vbox.add_widget(w)

elif wname == 'progressbar':
    w = Widgets.ProgressBar()
    w.set_value(0.6)
    vbox.add_widget(w)

elif wname == 'statusbar':
    w = Widgets.StatusBar()
    w.set_message("Hello, World! is my status")
    vbox.add_widget(w)

elif wname == 'image':
    w = Widgets.Image()
    w.load_file(os.path.join(icondir, 'ginga-512x512.png'))
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
    w.load_url("http://www.google.com/")
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
    w = Widgets.Splitter()
    w.add_widget(Widgets.Label('Content of Pane 1'))
    w.add_widget(Widgets.Label('Content of Pane 2'))
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
    vbox.add_widget(w, stretch=1)

elif wname == 'mdiwidget':
    w = Widgets.MDIWidget()
    w.add_widget(Widgets.Label('Content of MDI Area 1'))
    w.add_widget(Widgets.Label('Content of MDI Area 2'))
    vbox.add_widget(w, stretch=1)

elif wname == 'gridbox':
    w = Widgets.GridBox(rows=2, columns=2)
    w.add_widget(Widgets.Label('Content of Grid Area 1'), 0, 0)
    w.add_widget(Widgets.Label('Content of Grid Area 2'), 0, 1)
    w.add_widget(Widgets.Label('Content of Grid Area 3'), 1, 0)
    w.add_widget(Widgets.Label('Content of Grid Area 4'), 1, 1)
    vbox.add_widget(w, stretch=1)

elif wname == 'menubar':
    w = Widgets.Menubar()
    menu = w.add_name('Menu 1')
    menu.add_name('Larry').add_callback('activated',
                                        lambda *args: print("chose Larry"))
    menu.add_name('Curly').add_callback('activated',
                                        lambda *args: logger.info("chose Curly"))
    menu.add_name('Moe').add_callback('activated',
                                      lambda *args: logger.info("chose Moe"))
    vbox.add_widget(w)
    vbox.add_widget(Widgets.Label("App content"), stretch=1)

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

    #Create Menu Bar for QPlan
    w = Widgets.Menubar()
    menu = w.add_name('File')
    menu.add_name('Quit').add_callback('activated',
                                        lambda *args: print("Quit"))
    menu = w.add_name('Plugins')
    menu.add_name('Airmass Chart').add_callback('activated',
                                         lambda *args: logger.info("chose Airmass Chart"))
    menu.add_name('Control Panel').add_callback('activated',
                                         lambda *args: logger.info("chose Control Panel"))
    menu.add_name('Errors').add_callback('activated',
                                       lambda *args: logger.info("chose Errors"))
    menu.add_name('Log').add_callback('activated',
                                       lambda *args: logger.info("chose Log"))
    menu.add_name('Night Activity Chart').add_callback('activated',
                                       lambda *args: logger.info("chose Night Activity Chart"))
    menu.add_name('Proposal Chart').add_callback('activated',
                                       lambda *args: logger.info("chose Proposals Chart"))
    menu.add_name('Report').add_callback('activated',
                                       lambda *args: logger.info("chose Report"))
    menu.add_name('Schedule').add_callback('activated',
                                       lambda *args: logger.info("chose Schedule"))
    menu.add_name('Schedules Chart').add_callback('activated',
                                       lambda *args: logger.info("chose Schedules Chart"))
    menu.add_name('Semester Chart').add_callback('activated',
                                       lambda *args: logger.info("chose Semester Chart"))
    menu.add_name('Slew Chart').add_callback('activated',
                                       lambda *args: logger.info("chose Slew Chart"))
    vbox.add_widget(w, stretch=1)

    #Create Splitter for Qplan
    w = Widgets.Splitter()


    #For Content 1
    w.add_widget(Widgets.Label('Content of Pane 1'))

    x = Widgets.Splitter()

    #For Content 2
    vbox_2 = Widgets.VBox()
    a = Widgets.TabWidget()
    a.add_widget(Widgets.Frame(), title='Report')
    vbox_2.add_widget(a, stretch=0)
    b = Widgets.Button("Make OPE")
    b.add_callback('activated', lambda w: logger.info("Make OPE clicked"))
    vbox_2.add_widget(b, stretch=0)
    x.add_widget(vbox_2)

    #For Content 3
    a = Widgets.TabWidget()
    vbox_overall = Widgets.VBox()
    vbox_20 = Widgets.VBox()
    vbox_20.add_widget(Widgets.Label("Files"))

    hbox_10 = Widgets.HBox()
    hbox_10.add_widget(Widgets.Label("Inputs:"))
    l = Widgets.TextEntry()
    l.set_text('.')
    hbox_10.add_widget(l)
    vbox_20.add_widget(hbox_10)

    b = Widgets.Button("Load info")
    b.add_callback('activated', lambda w: logger.info("Load clicked"))
    vbox_20.add_widget(b,stretch=0)

    b = Widgets.Button("Update Current Conditions")
    b.add_callback('activated', lambda w: logger.info("Update Current Conditions clicked"))
    vbox_20.add_widget(b)

    b = Widgets.Button("Update Database from Files")
    b.add_callback('activated', lambda w: logger.info("Update Database from Files clicked"))
    vbox_20.add_widget(b)

    hbox_20 = Widgets.HBox()

    b = Widgets.Button("Build Schedule")
    b.add_callback('activated', lambda w: logger.info("Build clicked"))

    hbox_20.add_widget(b)
    hbox_20.add_widget(Widgets.CheckBox("Use QDB"))
    vbox_20.add_widget(hbox_20)
    o = Widgets.CheckBox("Remove scheduled OBs")
    o.set_state(True)
    vbox_20.add_widget(o)

    vbox_overall.add_widget(vbox_20)

    hbox_30 = Widgets.HBox()
    slider = Widgets.Slider(orientation='horizontal')
    slider.set_limits(-10, 10,incr_value=1)
    slider.set_value(4)
    hbox_30.add_widget(slider)
    hbox_30.add_widget(Widgets.TextEntrySet(text='100'))
    vbox_overall.add_widget(hbox_30)

    a.add_widget(vbox_overall, title='Control Panel')
    a.add_widget(Widgets.Button("Remove All"), title='Errors')
    vbox_5 = Widgets.VBox()
    vbox_5.add_widget(a, stretch=1)
    x.add_widget(vbox_5)

    y = Widgets.Splitter()

    #For Content 4
    vbox_4 = Widgets.VBox()
    a = Widgets.TabWidget()
    a.add_widget(Widgets.Frame(), title='Airmass Chart')
    a.add_widget(Widgets.Frame(), title='Night Activity Chart')
    a.add_widget(Widgets.Frame(), title='Proposals Chart')
    a.add_widget(Widgets.Frame(), title='Schedules Chart')
    a.add_widget(Widgets.Frame(), title='Semester Chart')
    vbox_4.add_widget(a, stretch=1)
    y.add_widget(vbox_4)

    #For Content 5
    a = Widgets.TabWidget()
    a.add_widget(Widgets.Frame(), title='Slew Chart')
    y.add_widget(a)

    z = Widgets.Splitter(orientation='vertical')
    z.add_widget(x)
    z.add_widget(y)

    w.add_widget(z)
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
