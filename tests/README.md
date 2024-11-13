# Tests

Unit & application tests are written using the [pytest](https://docs.pytest.org/en/latest/) framework.


## Dependencies

Before running the tests, install the required dependencies:

```bash
pip install -r test-requirements.txt
# or
make test-init
```

## Running Tests

To run the tests, execute the following command:

```bash
pytest
```

To run a specific test file or function, execute the following commands:

```bash
pytest tests/test_main.py

pytest tests/test_main.py::test_get_root
```

Some usefull flags are:
- `-v` verbose mode, more information about the tests
- `--lf` run only the tests that failed last time
- `--disable-warnings` disable warnings for cleaner output
- `-rA` show all the results, including the skipped tests

```bash
pytest -v --lf --disable-warnings -rA
```
