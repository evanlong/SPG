### Welcome

The purpose of Simple Page Gen (SPG) is to make it easy to build a simple
multipage website with a few markdown files.

### Install

`pip intall spg`

SPG depends on the following Python packages all of which can be installed with
pip:

    Jinja2
    Markdown
    Pygments


### Getting started

Once SPG is installed create a site, build it and view it. This can be done
with the following commands:

    spg create site_name
    spg make site_name
    open site_name_out/index.html

The template site is the documentation for SPG. The next steps are writing
markdown files and updating the `manifest.json` in order to render those files.

### Details after getting started

The template site and all SPG sites have the following structure:

    site_name/
        static/ - folder containing the static resources for the site
        manifest.json - metadata describing the site and and pages (this is a
        required file)
        base.html - a jinja2 template (this is a required file)
        index.markdown - this file
        docs.markdown - documentation of commands spg accepts

The `manifest.json` and the markdown files are the only files that require
editing. The manifest contains a JSON dictionary with two keys: `header` and
`links`. The `header` represents the text that will be passed to the templates
`header` variable.

The `links` key provides an array of key/value pairs. The order of the array
specifies the order in which the links should be rendered on the page. The
key/value pairs in the array specify the title and a URL or a markdown file
that they link to.

The manifest for the SPG documentation site has the following structure:

    "links": [
        {"title":"Home", "md":"index.markdown"},
        {"title":"Docs", "md":"docs.markdown"},
        {"title":"Github", "url":"https://github.com/evanlong/SPG"}
    ]

The first two links will be to pages rendered by the `index.markdown` and
`docs.markdown` files. The last link will be a link to an external site.

In order to add a another page create a markdown file. Create some content and
add it to the links list. Running `spg make site_name` again will regenerate
the site.

### License

SPG is licensed under the terms of the MIT License which can be found here:
<https://github.com/evanlong/SPG/blob/master/LICENSE.txt>.

