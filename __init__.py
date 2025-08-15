# https://github.com/hssm/browser-sticky-search
# Version 0.1
from PyQt6 import QtWidgets
from aqt import *
from anki.hooks import wrap
from aqt.browser import Browser


class BrowserStickySearch:

    def browser_will_show(self, browser):

        stickyEdit = QtWidgets.QComboBox(parent=browser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(stickyEdit.hasHeightForWidth())
        stickyEdit.setSizePolicy(sizePolicy)
        stickyEdit.setEditable(True)
        stickyEdit.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        stickyEdit.setObjectName("stickyEdit")
        stickyEdit.lineEdit().setPlaceholderText("Sticky search (type text, then press Enter")
        qconnect(stickyEdit.lineEdit().returnPressed, browser.onSearchActivated)


        # Put ours on top and move existing one down a row
        browser.form.gridLayout.addWidget(stickyEdit, 0, 1, 1, 1)
        browser.form.gridLayout.addWidget(browser.form.searchEdit, 0, 2, 2, 2)

        self.sticky = stickyEdit

    def browser_will_search(self, context):
        context.search = ' '.join([context.search, self.sticky.lineEdit().text()])
        return None

    def setup_search(self, *kwargs):
        self.sticky.setFocus()

bss = BrowserStickySearch()

# Hooks
gui_hooks.browser_will_show.append(bss.browser_will_show)
gui_hooks.browser_will_search.append(bss.browser_will_search)
Browser.setupSearch = wrap(Browser.setupSearch, bss.setup_search, "after")