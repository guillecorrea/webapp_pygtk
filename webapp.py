#!/usr/bin/python
import sys
import gtk 
import webkit
import gobject
import pygtk


class BrowserTab(gtk.VBox):
    def __init__(self, *args, **kwargs):
        super(BrowserTab, self).__init__(*args, **kwargs)

        go_button = gtk.Button("go to...")
        go_button.connect("clicked", self._load_url)
        self.url_bar = gtk.Entry()
        self.url_bar.connect("activate", self._load_url)
        self.webview = webkit.WebView()
        
        settings = webkit.WebSettings()
        #settings.set_property('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) Applewebkit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
        self.webview.set_settings(settings)
        self.webview.props.settings.props.enable_default_context_menu = False
        self.show()

        self.go_back = gtk.Button("Back")
        self.go_back.connect("clicked", lambda x: self.webview.go_back())
        self.go_forward = gtk.Button("Forward")
        self.go_forward.connect("clicked", lambda x: self.webview.go_forward())

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add(self.webview)

        find_box = gtk.HBox()
        close_button = gtk.Button("X")
        close_button.connect("clicked", lambda x: find_box.hide())
        self.find_entry = gtk.Entry()
        self.find_entry.connect("activate",
                                lambda x: self.webview.search_text(self.find_entry.get_text(),
                                                                   False, True, True))
        prev_button = gtk.Button("<")
        next_button = gtk.Button(">")
        prev_button.connect("clicked",
                            lambda x: self.webview.search_text(self.find_entry.get_text(),
                                                               False, False, True))
        next_button.connect("clicked",
                            lambda x: self.webview.search_text(self.find_entry.get_text(),
                                                               False, True, True))
        
        find_box.pack_start(self.find_entry, False, False, 0)
        find_box.pack_start(prev_button, False, False, 0)
        find_box.pack_start(next_button, False, False, 0)
        find_box.pack_start(close_button, False, False, 0)
        self.find_box = find_box

        url_box = gtk.HBox()
        url_box.pack_start(self.go_back, False, False, 0)
        url_box.pack_start(self.go_forward, False, False, 0)
        url_box.pack_start(self.url_bar, True, True, 0)
        url_box.pack_start(go_button, False, False, 0)

        self.pack_start(url_box, False, False, 0)
        self.pack_start(scrolled_window, True, True, 0)
        self.pack_start(find_box, False, False, 0)

        #url_box.show_all()
        scrolled_window.show_all()

    def _load_url(self, widget):
        url = self.url_bar.get_text()
        if not "://" in url:
            url = "http://" + url
        self.webview.load_uri(url)

class Browser(gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        # create notebook and tabs
        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.tottabs =1
    
        # basic stuff
        self.tabs = []
        self.set_size_request(400,400)

        # create a first, empty browser tab
        self.tabs.append((self._create_tab(), gtk.Label("New Tab")))
        self.notebook.append_page(*self.tabs[0])
        self.add(self.notebook)

	# connect signals
        self.connect("destroy", gtk.main_quit)
        self.connect("key-press-event", self._key_pressed)
        self.notebook.connect("switch-page", self._tab_changed)
        
        self.notebook.set_show_tabs(False)
        self.notebook.show()
        
        self.show()
        
        self.tabs[self.notebook.get_current_page()][0].webview.load_uri("http://localhost:6566/app.html")

    
        
    def _tab_changed(self, notebook, current_page, index):
        if not index:
            return
        title = self.tabs[index][0].webview.get_title()
        if title:
            self.set_title(title)

    def _title_changed(self, webview, frame, title):
        current_page = self.notebook.get_current_page()

        counter = 0
        for tab, label in self.tabs:
            if tab.webview is webview:
                label.set_text(title)
                self.set_title(title)
                if counter == current_page:
                    self._tab_changed(None, None, counter)
                break
            counter += 1

    def _create_tab(self):
        tab = BrowserTab()
        tab.webview.connect("title-changed", self._title_changed)
        return tab

    def _reload_tab(self):
        self.tabs[self.notebook.get_current_page()][0].webview.reload()

    def _close_current_tab(self):
        if self.notebook.get_n_pages() == 1:
            return
        page = self.notebook.get_current_page()
        current_tab = self.tabs.pop(page)
        self.notebook.remove(current_tab[0])
        self.tottabs  =  self.tottabs  -1 
        if( self.tottabs  == 1 ):
            self.notebook.set_show_tabs(False)

    def _open_new_tab(self):
        current_page = self.notebook.get_current_page()
        page_tuple = (self._create_tab(), gtk.Label("New Tab"))
        self.tabs.insert(current_page+1, page_tuple)
        self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page+1)
        self.notebook.set_current_page(current_page+1)     
        self.notebook.set_show_tabs(False)  
        self.tottabs  =  self.tottabs  +1
        if( self.tottabs  > 1 ):
            self.notebook.set_show_tabs(True)
     
                

    def _focus_url_bar(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].url_bar.grab_focus()

    def _raise_find_dialog(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].find_box.show_all()
        self.tabs[current_page][0].find_entry.grab_focus()
    

    def _key_pressed(self, widget, event):
    
        print(str(event.keyval))
       
        modifiers = gtk.accelerator_get_default_mod_mask()
        # mapping = {114: self._reload_tab,
        #            119: self._close_current_tab,
        #            116: self._open_new_tab,
        #            108: self._focus_url_bar,
        #            102: self._raise_find_dialog,
        #            113: gtk.main_quit}
        mapping = {114: self._reload_tab,
                   102: self._raise_find_dialog,
                   119: self._close_current_tab,
                   113: gtk.main_quit}

        if event.state & modifiers == gtk.gdk.CONTROL_MASK   and event.keyval in mapping:
            mapping[event.keyval]()
        


   
   

if __name__ == "__main__":
   

    browser = Browser()
    
    gtk.main()
