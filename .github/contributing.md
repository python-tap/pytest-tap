First,
come talk!
File an issue in GitHub
and we can discuss your bug/feature/idea.
If you are ready to start coding...

pytest-tap uses the `venv` module
and a requirements file
to manage development.

```bash
$ git clone git@github.com:python-tap/pytest-tap.git
$ cd pytest-tap
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements-dev.txt
$ # Edit some files and run the tests.
$ pytest
```

Once your feature or bug fix is ready,
[submit a Pull Request](https://help.github.com/articles/creating-a-pull-request/>).

...profit! :moneybag:

# Making Releases

pytest-tap uses `bump2version`
to set the proper version
for releases.

The steps to release are roughly:

```bash
# Set docs/releases.rst with an appropriate changelog.
$ bump2version minor
$ python setup.py release
$ twine upload dist/*
```
