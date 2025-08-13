# https://github.com/hssm/browser-sticky-search
# Version 0.1

from aqt import *
from anki.hooks import wrap
from aqt.browser import Browser


class BrowserStickySearch:

    def browser_will_show(self, browser):
        sticky = QLineEdit(browser)
        sticky.setPlaceholderText("Sticky search (type text, then press Enter)")
        qconnect(sticky.returnPressed, browser.onSearchActivated)

        # Put ours on top and move existing one down a row
        browser.form.gridLayout.addWidget(sticky, 0, 1, 1, 1)
        browser.form.gridLayout.addWidget(browser.form.searchEdit, 1, 1, 1, 1)

        self.sticky = sticky

    def browser_will_search(self, context):
        context.search = ' '.join([context.search, self.sticky.text()])
        return None

    def setup_search(self, *kwargs):
        self.sticky.setFocus()

bss = BrowserStickySearch()

# Hooks
gui_hooks.browser_will_show.append(bss.browser_will_show)
gui_hooks.browser_will_search.append(bss.browser_will_search)
Browser.setupSearch = wrap(Browser.setupSearch, bss.setup_search, "after")