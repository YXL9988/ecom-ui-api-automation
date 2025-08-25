# Ecommerce UI + API Tests

End-to-end demo combining **Playwright (UI)** and **pytest/requests (API)** for an ecommerce site.

## Tech Stack
- Python, pytest
- Playwright (UI automation)
- requests / Postman (API testing)
- GitHub Actions (CI)

## Project Structure
playwright_ecom-ui-api/
├─ test_ui/
│  ├─ test_UIValidations_1.py        # child-window demo
│  ├─ test_playwrightBasics_ui.py
│  ├─ test_filter_UI.py
│  ├─ test_Network1_ui.py
│  └─ test_Network2_ui.py
├─ test_api/
│  └─ test_framework_web_api.py
├─ utils/
│  └─ apiBaseFramework.py
├─ conftest.py                       
├─ pytest.ini
├─ requirements.txt
└─ (reports/)              


## Quick Start
```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python -m playwright install --with-deps
```

## Run Tests

```bash
# Run all (default)
pytest
```

```bash
# Only UI
pytest -m ui
```

```bash
# Only API
pytest -m api
```

```bash
# Single file / single test
pytest playwright_ecom-ui-api/test_framework_web_api.py
```
```bash
# Parallel (requires pytest-xdist)
pytest -n 3
```

```bash
#Windows PowerShell
Remove-Item -Recurse -Force reports -ErrorAction SilentlyContinue; mkdir reports\videos -Force > $null; pytest -n 3 -rA -vv --html=reports/index.html --self-contained-html 2>&1 | Tee-Object -FilePath reports\pytest.log

```

```bash
#macOS/Linux
rm -rf reports; mkdir -p reports/videos; set -o pipefail; pytest -n 3 -rA -vv --html=reports/index.html --self-contained-html 2>&1 | tee reports/pytest.log

```

## Pytest configuration
We keep a small `pytest.ini` at the repo root:

```ini
[pytest]
addopts = -q
testpaths = playwright_ecom-ui-api
pythonpath = .
python_files = test_*.py
python_functions = test_*

markers =
    ui: UI tests with Playwright
    api: API tests using requests/Postman
    e2e: End-to-end cross-layer flows
```
