## Command Line Interface

SPG provides the following command line interface:

    make dir_name - takes the specified directory and generates the website. The
        output is placed in a directory with `dir_name` suffixed with "_out"
    create dir_name - creates a new site in `dir_name` using the spg template
    help - displays this message

## manifset.json

    {
        "header": "String for header variable in the template",
        "links": [
            {"title":"Title used for page and link", "md":"md file to render"},
            {"title":"External Page", "url":""},
            {"title":"Error no md or url key"}
        ]
    }

If a link entry has neither a `url` or a `md` key that is considered an
error. If it contains both a `url` and a `md` key then preference is given to
the `url` and the link will be external.

In order for a markdown file to be rendered it must appear in the `links` array.

## Creating a template

SPG uses [Jinja2](http://jinja.pocoo.org/docs/) for templating.

SPG has exactly one template: `base.html`. It exists in the site's root
directory and is used for each rendered page.

A custom template must account for the following variables: `title`, `header`,
`links`, and `content`. Each variable is described below:

    header - Text used on the top of each page.
    title - The title of the page when active. Derived from the link name.
    links - Array of key/value pairs with for each page. The keys are title and
    link.
    content - Result of rendering markdown to HTML.

That is it. Just four variables. Render them as desired.
