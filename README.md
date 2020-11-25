## Project summary
---
My notes, implementations, and experiments related to principles presented in *Powerful Python* by Aaron Maxwell.

## Project set up
---
I'm using Poetry for package and venv management and pyenv for python version management.  
* `$ poetry init`
* `$ poetry install --no-root` installed Python 3.7.8 into `.venv`.
   * I have Python 3.7.8 set as my global Python version (`$ pyenv global 3.7.8`).
   * If I wanted a different version, I think I could do something like `pyenv local 3.8.1` assuming that is installed.
* `$ source .venv/bin/activate` (so I don't need to use `poetry run` before each python command)

## Documentation
----
The documentation can be viewed and navigated via web browser using MkDocs.  To start the server on MacOS:
* navigate to the directory that hosts `mkdocs.yml`
* activate a virtual environment (mine is called "docs")
* install mkdocs (like `$ poetry add mkdocs mkdocs-material mkdocs-material-extensions`)
* start the server:
```bash
$ mkdocs serve --dev-addr 127.0.0.1:8001
```
where `--dev-addr` is used to override the default IP address, I think.  The server polls the docs for changes so that 
one can see real-time updates to pages as they are written.

Helpful MkDocs-related references:

* [MkDocs](https://www.mkdocs.org/)
    * [Writing your docs](https://www.mkdocs.org/user-guide/writing-your-docs/)
* [Material (theme) for MkDocs](https://squidfunk.github.io/mkdocs-material/getting-started/)
    * [Admonition](https://squidfunk.github.io/mkdocs-material/extensions/admonition/) - helpful
   reference for admonition terms and icons
* [markdown-include](https://pypi.org/project/markdown-include/) - Python library that allows 
Python code to be 'included' in the docs via reference to Python files (so the code can be 
runnable and also not have to be copied and pasted wherever it appears in the docs)
* FastAPI has detailed, thorough documentation, so I like to use it as an example for how to 
accomplish certain things via Markdown.
    * [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) - example UI page 
    implementing MkDocs, Material, and markdown-include
    * [Query Parameters](https://raw.githubusercontent.com/tiangolo/fastapi/22982287ff5e8434fdaffcf118d56eb084f2490c/docs/tutorial/query-params.md) - example raw markup
    * [fastapi/mkdocs.yml](https://github.com/tiangolo/fastapi/blob/master/mkdocs.yml) - example YML
