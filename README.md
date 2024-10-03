# Logitech G513 keyboard helper for Linux

GUI interface to modify led lights and create custom led setup for Logitech G513 mechanical keyboard. Program is written in Python.
Minimum required Python version is 3.10.0

### changelog

- 1.0.0 initial release

### prerequisites

```
sudo apt install python3 python3-gi g810-led
```

### how to run

```
python3 gui.py
```

### important notes

Gui.py does not work with python 3.11 because python3-gi module was compiled for python 3.10.
It works and was tested with python version 3.10.12

Have fun!
