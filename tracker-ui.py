#!/usr/bin/python
import sys
import os
import gtk
import gobject

class TrackerApp:
  def __init__(self):
    self.icon = gtk.StatusIcon()    
    self.icon.set_from_file("data/time-100.png")
    self.icon.connect('activate', self.activate_win)
    self.icon.connect('popup-menu', self.popup_menu)
    self.win = gtk.Window()
    self.win.set_title("Time Left")
    self.win.set_border_width(5)
    self.win.set_resizable(False)
    self.win.set_deletable(False)    
    self.win.connect("destroy", gtk.main_quit)
    self.vbox = gtk.VBox()
    self.vbox.set_spacing(5)
    self.win.add(self.vbox)
    self.bar = gtk.ProgressBar()
    self.vbox.add(self.bar)
    self.label = gtk.Label()
    self.vbox.add(self.label)
    self.win_hide = True
    self.menu = gtk.Menu()
        
    menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
#    menuItem.connect('activate', self.activate_setupwin)
    self.menu.append(menuItem)

    menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
#    menuItem.connect('activate', self.activate_aboutbox)
    self.menu.append(menuItem)

    menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    menuItem.connect('activate', self.quit)
    self.menu.append(menuItem)
    
  def activate_win(self, widget):
    if self.win_hide == True:
      self.win.show_all()
      self.win_hide = False
    else:
      self.win.hide_all()
      self.win_hide = True

  def popup_menu(self, widget, button, time):
    if button == 3:
      self.menu.show_all()
      self.menu.popup(None, None, None, 3, time)
      
  def set_window(self, text = 'Unknown time left', fraction = 0.0):
    if self.win:
      self.label.set_text(text)
      self.bar.set_fraction(fraction)
      self.icon.set_tooltip(text)
      filename = self.get_icon_filename(fraction)
      self.icon.set_from_file(filename)
      
  def set_lbl_markup(self, text):
    if self.win:
      self.label.set_markup('<span color="#FF0000">%s</span>' % text)      
      
  def update(self):
    lines = open('/var/log/tracker/%s' % os.getenv('USER')).readlines()
    try:
      words = lines[0].split()
      maxtime = words[0]
      usedtime = words[1]
      prettytime = lines[2].strip()
    except IndexError:
      self.set_window()
      return

    frac = float(usedtime)/float(maxtime)

    if (frac < 0.1):
      self.set_lbl_markup(prettytime)
      self.icon.set_tooltip(prettytime)
    else:
      self.set_window(prettytime, frac)
      self.icon.set_tooltip(prettytime)
   

  def start(self):
    self.icon.set_visible(True)
    gobject.timeout_add(1000, self.update)
    self.update()
    gtk.main()

  def quit(self, widget):
    self.icon.set_visible(False)
    gtk.main_quit()

  def get_icon_filename(self, fraction):
    if fraction < 0.12:
      return "data/time-000.png"
    if fraction < 0.24:
      return "data/time-012.png"     
    if fraction < 0.36:
      return "data/time-024.png"     
    if fraction < 0.48:
      return "data/time-036.png"     
    if fraction < 0.60:
      return "data/time-048.png"     
    if fraction < 0.72:
      return "data/time-060.png"     
    if fraction < 0.84:
      return "data/time-072.png"     
    if fraction < 0.96:
      return "data/time-084.png"     
    if fraction < 1.0:
      return "data/time-096.png"     
    if fraction == 1.0:
      return "data/time-100.png"     
    
if __name__ == '__main__':
  app = TrackerApp()
  app.start()
