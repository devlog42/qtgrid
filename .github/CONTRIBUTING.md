# How to contribute

[1]: https://github.com/devlog42/qtgrid                                      "Repository"
[2]: https://github.com/devlog42/qtgrid/blob/main/.github/CODE_OF_CONDUCT.md "Code of Conduct"
[3]: https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project         "Contributing Tutorial"
[4]: https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History              "Rewriting History"
[5]: https://pypi.org/project/pycodestyle/                                   "pycodestyle"
[6]: https://pypi.org/project/pipenv/                                        "pipenv"
[7]: https://pytest.org                                                      "pytest"
[8]: https://devlog42.github.io/qtgrid                                       "Documentation Homepage"
[9]: https://www.mkdocs.org/                                                 "mkdocs"

First off, thanks for taking the time to contribute!

Before we start, I would like to point out that we naturally treat each other in a friendly manner. And yes, that includes allowing us to have a bad day. I mean, sometimes a lot just comes together. The neighbour's dog doesn't rest, the weather is gray, you have run out of coffee and the internet trolls are now making it onto television. What can I say? Well, there is a separate page called the [Code of Conduct][2] that you should have a look at.

So that you can make the contribution you want, proceed in the usual way for GitHub. That means, you create a fork from the repository, tinker yourself with a nice branch and at the end send me a pull request.

If you don't know how to do this yet - or as a reminder - you'll find a nice tutorial [here][3].

## Styleguides

### Git Commit Messages

The usual rules apply to the commits

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    >
    > A paragraph describing what have changed and its impact."

### Python Styleguide

All python code is linted with [pycodestyle][5] (formerly called pep8). The following errors and warnings are disabled:

E121,E123,E126,E201,E202,E221,E226,E251,E272,E24,E704,W503

## Environment

For the virtual environment and installations I use [pipenv][6]. I would like to ask you to do the same.

You won't find the Pipfiles in the repository because I installed additional modules that are only there
for packaging. So after cloning, here's what you should do:

    $ git clone https://github.com/devlog42/qtgrid
    $ cd qtgrid
    $ pipenv shell
    $ pipenv install --dev pytest pydoctor PyQt5

In case you are also working on the [Documentation Homepage][8], ...

    $ pipenv install --dev mkdocs

## Writing tests

As far as testing is concerned, it becomes a little more complex. Since **qtgrid** should work equally for *PyQt6*,
*PyQt5* and *PySide6*, you currently have to install and uninstall each module one at a time. I haven't found a better way yet. If you can think of anything, I would be very grateful to hear about it.

The test scripts are as usual in the *tests/* folder. A certain order is guaranteed by numbers in the names. There you'll find examples of how to test for qt packages with importlib. But you'll see, just look around.

## Documentation

As for the documentation, there is the [Documentation Homepage][8] on GitHub and the API is a subset of that.

If it's only about the API, you don't have to worry about the homepage. You can regenerate the API if necessary
by executing the *mkapi.sh* script in the *docs-source/* folder. The output is written to *docs/api/*.

Within the docstrings, reStructuredText is used. Here is a general example:

    def foo(arg1="x", arg2=1) -> str :
        """
        Short summary line

        | Lorem ipsum dolor it samet Lorem ipsum
        | dolor it samet Lorem ipsum dolor et

        .. python::

            grid.foo( arg1="bar", arg2=1 )
            grid.foo("bar", 1)

        :param arg1: description
        :param arg2: description

        :return: some string
        """

When it comes to rebuilding the entire homepage, the [mkdocs][9] module comes into play.
The corresponding sites of the homepage can be found in *docs-source/docs/* folder as good old markdown files.

As long as you are working on it, you can start a small dev server :

    $ cd docs-pages
    $ mkdocs serve &

When the work is done, call the following script to regenerate the pages in *docs/*.

    $ cd docs-pages
    $ bash mkpages.sh


&nbsp;<br/>
&nbsp;<br/>

Thanx, and happy coding!

&nbsp;&nbsp;&nbsp;&nbsp;devlog42
