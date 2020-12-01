import gi
import img_ascii as ia

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from gi.repository import Gio
import sys


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Pic to Ascii-Art", application=app)

        ### VARIABLES ###

        self.path = ''
        self.resultado = 0

        ### CONTAINER ###

        self.grid = Gtk.Grid()
        self.add(self.grid)

        ### ELEMENTS ###

        self.all_in_screen()

        ### ACTIONS ###

        # action without a state created
        new_action = Gio.SimpleAction.new("new", None)
        # action connected to the callback function
        new_action.connect("activate", self.new_callback)
        # action added to the application
        self.add_action(new_action)

        # action without a state created
        save_action = Gio.SimpleAction.new("save", None)
        # action connected to the callback function
        save_action.connect("activate", self.save_callback)
        # action added to the application
        self.add_action(save_action)

        # action without a state created (name, parameter type)
        login_action = Gio.SimpleAction.new("login", None)
        # connected with the callback function
        login_action.connect("activate", self.login_callback)
        # added to the window
        self.add_action(login_action)

        # action without a state created (name, parameter type)
        logout_action = Gio.SimpleAction.new("logout", None)
        # connected with the callback function
        logout_action.connect("activate", self.logout_callback)
        # added to the window
        self.add_action(logout_action)

        # action with a state created (name, parameter type, initial state)
        shape_action = Gio.SimpleAction.new_stateful(
            "shape", GLib.VariantType.new('s'), GLib.Variant.new_string('line'))
        # connected to the callback function
        shape_action.connect("activate", self.shape_callback)
        # added to the window
        self.add_action(shape_action)

        # action with a state created
        about_action = Gio.SimpleAction.new("about", None)
        # action connected to the callback function
        about_action.connect("activate", self.about_callback)
        # action added to the application
        self.add_action(about_action)

        # action with a state created
        source_action = Gio.SimpleAction.new("source", None)
        # action connected to the callback function
        source_action.connect("activate", self.source_callback)
        # action added to the application
        self.add_action(source_action)

    def all_in_screen(self):
        scale_lbl = Gtk.Label(label='Scale (percentage)')
        adjustment = Gtk.Adjustment(upper=200,
        step_increment=1, page_increment=10)
        self.scale_btn = Gtk.SpinButton()
        self.scale_btn.set_adjustment(adjustment)
        self.scale_btn.set_value(50)
        self.grid.attach(scale_lbl,1,6,2,1)
        self.grid.attach(self.scale_btn,1,7,2,1)

        generate_btn = Gtk.Button(label='Generate\nimage')
        generate_btn.connect("clicked", self.gen)
        self.grid.attach(generate_btn,5,6,2,2)

        tuit_btn = Gtk.Button(label='Share with\nTwitter')
        tuit_btn.connect("clicked", self.tuitear)
        self.grid.attach(tuit_btn,5,9,2,1)

        invertcolors = Gtk.Button(label='invert image\ncolors')
        invertcolors.connect("clicked", self.inversion)
        self.grid.attach(invertcolors,5,8,2,1)

        quality_lbl = Gtk.Label(label='Quality')
        quality_btn = Gtk.ListStore(str)
        opciones = [''.join(i[1]) for i in ia.chars.items()]
        for opcion in opciones:
            quality_btn.append([opcion])
        self.quality_combo = Gtk.ComboBox.new_with_model(quality_btn)
        renderer_text = Gtk.CellRendererText()
        self.quality_combo.pack_start(renderer_text, True)
        self.quality_combo.add_attribute(renderer_text, "text", 0)
        self.grid.attach(quality_lbl,9,6,2,1)
        self.grid.attach(self.quality_combo,9,7,2,1)

    def inversion(self, widget):
        if self.resultado != 0:
            self.resultado.invertc()
        else:
            print('no generaste la imagen')

    def tuitear(self, widget):
        if self.resultado != 0:
            try:
                self.resultado.tweet()
                print('done')
            except:
                print('Imagen muy pesada')
        else:
            print('no generaste la imagen')

    def gen(self, widget):
        if self.path != '':
            tree_iter = self.quality_combo.get_active_iter()
            if tree_iter is not None:
                model = self.quality_combo.get_model()
                posibilidad = model[tree_iter][0]
                for i in ia.chars.items():
                    if list(i[1]) == posibilidad:
                        calidad = i[0]
            else:
                calidad = '16ch'

            if self.scale_btn.get_value_as_int() == 0:
                escala = 50
            else:
                escala = self.scale_btn.get_value_as_int()

            self.resultado = ia.ImgToAscii(self.path,
                escala/100,
                calidad)
            self.resultado.to_blackwhite()
            self.resultado.rescale()
            self.resultado.imgmatrix()
            self.resultado.to_pic()
        else:
            print('no se seleccionó imagen')

    # callback function for new
    def new_callback(self, action, widget):
        print("You clicked \"New\"")
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.path = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    # filters for new function
    def add_filters(self, dialog):
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Images")
        filter_img.add_pattern('*.jpeg')
        filter_img.add_pattern('*.jpg')
        filter_img.add_pattern('*.png')
        filter_img.add_pattern('*.eps')
        dialog.add_filter(filter_img)

    # callback function for save
    def save_callback(self, action, parameter):
        print("You clicked \"Save\"")

    # callback function for copy_action
    def login_callback(self, action, parameter):
        print("\"Login\" activated")
        if not ia.is_logged():
            dialog = TwitterDialog(self)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                pin = dialog.entry.get_text()
                ia.get_logged(dialog.auth, pin)
            elif response == Gtk.ResponseType.CANCEL:
                pass
            dialog.destroy()
        else:
            print("You are already logged")

    # callback function for paste_action
    def logout_callback(self, action, parameter):
        print("\"Logout\" activated")
        ia.logout()

    # callback function for shape_action
    def shape_callback(self, action, parameter):
        print("Shape is set to", parameter.get_string())
        # Note that we set the state of the action!
        action.set_state(parameter)

    def source_callback(self, action, parameter):
        ia.webbrowser.open_new("https://github.com/AmadoCab/Proyecto3-progra")

    # callback function for about (see the AboutDialog example)
    def about_callback(self, action, parameter):
        # Instance of Gtk.AboutDialog
        aboutdialog = Gtk.AboutDialog()

        # Varibles of the aboutdialog
        image = GdkPixbuf.Pixbuf.new_from_file_at_scale('icono.png',4*12,5*12,True)
        authors = ["Amado Alberto Cabrera Estrada"]
        comments = "Implementación de un conversor de imágenes a Ascii-Art que permite compartir imágenes hechas de caracteres a través de Twitter."
        version = "1.0"

        # Fill the aboutdialog
        aboutdialog.set_logo(image)
        aboutdialog.set_program_name("Pic to Ascii-Art")
        aboutdialog.set_copyright("Copyright \xc2\xa9 2020 Amado C.")
        aboutdialog.set_authors(authors)
        aboutdialog.set_comments(comments)
        aboutdialog.set_website("https://github.com/AmadoCab/Proyecto3-progra")
        aboutdialog.set_website_label("Github Source Code")
        aboutdialog.set_version(version)

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        aboutdialog.show()

    # a callback function to destroy the aboutdialog
    def on_close(self, action, parameter):
        action.destroy()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        # FIRST THING TO DO: do_startup()
        Gtk.Application.do_startup(self)

        # action without a state created
        quit_action = Gio.SimpleAction.new("quit", None)
        # action connected to the callback function
        quit_action.connect("activate", self.quit_callback)
        # action added to the application
        self.add_action(quit_action)

        # action with a state created
        state_action = Gio.SimpleAction.new_stateful(
            "state",  GLib.VariantType.new('s'), GLib.Variant.new_string('off'))
        # action connected to the callback function
        state_action.connect("activate", self.state_callback)
        # action added to the application
        self.add_action(state_action)

        # action with a state created
        awesome_action = Gio.SimpleAction.new_stateful(
            "awesome", None, GLib.Variant.new_boolean(False))
        # action connected to the callback function
        awesome_action.connect("activate", self.awesome_callback)
        # action added to the application
        self.add_action(awesome_action)

        # a builder to add the UI designed with Glade to the grid:
        builder = Gtk.Builder()
        # get the file (if it is there)
        try:
            builder.add_from_file("menubar.xml")
        except:
            print("file not found")
            sys.exit()

        # we use the method Gtk.Application.set_menubar(menubar) to add the menubar
        # and the menu to the application (Note: NOT the window!)
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("appmenu"))

    # callback function for quit
    def quit_callback(self, action, parameter):
        print("You clicked \"Quit\"")
        sys.exit()

    # callback function for state
    def state_callback(self, action, parameter):
        print("State is set to", parameter.get_string())
        action.set_state(parameter)

    # callback function for awesome
    def awesome_callback(self, action, parameter):
        action.set_state(GLib.Variant.new_boolean(not action.get_state()))
        if action.get_state().get_boolean() is True:
            print("You checked \"Awesome\"")
        else:
            print("You unchecked \"Awesome\"")

class TwitterDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Twitter Login", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        vbox = self.get_content_area()

        label = Gtk.Label(label="Insert your pin")
        self.en = Gtk.Entry()

        vbox.pack_start(label, True, True, 0)
        vbox.pack_end(self.entry, True, True, 0)
        self.show_all()

        consumer_key = ia.consumer_key
        consumer_secret = ia.consumer_secret
        self.auth = ia.tweepy.OAuthHandler(consumer_key, consumer_secret)
        ia.webbrowser.open(self.auth.get_authorization_url())

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
