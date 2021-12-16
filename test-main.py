#!/usr/bin/env python

import gtk
from bluetooth import *
from time import sleep

socket = BluetoothSocket(RFCOMM)
Connected = None
context_id = 0


class Window:

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('console_new.ui')
        self.set_hlt = self.builder.get_object('set_hlt_temp')
        self.set_mash = self.builder.get_object('set_mash_temp')
        self.set_boil = self.builder.get_object('set_boil_temp')
        self.status = self.builder.get_object('status')
        self.status.push(context_id, 'Not Connected')
        adj_hlt = gtk.Adjustment(0, 0, 212, 0.5)
        adj_mash = gtk.Adjustment(0, 0, 212, 0.5)
        adj_boil = gtk.Adjustment(0, 0, 212, 0.5)
        self.set_hlt.configure(adj_hlt, 0.5, 2)
        self.set_mash.configure(adj_mash, 0.5, 2)
        self.set_boil.configure(adj_boil, 0.5, 2)
        self.window = self.builder.get_object('main_window')
        if self.window:
            self.window.connect('destroy', self.exit)
        handlers = {
                    'about'             :   self.about,
                    'gtk_main_quit'     :   self.exit,
                    'about_response'    :   self.about_response,
                    'bt_error_response' :   self.bt_error,
                    'connect_bt'        :   self.connect_bt,
                    'boil_setTemp'      :   self.boil_setTemp,
                    'mash_setTemp'      :   self.mash_setTemp,
                    'hlt_setTemp'       :   self.hlt_setTemp,
        }
        self.builder.connect_signals(handlers)

    def exit(self, widget):
        global Connected
        if Connected is True:
            socket.close()
            Connected = False
        gtk.main_quit()

    def hlt_setTemp(self, widget):
        if Connected is True:
            socket.send('S0')
            socket.send('T:' + str(widget.get_value()))
        else:
            pass

    def mash_setTemp(self, widget):
        if Connected is True:
            socket.send('S2')
            socket.send('T:' + str(widget.get_value()))
        else:
            pass

    def boil_setTemp(self, widget):
        if Connected is True:
            socket.send('S4')
            socket.send('T:' + str(widget.get_value()))
        else:
            pass

    def connect_bt(self, widget):
        global Connected
        global context_id
        port = 1
        address = None
        target = 'BrewConsole'
        try:
            devices = discover_devices()
            for device in devices:
                if target == lookup_name(device):
                    address = device
            if address:
                socket.connect((address, port))
                Connected = True
                context_id = 1
                self.status = self.builder.get_object('status')
                self.status.push(context_id, 'Connected')
                self.update()
        except BluetoothError:
            self.builder.get_object('bt_error').show()
            Connected = False

    def bt_error(self, widget, *args):
        self.builder.get_object('bt_error').hide()

    def about(self, widget):
        self.builder.get_object('aboutdialog1').show()

    def about_response(self, widget, *args):
        self.builder.get_object('aboutdialog1').hide()

    def update(self):
        hltTemp = None
        mashTemp = None
        boilTemp = None
        #hlt_element = None
        #boil_element = None
        self.hlt_temp = self.builder.get_object('hlt_probe')
        self.mash_temp = self.builder.get_object('mash_probe')
        self.boil_temp = self.builder.get_object('boil_probe')
        #self.hlt_element = self.builder.get_object('hlt_element')
        #self.boil_element = self.builder.get_object('boil_element')
        while Connected is True:
            data = socket.recv(2048)
            if data:
                try:
                    disp = data.split('::')
                    disp = disp[1].split(',')
                    temp = disp[0].strip(':')
                    temp1 = disp[1].strip(':')
                    temp2 = disp[2].strip(':')
                    #element1 = disp[3].strip(':')
                    #element2 = disp[4].strip(':')
                    #print disp
                    #print temp
                    if temp:
                        hltTemp = temp
                    else:
                        pass
                    if temp1:
                        mashTemp = temp1
                    else:
                        pass
                    if temp2:
                        boilTemp = temp2
                    else:
                        pass
                    #if element1:
                    #    hlt_element = element1
                    #else:
                    #    pass
                    #if element2:
                    #    boil_element = element2
                    #else:
                    #    pass
                except:
                    pass
            #print hltTemp
            #print mashTemp
            #print boilTemp
            #print hlt_element
            #print boil_element
            if hltTemp == '-196.60':
                self.hlt_temp.set_text('Error')
            else:
                self.hlt_temp.set_text(str(hltTemp))
            if mashTemp == '-196.60':
                self.mash_temp.set_text('Error')
            else:
                self.mash_temp.set_text(str(mashTemp))
            if boilTemp == '-196.60':
                self.boil_temp.set_text('Error')
            else:
                self.boil_temp.set_text(str(boilTemp))
            #if hlt_element == '1':
            #    self.hlt_element.set_text('On')
            #else:
            #    self.hlt_element.set_text('Off')
            #if boil_element == '1':
            #    self.boil_element.set_text('On')
            #else:
            #    self.boil_element.set_text('Off')
            while gtk.events_pending():
                gtk.main_iteration()
            sleep(1)


if __name__ == '__main__':
    gui = Window()
    gui.window.show()
    gtk.main()
