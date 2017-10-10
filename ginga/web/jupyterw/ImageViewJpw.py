#
# ImageViewJpw.py -- Module for a Ginga FITS viewer in a Jupyter web notebook.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
"""
This example illustrates using a Ginga as the driver of a Jupyter web widget.

Basic usage in a Jupyter notebook:

import ipywidgets as widgets

# create a Jupyter image that will be our display surface
# format can be 'jpeg' or 'png'; specify width and height to set viewer size
jp_img = widgets.Image(format='jpeg', width=500, height=500)

# Boilerplate to create a Ginga viewer connected to this widget
# this could be simplified by creating a class that created viewers
# as a factory.
from ginga.misc.log import get_logger
logger = get_logger("v1", log_stderr=True, level=40)

from ginga.web.jupyterw.ImageViewJpw import EnhancedCanvasView
v1 = EnhancedCanvasView(logger=logger)
v1.set_widget(jp_img)

bd = v1.get_bindings()
bd.enable_all(True)

# You can now build a GUI with the image widget and other Jupyter
# widgets.  Here we just show the image widget.
v1.embed()

"""
import ipywidgets

# TODO: try for Agg backend first and fall back to PIL if not available
from ginga.pilw.ImageViewPil import ImageViewPil as ImageView
from ginga import AstroImage
from ginga import Mixins, Bindings
from ginga.canvas.mixins import DrawingMixin, CanvasMixin, CompoundMixin
from ginga.util.toolbox import ModeIndicator

from ginga.web.jupyterw import JpHelp


class ImageViewJpw(ImageView):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageView.__init__(self, logger=logger,
                           rgbmap=rgbmap,
                           settings=settings)

        self.jp_img = None
        self.jp_dom = None

        self._defer_task = None
        self.msgtask = None

    def set_widget(self, jp_img):
        """Call this method with the Jupyter image widget (image_w) and
        DOM widget (dom_w) that will be used.
        """
        self.jp_img = jp_img

        # TODO: need configure (resize) event callback

        # see reschedule_redraw() method
        self._defer_task = JpHelp.Timer()
        self._defer_task.add_callback('expired',
                                      lambda timer: self.delayed_redraw())
        self.msgtask = JpHelp.Timer()
        self.msgtask.add_callback('expired',
                                  lambda timer: self.onscreen_message(None))

        # for some reason these are stored as strings!
        wd, ht = int(jp_img.width), int(jp_img.height)
        self.configure_surface(wd, ht)

    def get_widget(self):
        return self.jp_img

    def update_image(self):
        fmt = self.jp_img.format
        web_img = self.get_rgb_image_as_bytes(format=fmt)

        # this updates the model, and then the Jupyter image(s)
        self.jp_img.value = web_img

    def reschedule_redraw(self, time_sec):
        self._defer_task.stop()
        self._defer_task.start(time_sec)

    def configure_window(self, width, height):
        self.configure_surface(width, height)

    def _resize_cb(self, event):
        self.configure_window(event.width, event.height)

    def set_cursor(self, cursor):
        # TODO
        pass

    def onscreen_message(self, text, delay=None, redraw=True):
        if self.jp_img is None:
            return
        self.msgtask.stop()
        self.set_onscreen_message(text, redraw=redraw)
        if delay is not None:
            self.msgtask.start(delay)


