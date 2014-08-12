#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime_plugin


class RanchorsCommand(sublime_plugin.TextCommand):
    """Tworzy odnośniki do poszczególnych ciał niebieskich w tabelce. Nie chce
    mi się tego opisywać.

    """

    def _transform(self, text):
        entries = []
        for entry in text.split(","):
            entries.append("[[#%s]]" % entry.strip())
        return ", ".join(entries)

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = self._transform(text)
                self.view.replace(edit, region, text)


class RtableCommand(sublime_plugin.TextCommand):
    """Przekształca tabele z narzędzia, którego używa Kamil do wygenerowania
    opisów systemów planetarnych na markup Mediawiki.

    """

    def _transform(self, text):
        lines = []
        for line in text.split("\n"):
            self_contained = False
            try:
                header, cell = line.split(":")
            except ValueError:
                self_contained = True
                header = line
                cell = ""

            header = header.strip()
            cell = cell.strip()

            if self_contained:
                lines.append("!colspan=\"2\"|%s" % header)
            else:
                lines.append("!%s\n|%s" % (header, cell))

        result = "{| class=\"wikitable\"\n%s\n|}\n" % "\n|-\n".join(lines)

        return result

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = self._transform(text)
                self.view.replace(edit, region, text)
