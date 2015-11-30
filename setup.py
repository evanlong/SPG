try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(name="spg",
      version="0.0.2",
      author="Evan Long",
      author_email="annglove@gmail.com",
      description="SPG is a simple page generator. Given a set of markdown "\
          "files a website will be generated.",
      license="MIT License",
      packages=["spg"],
      package_data={"spg":["samplesite/base.html",
                           "samplesite/manifest.json",
                           "samplesite/*.markdown",
                           "samplesite/static/*"]},
      install_requires = ["Jinja2", "Markdown", "Pygments"],
      entry_points={
        "console_scripts": [
            "spg = spg.site:main"
            ]
        },
      )
