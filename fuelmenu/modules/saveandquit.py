#!/usr/bin/env python
# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import urwid
import urwid.raw_display
import urwid.web_display
from fuelmenu.common.urwidwrapper import *
from fuelmenu.common import dialog
import subprocess
import time
blank = urwid.Divider()


class saveandquit():
    def __init__(self, parent):
        self.name = "Save & Quit"
        self.priority = 99
        self.visible = True
        self.parent = parent
        self.screen = None


    def save_and_continue(self, args):
        self.save()

    def save_and_exit(self, args):
        if self.save():
            self.parent.refreshScreen()
            time.sleep(1.5)
            self.parent.exit_program(None)

    def save(self):
        results, modulename = self.parent.global_save()
        if results:
           self.parent.footer.set_text("All changes saved successfully!")
           return True
        else:
           #show pop up with more details
           msg = "ERROR: Module %s failed to save. Go back" % (modulename)\
                 + " and fix any mistakes or choose Exit without Saving."
           diag = dialog.display_dialog(self, TextLabel(msg),
                                        "Error saving changes!")
           return False

    def exit_without_saving(self, args):
        self.parent.exit_program(None)

    def refresh(self):
        pass

    def screenUI(self):
        #Define your text labels, text fields, and buttons first
        text1 = urwid.Text("Save configuration before you exit?")
        saveandcontinue_button = Button("Save and Continue",
                                        self.save_and_continue)
        saveandexit_button = Button("Save and Exit", self.save_and_exit)
        exitwithoutsaving_button = Button("Exit without saving",
                                          self.exit_without_saving)
        #Build all of these into a list
        listbox_content = [text1, blank, saveandcontinue_button,
                           saveandexit_button, exitwithoutsaving_button]

        #Add everything into a ListBox and return it
        screen = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        return screen