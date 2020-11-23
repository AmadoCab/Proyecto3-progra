import gi
from webbrowser import open_new
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
        self.set_default_size(500, 500)

        ### VARIABLES ###

        self.is_logged = ia.is_logged()

        ### CONTAINER ###
        
        grid = Gtk.Grid()
        self.add(grid)

        ### ELEMENTS ###

        # Buttons

        ### ACTIONS ###

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

    def startgame(self, widget):
        pass

    def set_play(self, widget):
        pass

    # callback function for copy_action
    def login_callback(self, action, parameter):
        print("\"Login\" activated")
        ia.get_logged()

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
        open_new("https://github.com/AmadoCab/Proyecto3-progra")

    # callback function for about (see the AboutDialog example)
    def about_callback(self, action, parameter):
        # Instance of Gtk.AboutDialog
        aboutdialog = Gtk.AboutDialog()

        # Varibles of the aboutdialog
        image = GdkPixbuf.Pixbuf.new_from_file_at_scale('icono.png',4*12,5*12,True)
        authors = ["Amado Alberto Cabrera Estrada"]
        comments = "Implementación de un conversor de imagenes a Ascii-Art que permite compartir imagenes hechas de caracteres a traves de twitter."
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

    # callback function for new
    def new_callback(self, action, parameter):
        print("You clicked \"New\"")
        self.imagen = ia.ImgToAscii('Images/Amadito.jpeg')

    # callback function for save
    def save_callback(self, action, parameter):
        print("You clicked \"Save\"")

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


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)