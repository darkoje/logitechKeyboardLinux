#!/bin/python3


import gi
import os

gi.require_version("Notify", "0.7")
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Notify

import subprocess
import sys


# {type: k/g/a, name: name, color: color}

single_keys = {}
key_groups = {}  # group: color
all_keys = ""  # "color"
fx_command = ""


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Logitech G513 Keyboard Helper for Linux")
        Gtk.Window.set_default_size(self, 640, 480)
        Gtk.Window.set_icon_from_file(self, "keys.ico")

        Notify.init("Simple GTK3 Application")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        # Change all
        self.all_button = Gtk.Button(label="Change all keys")
        self.all_button.set_margin_top(50)
        self.all_button.set_margin_bottom(10)
        self.all_button.connect("clicked", self.on_button_clicked)

        # Turn off
        self.off_button = Gtk.Button(label="Turn off lights")
        self.off_button.connect("clicked", self.on_clear_button)
        self.off_button.set_margin_bottom(10)

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

        # EFFECTS
        effects_list = Gtk.ListStore(str)
        effects = ["breathing", "cycle", "hwave", "vwave", "cwave", "color", "warning"]
        for effect in effects:
            effects_list.append([effect])
        effects_combo = Gtk.ComboBox.new_with_model(effects_list)
        effects_combo.connect("changed", self.on_effects_combo_changed)
        effects_text = Gtk.CellRendererText()
        effects_combo.pack_start(effects_text, False)
        effects_combo.add_attribute(effects_text, "text", 0)
        effects_combo.set_margin_bottom(10)
        effects_combo.set_halign(Gtk.Align.CENTER)
        effects_label = Gtk.Label(label="Use FX:", angle=0)

        # autocomplete
        liststore = Gtk.ListStore(str)
        for item in [
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f8",
            "f9",
            "f10",
            "f11",
            "f12",
            "num_indicator",
            "caps_indicator",
            "scroll_indicator",
            "game_mode",
            "light",
            "shift_left",
            "ctrl_left",
            "win_left",
            "alt_left",
            "alt_right",
            "win_right",
            "menu",
            "ctrl_right",
            "shift_right",
            "arrow_top",
            "top",
            "arrow_left",
            "left",
            "arrow_bottom",
            "bottom",
            "arrow_right",
            "right",
            "num_lock",
            "num_slash",
            "num_asterisk",
            "num_minus",
            "num_plus",
            "numenter",
            "num0",
            "num1",
            "num2",
            "num3",
            "num4",
            "num5",
            "num6",
            "num7",
            "num8",
            "num9",
            "num_dot",
            "escape",
            "print_screen",
            "scroll_lock",
            "pause_break",
            "insert",
            "home",
            "page_up",
            "page_down",
            "delete",
            "end",
            "tab",
            "caps_lock",
            "space",
            "enter",
            "tilde",
            "minus",
            "equal",
            "open_bracket",
            "close_bracket",
            "backslash",
            "semicolon",
            "dollar",
            "quote",
            "intl_backslash",
            "comma",
            "period",
            "slash",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]:
            liststore.append([item])

        self.entrycompletion = Gtk.EntryCompletion()
        self.entrycompletion.set_model(liststore)
        self.entrycompletion.set_text_column(0)

        self.user_entry = Gtk.Entry()
        self.user_entry.set_completion(self.entrycompletion)
        self.user_entry.connect("changed", self.on_user_input)
        self.user_entry.set_halign(Gtk.Align.CENTER)

        self.single_button = Gtk.Button(label="Change single key")
        self.single_button.connect("clicked", self.change_single_key)
        self.single_button.set_margin_bottom(10)
        self.single_button.set_halign(Gtk.Align.CENTER)

        self.save_button = Gtk.Button(label="Save changes permanently")
        self.save_button.connect("clicked", self.save_changes_permanently)
        self.save_button.set_margin_bottom(10)
        self.save_button.set_halign(Gtk.Align.CENTER)

        # version = Gtk.Label(label="v1.0.0")
        # version.set_margin_bottom(10)
        # version.set_margin_top(10)

        image = Gtk.Image()
        image.set_from_file("keys.png")

        # GRID
        grid = Gtk.Grid()
        # grid.attach(version, 0, 9, 2, 1)
        # grid.attach(image, 0, 9, 2, 1)
        grid.attach(self.all_button, 0, 2, 2, 1)
        grid.attach(groups_label, 0, 3, 2, 1)
        grid.attach(groups_combo, 0, 4, 2, 1)
        grid.attach(self.user_entry, 0, 5, 2, 1)
        grid.attach(self.single_button, 0, 6, 2, 1)
        grid.attach(effects_label, 0, 7, 2, 1)
        grid.attach(effects_combo, 0, 8, 2, 1)
        grid.attach(self.off_button, 0, 10, 2, 1)
        grid.attach(self.save_button, 0, 11, 1, 1)
        grid.set_margin_top(0)
        grid.set_margin_start(50)
        self.box.add(grid)

        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        self.colorchooser.set_margin_top(50)
        self.box.pack_start(self.colorchooser, True, True, 50)

    def fx(self, widget):
        hex = self.get_selected_hex()
        command = f"g513-led -fx breathing all {hex} 20"
        os.system(command)

    def save_changes_permanently(self, widget):
        global all_keys
        text_lines = []
        if fx_command:
            text_lines.append(fx_command)
        elif all_keys:
            text_lines.append(f"a {all_keys}")
        else:
            for key, value in key_groups.items():
                text_lines.append(f"g {key} {value}")
            for key, value in single_keys.items():
                text_lines.append(f"k {key} {value}")
        text_lines.append("c")
        text_for_file = "\n".join(text_lines)
        command = f'echo "{text_for_file}" | /usr/bin/pkexec --disable-internal-agent tee /etc/g810-led/profile'
        os.system(command)
        notification = Notify.Notification.new("Successfully saved profile", "success")
        notification.show()

    def change_single_key(self, widget):
        if hasattr(self, "text"):
            hex = self.get_selected_hex()

            match self.text:
                case "-":
                    self.text = "minus"
                case "+":
                    self.text = "plus"
                case " ":
                    self.text = "space"
                case "/":
                    self.text = "slash"
                case "\\":
                    self.text = "backslash"
                case ".":
                    self.text = "period"
                case ",":
                    self.text = "comma"
                case "'":
                    self.text = "quote"
                case "$":
                    self.text = "dollar"
                case ";":
                    self.text = "semicolon"
                case "(":
                    self.text = "open_bracket"
                case ")":
                    self.text = "close_bracket"
                case "=":
                    self.text = "equal"
                case "`":
                    self.text = "tilde"

            command = f"g513-led -k {self.text} {hex} -c"
            os.system(command)
            single_keys[self.text] = hex

        else:
            print("Type in the single key")

    def on_user_input(self, widget):
        self.text = self.user_entry.get_text()

    def get_selected_hex(self):
        color_rgba = self.colorchooser.get_rgba()
        self.color = color_rgba
        red = int(color_rgba.red * 255)
        green = int(color_rgba.green * 255)
        blue = int(color_rgba.blue * 255)
        hex = "%02x%02x%02x" % (red, green, blue)
        return hex

    def on_groups_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            group = model[tree_iter][0]
            hex = self.get_selected_hex()
            command = f"g513-led -g {group} {hex} -c"
            os.system(command)
            # add group to dictionary
            key_groups[group] = hex

    def on_effects_combo_changed(self, combo):
        global all_keys
        global fx_command
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            group = model[tree_iter][0]
            hex = self.get_selected_hex()
            print("Combo changed, hex:", hex, "group:", group)
            if group == "breathing":
                command = f"g513-led -fx breathing all {hex} 20"
            elif group == "cycle":
                command = "g513-led -fx cycle all 30"
            elif group == "hwave":
                command = "g513-led -fx hwave keys 0a"
            elif group == "vwave":
                command = "g513-led -fx vwave all 20"
            elif group == "cwave":
                command = "g513-led -fx cwave keys 0a"
            elif group == "color":
                command = f"g513-led -fx color keys {hex}"
            elif group == "warning":
                command = f"g513-led -fx breathing keys {hex} 5"
            os.system(command)
            all_keys = ""
            single_keys.clear()
            key_groups.clear()
            fx_command = command.strip("g513-led -")

    def on_clear_button(self, widget):
        global all_keys
        global fx_command
        command = f"g513-led -a 000000 -c"
        os.system(command)
        key_groups.clear()
        single_keys.clear()
        all_keys = "000000"
        fx_command = ""

    def on_button_clicked(self, widget):
        global all_keys
        global fx_command
        hex = self.get_selected_hex()
        command = f"g513-led -a {hex} -c"
        os.system(command)
        all_keys = f"{hex}"
        single_keys.clear()
        key_groups.clear()
        fx_command = ""
        notification = Notify.Notification.new("Changed colors of all keys", self.color.to_string())
        notification.show()


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
