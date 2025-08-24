# https://github.com/hssm/browser-sticky-search
# Version 1.1
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

        # Put ours on top and move existing one down a row
        browser.form.gridLayout.addWidget(stickyEdit, 1, 1, 1, 1)
        browser.form.gridLayout.addWidget(browser.form.searchEdit, 0, 1, 1, 1)

        self.browser = browser
        self.sticky = stickyEdit

    def browser_will_search(self, context):
        sticky_text = self.sticky.lineEdit().text()
        if sticky_text:
            context.search =  ' and '.join(['(' + sticky_text + ')', context.search])
            self.update_history(sticky_text)
        print(context.search)

    def update_history(self, text):
        sh = self.browser.mw.pm.profile.get("stickySearchHistory", [])
        if text and text in sh:
            sh.remove(text)
        sh.insert(0, text)
        sh = sh[:30]
        self.sticky.clear()
        self.sticky.addItems(sh)
        self.browser.mw.pm.profile["stickySearchHistory"] = sh

    def setup_search(self, *kwargs):
        line_edit = self.sticky.lineEdit()
        qconnect(line_edit.returnPressed, self.browser.onSearchActivated)
        self.sticky.setCompleter(None)
        line_edit.setPlaceholderText("Sticky search")
        line_edit.setMaxLength(2000000)
        self.sticky.addItems([""] + self.browser.mw.pm.profile.get("stickySearchHistory", []))


bss = BrowserStickySearch()

# Hooks
gui_hooks.browser_will_show.append(bss.browser_will_show)
gui_hooks.browser_will_search.append(bss.browser_will_search)
Browser.setupSearch = wrap(Browser.setupSearch, bss.setup_search, "after")
