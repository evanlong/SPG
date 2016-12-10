#!/usr/bin/env python

import json
import codecs

class ModelError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)

class Section(object):
    def __init__(self, sectionDict, parentSection=None):
        super(Section, self).__init__()

        if type(sectionDict) != type({}):
            raise ModelError("Dictionary required to create Section")

        self._name = None
        if sectionDict.has_key("name"):
            self._name = sectionDict["name"]

        self._header = None
        if sectionDict.has_key("header"):
            self._header = sectionDict["header"]

        self._templateName = None
        if sectionDict.has_key("template"):
            self._templateName = sectionDict["template"]

        self._links = []
        if sectionDict.has_key("links"):
            links = sectionDict["links"]
            for link in links:
                self._links.append(Link(link, self))

        self._sections = []
        if sectionDict.has_key("sections"):
            sections = sectionDict["sections"]
            for section in sections:
                self._sections.append(Section(section, self))

        self._parentSection = parentSection
        self._active = False

    def __repr__(self):
        linksRepr = ""
        for l in self._links:
            linksRepr += "\t\t"
            linksRepr += repr(l)
            linksRepr += "\n"

        sectionRepr = ""
        for s in self._sections:
            sectionRepr += "\t"
            sectionRepr += repr(s)
            sectionRepr += "\n"

        return "Section(header = %s, templateName = %s, links = [\n%s],\nsections = [\n%s]" % (self.header,
            self.templateName,
            linksRepr,
            sectionRepr)

    @property
    def name(self):
        return self._name

    @property
    def header(self):
        return self._header

    @property
    def parentSection(self):
        return self._parentSection
    
    @property
    def templateName(self):
        if self._templateName:
            return self._templateName
        else:
            return self.parentSection.templateName

    @property
    def links(self):
        return self._links

    @property
    def sections(self):
        return self._sections

    def sectionByName(self, name):
        for section in self.sections:
            if section.name == name:
                return section
        raise KeyError(name)

    @property
    def active(self):
        for link in self.links:
            if link.active:
                return True

        for section in self.sections:
            if section.active:
                return True

        return False

class LinkType:
    UNKNOWN = 0
    MARKDOWN = 1
    URL = 2
    SECTION = 3

    @classmethod
    def string(self, t):
        if t == LinkType.MARKDOWN:
            return "MARKDOWN"
        elif t == LinkType.URL:
            return "URL"
        elif t == LinkType.SECTION:
            return "SECTION"
        else:
            return "UNKNOWN"

class Link(object):
    def __init__(self, linkDict, parentSection=None):
        super(Link, self).__init__()

        if type(linkDict) != type({}):
            raise ModelError("Dictionary required to create Link")

        self._title = linkDict.get("title", "unknown title")

        # LinkType md, url, section
        self._type = LinkType.UNKNOWN
        self._data = None
        if linkDict.has_key("md"):
            self._type = LinkType.MARKDOWN
            self._data = linkDict["md"]
        elif linkDict.has_key("url"):
            self._type = LinkType.URL
            self._data = linkDict["url"]
        elif linkDict.has_key("section"):
            self._type = LinkType.SECTION
            self._data = linkDict["section"]

        self._templateName = None
        if linkDict.has_key("template"):
            self._templateName = linkDict["template"]

        self._parentSection = parentSection
        self._active = False

    def __repr__(self):
        return "Link(title = %s, templateName = %s, type = %s, data = %s" % (self.title, self.templateName, LinkType.string(self.type), self.data)

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def templateName(self):
        if self._templateName:
            return self._templateName
        else:
            return self.parentSection.templateName

    @property
    def parentSection(self):
        return self._parentSection

    @property
    def active(self):
        if self._active:
            return True
        elif self.type == LinkType.SECTION:
            sectionName = self.data
            sectionRef = self.parentSection.sectionByName(sectionName)
            return sectionRef.active
        else:
            return False

    def __enter__(self):
        self._active = True
        return self

    def __exit__(self ,type, value, traceback):
        self._active = False
        return True

def loadSection(path):
    with codecs.open(path, "r", encoding="utf-8") as f:
        manifestData = json.load(f)
    return Section(manifestData)
