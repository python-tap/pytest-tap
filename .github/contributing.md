First,
come talk!
File an issue in GitHub
and we can discuss your bug/feature/idea.
If you are ready to start coding...

pytest-tap uses [uv](https://docs.astral.sh/uv/) for development.

```bash
$ git clone git@github.com:python-tap/pytest-tap.git
$ cd pytest-tap
$ # Edit some files and run the tests.
$ make test
```

Once your feature or bug fix is ready,
[submit a Pull Request](https://help.github.com/articles/creating-a-pull-request/>).

...profit! :moneybag:

# Release checklist

These are notes for my release process,
so I don't have to remember all the steps.
Other contributors are free to ignore this.

1. Update `docs/releases.rst`.
2. Update version in `pyproject.toml` and `src/pytest_tap/__init__.py`.
3. `rm -rf dist && uv build`
4. `uv publish`
5. `git tag -a vX.X -m "Version X.X"`
6. `git push --tags`
