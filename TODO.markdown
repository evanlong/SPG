* need template_base.html
* css styling
* mobile?
* Allow for sub-sites
* spg updgrade - update the static assets and base.html files
* no .sidebar in the single page case
* sidebar in compact case
    - Ideas
        + Expansion MENU on click (how to handle the noscript case for this)
        + overflow-y scrolling
* reevaluate noscript usage on the site. Possible to make the whole thing without JS?
    * or simply improve ability to emit fragments of the body so JS can load that content separately
* manifest is json
    {
        "pages":[
            {"title":"Page title", "url":"http://www.google.com" },
            {"title":"Index Page", "md":"index.markdown" },
            {"title":"Other Page", "md":"other.markdown" }
        ]
    }




Putting it on the model is easy now... To get rendered links and what not Going forward might want to pull it out so model is a raw look at the user defined state and rules around interpreting that state so figuring out defaults are what and how tree is searched when a default isn't specified

- Does model directly generate the data used for the template? Or a renderer?
- Does activate state even belong on the model? Or does it belong on a renderer?
- model can define the rules around default values, it's not specified where does it find that state in the tee
- how much does the template know about model object directly? Or is this where we provide a superset facade?
