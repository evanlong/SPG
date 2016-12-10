#!/usr/bin/env python

import sys
import os
import datetime
import shutil
import codecs
from jinja2 import Environment, FileSystemLoader, Template
import markdown
import json

import model

"""
Note:

Think about how the render of the model should work with respect to:
    - Who generates the file path? Should the renderer do this?
    - Who generates the file names of output for a link? Renderer? Helper method on the objects themselves?
    - The advantage of breaking that out is a renderer could generate it's own filename to model object mapping
        - instead of creating a folder structure, the renderer could generate uuid file name for each link output?

    - model -> renderer -> template are we passing raw model objects to the template or some agreed upon format?
        - Doesn't seem like a great idea passing models directly because input to template should be indepedent of the model itself I think

    - Could have wrapper/mapper objects that wrap our models and provide things like: header, link, file etc...
"""

def renderSection(section):
    for l in section.links:
        renderLink(l)

    for s in section.sections:
        renderSection(s)

def renderLink(link):
    if link.type == LinkType.MARKDOWN:
        renderMarkdownLink(link)
    elif link.type == LinkType.URL:
        renderUrlLink(link)
    elif link.type == LinkType.SECTION:
        renderSectionLink(link)

def renderMarkdownLink(link):
    with link as l:
        templateData = {}
        templateData["header"] = link.parentSection.header
        templateData["links"] = link.parentSection.links
        templateData["content"] = "Hello World!"

def renderUrlLink(link):
    pass

def renderSectionLink(link):
    pass

def _setExtension(path, newExt):
    return os.path.splitext(path)[0] + newExt

def buildSite(path, manifestPath, templatePath):
    # setup the output directory
    outPath = os.path.abspath(path) + "_out"
    if os.path.isdir(outPath):
        shutil.rmtree(outPath, ignore_errors=True)
    elif os.path.isfile(outPath):
        os.remove(outPath)

    shutil.copytree(path, outPath)

    os.remove(os.path.join(outPath, os.path.basename(manifestPath)))
    os.remove(os.path.join(outPath, os.path.basename(templatePath)))

    with codecs.open(manifestPath, "r", encoding="utf-8") as f:
        manifestData = json.load(f)

    if type(manifestData) != type({}):
        showError("%s must specify an object of parameters" % (manifestPath))
        return

    header = manifestData.get("header", "Specify \"header\" in manifest.json")

    links = manifestData.get(u"links", [])
    if type(links) != type([]):
        showError("%s must specify an array with key `links`" % (manifestPath))
        return

    forTemplate = {
        "header": header,
        }
    transformedLinks = []
    markdownFiles = []
    for l in links:
        title = l.get("title", "unknown title")
        o = {"title": title}
        if l.has_key("url"):
            o["link"] = l["url"]
        elif l.has_key("md"):
            inputMd = os.path.exists(os.path.join(path, l["md"]))
            if not os.path.exists(os.path.join(path, l["md"])):
                showError("The manifest.json specified the file %s but it could not be found" % l["md"])
                return
            o["link"] = _setExtension(l["md"], ".html")
            markdownFiles.append((title, os.path.join(outPath, l["md"])))
        else:
            showError("links require a url or a markdown file")
            return
        transformedLinks.append(o)
    forTemplate["links"] = transformedLinks

    env = Environment(loader=FileSystemLoader(path), autoescape=False)
    template = env.get_template("base.html")
    for mdPair in markdownFiles:
        forTemplate["title"] = mdPair[0]
        mdFile = mdPair[1]
        with codecs.open(mdFile, "r", encoding="utf-8") as f:
            forTemplate["content"] = markdown.markdown(f.read(), ["codehilite"])
        result = template.render(forTemplate)
        with codecs.open(_setExtension(mdFile, ".html"), "w", encoding="utf-8") as f:
            f.write(result)
        os.remove(mdFile)

def main():
    if len(sys.argv) > 2:
        command = sys.argv[1]
        param = sys.argv[2]
        if command == "make":
            if not os.path.isdir(param):
                showError("The directory %s does not exist" % (param))
            else:
                manifestPath = os.path.join(param, "manifest.json")
                templatePath = os.path.join(param, "base.html")
                if not os.path.isfile(manifestPath):
                    showError("Could not find the manifest at: %s" % manifestPath)
                    return
                if not os.path.isfile(templatePath):
                    showError("Could not find the template at: %s" % templatePath)
                    return
                buildSite(param, manifestPath, templatePath)
        elif command == "create":
            if os.path.exists(param):
                showError("The directory %s already exists." % (param))
            else:
                samplesitePath = os.path.join(os.path.dirname(__file__), "samplesite")
                shutil.copytree(samplesitePath, param)
    else:
        showHelp()

_usage="""Usage: %s command params

Commands:
  make dir_name - takes the specified directory and generates the website. The
    output is placed in a directory with `dir_name` suffixed with "_out"

  create dir_name - creates a new site in `dir_name` using the spg template

  help - displays this message
""" % (sys.argv[0])
def showHelp():
    print _usage

def showError(msg):
    sys.stderr.write("Error: %s\n" % msg)

if __name__ == "__main__":
    main()
