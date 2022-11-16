import gi
import os

gi.require_version("Gtk", "3.0")
# gi.require_version('Notify', '0.7')

from gi.repository import Gtk
# from gi.repository import Notify

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Logitech G513 Keyboard Helper for Linux")
        Gtk.Window.set_default_size(self, 640, 480)
        Gtk.Window.set_icon_from_file(self, "keys.ico")

        # Notify.init("Simple GTK3 Application")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        # Change all button 
        self.button = Gtk.Button(label="Change all keys")
        self.button.set_margin_top(50)
        self.button.set_margin_bottom(10)
        self.button.connect("clicked", self.on_button_clicked)

        # Remove colors button
        self.button2 = Gtk.Button(label="Turn off lights")
        self.button2.connect("clicked", self.on_clear_button)
        self.button2.set_margin_bottom(10)

        # GROUPS    
        groups_list = Gtk.ListStore(str)  
        groups = [
            "List",
            "indicators",
            "fkeys",
            "modifiers",
            "arrows",
            "numeric",
            "functions",
            "keys",
        ]
        for group in groups:
            groups_list.append([group])

        groups_combo = Gtk.ComboBox.new_with_model(groups_list)
        groups_combo.connect("changed", self.on_groups_combo_changed)
        renderer_text = Gtk.CellRendererText()

        groups_combo.pack_start(renderer_text, False)
        groups_combo.add_attribute(renderer_text, "text", 0)
        groups_combo.set_margin_bottom(10)
        groups_combo.set_halign(Gtk.Align.CENTER)
        groups_label = Gtk.Label(label="Change group:", angle=0)

        self.user_entry = Gtk.Entry()
        self.user_entry.connect("changed", self.on_user_input)
        self.user_entry.set_halign(Gtk.Align.CENTER)

        self.button3 = Gtk.Button(label="Change single key")
        self.button3.connect("clicked", self.change_single_key)
        self.button3.set_margin_bottom(10)
        self.user_entry.set_halign(Gtk.Align.CENTER)

        version = Gtk.Label(label="v1.0.0")
        version.set_margin_bottom(10)
        version.set_margin_top(10)

        image = Gtk.Image()
        image.set_from_file("keys.png")

        # GRID
        grid = Gtk.Grid()
        grid.attach(version, 0,9,2,1)
        grid.attach(image, 0,8,2,1)
        grid.attach(self.button, 0,2,2,1)
        grid.attach(groups_label, 0,3,2,1)
        grid.attach(groups_combo, 0,4,2,1)    
        grid.attach(self.user_entry, 0,5,2,1)
        grid.attach(self.button3, 0,6,2,1)
        grid.attach(self.button2, 0,7,2,1)        
        grid.set_margin_top(0)
        grid.set_margin_start(50)
        self.box.add(grid)

        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        self.colorchooser.set_margin_top(50)
        self.box.pack_start(self.colorchooser, True, True, 50)

    def change_single_key(self, widget):
        if hasattr(self, 'text'):
            print(self.text, "yep")
            hex = self.get_selected_hex()
            command = f"g513-led -k {self.text} {hex} -c"
            os.system(command)
        else:
            print("Type in the single key")

    def on_user_input(self, widget):
        self.text = self.user_entry.get_text()
        print(self.text, "self.text")

        
    def get_selected_hex(self):
        color_rgba = self.colorchooser.get_rgba()
        self.color = color_rgba
        red = int(color_rgba.red*255)
        green = int(color_rgba.green*255)
        blue = int(color_rgba.blue*255)
        hex = '%02x%02x%02x' % (red, green, blue) 
        return hex


    def on_groups_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            group = model[tree_iter][0]
            hex = self.get_selected_hex()
            command = f"g513-led -g {group} {hex} -c"
            os.system(command)


    def on_clear_button(self, widget):
        command = f"g513-led -a 000000 -c"
        os.system(command)


    def on_button_clicked(self, widget):        
        hex = self.get_selected_hex()
        command = f"g513-led -a {hex} -c"
        os.system(command)
        # notification = Notify.Notification.new("My first GTK3 Application",  self.color.to_string())
        # notification.show()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
