# What I Learned Today (Testing + Python Imports)

## Quick Rules

- If a method only mutates instance state (no external call), I do not need to mock dependencies.
- If a method calls external systems (SDKs, sockets, network clients), patch at the import path used by the module under test.
- `pytest.raises(SomeError)` passes if any matching error is raised inside the block, even if I do not raise it manually.
- A fixture factory does not auto-mock the class instance; it returns a real instance unless I explicitly mock it.
- Empty `__init__.py` files are normal and valid.

## Mocking Patterns That Worked

- Patch constructors like `yf.Ticker` and `yf.WebSocket` where they are used:
  - `btc_streaming_etl.pubsub.yfinance_manager.yf.Ticker`
  - `btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket`
- Use one shared mock fixture when I want to compare the same object identity.
- For error tests, set `side_effect` to the actual exception type/object I expect.
- Keep one behavior per test (setter behavior, socket creation, error path, etc.).

## Import and Environment Lessons

- If tests do not reflect code changes, I may be importing stale code from `site-packages` instead of local `src`.
- Editable install (`pip install -e .` or `uv pip install -e .`) keeps imports mapped to live source files.
- Running pytest from the correct project root matters for `pyproject.toml` path settings.
- Wrong `pythonpath` configuration can point pytest to the wrong module location.

## Common Failure Causes I Hit

- Wrong patch target string (including tiny typos like trailing dots).
- Fixture names used in function signatures but not defined.
- Broad error assertions (`TypeError`) passing for unintended reasons.
- Import-time execution in module files causing collection/import failures.

## Personal Debug Checklist (Reuse)

1. Confirm interpreter/venv: `which python` and `which pytest`.
2. Confirm imported module path:
   - `python -c "import module as m; print(m.__file__)"`
3. Validate patch target matches the exact call site in code under test.
4. Make error assertions specific when possible (type + message).
5. Keep tests deterministic: patch external calls, avoid accidental live dependency behavior.

## Next Quality Step

- For every public method, keep at least:
  - one success test,
  - one controlled failure test,
  - one invalid-input/guard test (if applicable).