class ImageViewEvent(ImageViewJpw):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageViewJpw.__init__(self, logger=logger, rgbmap=rgbmap,
                              settings=settings)

        # Does widget accept focus when mouse enters window
        self.enter_focus = self.t_.get('enter_focus', True)

        self._button = 0

        # maps DOMListener events to callback handlers
        self._evt_dispatch = {
            'mousedown': self.button_press_event,
            'mouseup': self.button_release_event,
            'mousemove': self.motion_notify_event,
            'wheel': self.scroll_event,
            'mouseenter': self.enter_notify_event,
            'mouseleave': self.leave_notify_event,
            'keydown': self.key_press_event,
            'keyup': self.key_release_event,
            }

        # mapping from DOMListener key events to ginga key events
        self._keytbl = {
            'shiftleft': 'shift_l',
            'shiftright': 'shift_r',
            'controlleft': 'control_l',
            'controlright': 'control_r',
            'altleft': 'alt_l',
            'altright': 'alt_r',
            'osleft': 'super_l',
            'osright': 'super_r',
            'contextmenu': 'menu_r',
            'backslash': 'backslash',
            'space': 'space',
            'escape': 'escape',
            'enter': 'return',
            'tab': 'tab',
            'arrowright': 'right',
            'arrowleft': 'left',
            'arrowup': 'up',
            'arrowdown': 'down',
            'pageup': 'page_up',
            'pagedown': 'page_down',
            'f1': 'f1',
            'f2': 'f2',
            'f3': 'f3',
            'f4': 'f4',
            'f5': 'f5',
            'f6': 'f6',
            'f7': 'f7',
            'f8': 'f8',
            'f9': 'f9',
            'f10': 'f10',
            'f11': 'f11',
            'f12': 'f12',
            }

        self._keytbl2 = {
            '`': 'backquote',
            '"': 'doublequote',
            "'": 'singlequote',
            }

        # Define cursors for pick and pan
        #hand = openHandCursor()
        hand = 'fleur'
        self.define_cursor('pan', hand)
        cross = 'cross'
        self.define_cursor('pick', cross)

        for name in ('motion', 'button-press', 'button-release',
                     'key-press', 'key-release', 'drag-drop',
                     'scroll', 'map', 'focus', 'enter', 'leave',
                     ):
            self.enable_callback(name)

    def set_widget(self, jp_imgw):
        """Call this method with the Jupyter image widget (image_w) and
        DOM widget (dom_w) that will be used.
        """
        super(ImageViewEvent, self).set_widget(jp_imgw)

        self.jp_dom = ipywidgets.DOMListener(source=jp_imgw)
        self.jp_dom.watched_events = [
            'keydown', 'keyup', 'mouseenter', 'mouseleave',
            'mousedown', 'mouseup', 'mousemove', 'wheel',
            'contextmenu'
            ]
        self.jp_dom.prevent_default_action = True

        self.jp_dom.on_dom_event(self._handle_event)
        self.logger.info("installed event handlers")

        return self.make_callback('map')

    def _handle_event(self, event):
        # TODO: need focus events and maybe a map event
        # TODO: Set up widget as a drag and drop destination
        evt_kind = event['type']
        handler = self._evt_dispatch.get(evt_kind, None)
        if handler is not None:
            return handler(event)
        return False

    def transkey(self, keycode, keyname=None):
        keycode = str(keycode).lower()
        if keyname is None:
            keyname = keycode
        self.logger.debug("key code in jupyter '%s'" % (keycode))
        res = self._keytbl.get(keycode, None)
        if res is None:
            res = self._keytbl2.get(keyname, keyname)
        return res

    def get_keyTable(self):
        return self._keytbl

    def set_enter_focus(self, tf):
        self.enter_focus = tf

    def focus_event(self, event, has_focus):
        return self.make_callback('focus', has_focus)

    def enter_notify_event(self, event):
        if self.enter_focus:
            # TODO: set focus on canvas
            pass
        return self.make_callback('enter')

    def leave_notify_event(self, event):
        self.logger.debug("leaving widget...")
        return self.make_callback('leave')

    def key_press_event(self, event):
        keyname = self.transkey(event['code'], keyname=event['key'])
        self.logger.debug("key press event, key=%s" % (keyname))
        return self.make_ui_callback('key-press', keyname)

    def key_release_event(self, event):
        keyname = self.transkey(event['code'], keyname=event['key'])
        self.logger.debug("key release event, key=%s" % (keyname))
        return self.make_ui_callback('key-release', keyname)

    def button_press_event(self, event):
        x = event['arrayX']; y = event['arrayY']
        self.last_win_x, self.last_win_y = x, y

        button = 0
        button |= 0x1 << event['button']
        self._button = button
        self.logger.debug("button event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.check_cursor_location()

        return self.make_ui_callback('button-press', button, data_x, data_y)

    def button_release_event(self, event):
        x = event['arrayX']; y = event['arrayY']
        self.last_win_x, self.last_win_y = x, y

        button = 0
        button |= 0x1 << event['button']
        self._button = 0
        self.logger.debug("button release at %dx%d button=%x" % (x, y, button))

        data_x, data_y = self.check_cursor_location()

        return self.make_ui_callback('button-release', button, data_x, data_y)

    def motion_notify_event(self, event):
        button = self._button
        x = event['arrayX']; y = event['arrayY']
        self.last_win_x, self.last_win_y = x, y

        self.logger.debug("motion event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.check_cursor_location()

        return self.make_ui_callback('motion', button, data_x, data_y)

    def scroll_event(self, event):
        x = event['arrayX']; y = event['arrayY']
        self.last_win_x, self.last_win_y = x, y

        dx, dy = event['deltaX'], event['deltaY']
        # TODO: calculate actual angle of direction
        if dy < 0:
            direction = 0.0   # up
        elif dy > 0:
            direction = 180.0   # down
        else:
            return False

        # 15 deg is standard 1-click turn for a wheel mouse
        num_deg = 15.0
        self.logger.debug("scroll deg=%f direction=%f" % (
            num_deg, direction))

        data_x, data_y = self.check_cursor_location()

        return self.make_ui_callback('scroll', direction, num_deg,
                                     data_x, data_y)

class ImageViewZoom(Mixins.UIMixin, ImageViewEvent):

    # class variables for binding map and bindings can be set
    bindmapClass = Bindings.BindingMapper
    bindingsClass = Bindings.ImageViewBindings

    @classmethod
    def set_bindingsClass(cls, klass):
        cls.bindingsClass = klass

    @classmethod
    def set_bindmapClass(cls, klass):
        cls.bindmapClass = klass

    def __init__(self, logger=None, rgbmap=None, settings=None,
                 bindmap=None, bindings=None):
        ImageViewEvent.__init__(self, logger=logger, rgbmap=rgbmap,
                                settings=settings)
        Mixins.UIMixin.__init__(self)

        self.ui_set_active(True)

        if bindmap is None:
            bindmap = ImageViewZoom.bindmapClass(self.logger)
        self.bindmap = bindmap
        bindmap.register_for_events(self)

        if bindings is None:
            bindings = ImageViewZoom.bindingsClass(self.logger)
        self.set_bindings(bindings)

    def get_bindmap(self):
        return self.bindmap

    def get_bindings(self):
        return self.bindings

    def set_bindings(self, bindings):
        self.bindings = bindings
        bindings.set_bindings(self)


class CanvasView(ImageViewZoom):

    def __init__(self, logger=None, settings=None, rgbmap=None,
                 bindmap=None, bindings=None):
        ImageViewZoom.__init__(self, logger=logger, settings=settings,
                               rgbmap=rgbmap,
                               bindmap=bindmap, bindings=bindings)

        # Needed for UIMixin to propagate events correctly
        self.objects = [self.private_canvas]

        self._mi = ModeIndicator(self)

    def set_canvas(self, canvas, private_canvas=None):
        super(CanvasView, self).set_canvas(canvas,
                                           private_canvas=private_canvas)

        self.objects[0] = self.private_canvas


class EnhancedCanvasView(CanvasView):
    """
    This just adds some convenience methods to the viewer for loading images,
    grabbing screenshots, etc.  You can subclass to add new methods.
    """

    def embed(self):
        """
        Embed a viewer into a Jupyter notebook.
        """
        return self.jp_img

    def open(self, new=1):
        """
        Open this viewer in a new browser window or tab.
        """
        # TBD
        raise Exception("Not yet implemented!")

    def show(self, fmt=None):
        """
        Capture the window of a viewer.
        """
        # force any delayed redraws
        # TODO: this really needs to be addressed in get_rgb_image_as_bytes()
        # of the various superclasses, as it affects other backends as well
        self.redraw_now()

        from IPython.display import Image

        if fmt is None:
            # what format are we using for the Jupyter image--use that
            fmt = self.jp_img.format

        return Image(data=bytes(self.get_rgb_image_as_bytes(format=fmt)),
                     format=fmt, embed=True)

    def load_fits(self, filepath):
        """
        Load a FITS file into the viewer.
        """
        image = AstroImage.AstroImage(logger=self.logger)
        image.load_file(filepath)

        self.set_image(image)

    load = load_fits

    def load_hdu(self, hdu):
        """
        Load an HDU into the viewer.
        """
        image = AstroImage.AstroImage(logger=self.logger)
        image.load_hdu(hdu)

        self.set_image(image)

    def load_data(self, data_np):
        """
        Load raw numpy data into the viewer.
        """
        image = AstroImage.AstroImage(logger=self.logger)
        image.set_data(data_np)

        self.set_image(image)

    def add_canvas(self, tag=None):
        # add a canvas to the view
        my_canvas = self.get_canvas()
        DrawingCanvas = my_canvas.get_draw_class('drawingcanvas')
        canvas = DrawingCanvas()
        # enable drawing on the canvas
        canvas.enable_draw(True)
        canvas.enable_edit(True)
        canvas.set_drawtype(None)
        canvas.ui_set_active(True)
        canvas.set_surface(self)
        canvas.register_for_cursor_drawing(self)
        # add the canvas to the view.
        my_canvas.add(canvas, tag=tag)

        return canvas
