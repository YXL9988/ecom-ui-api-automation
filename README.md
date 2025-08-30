[![Tests](https://github.com/YXL9988/ecom-ui-api-automation/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YXL9988/ecom-ui-api-automation/actions/workflows/tests.yml)


# Ecommerce UI + API Tests

End-to-end demo combining **Playwright (UI)** and **pytest/requests (API)** for an ecommerce site.
It runs locally and on GitHub Actions, publishes an HTML report to GitHub Pages, and attaches UI test videos as workflow artifacts.

---
## Tech Stack
- Python, pytest
- Playwright (UI automation)
- requests (API)
- GitHub Actions + GitHub Pages

---

## What’s Covered

**UI (Playwright)**

- Basic navigation & core locators
- Add all items to cart / delete from cart
- Network stubbing: “no orders” and “unauthorized” flows (simulate edge cases)
- Session storage / token reuse to bypass login
- Filters & search
- Video recording of browser sessions

**API (requests + pytest)**

- Login (positive & negative)
- Create/Get orders(positive)
- Create order (negative - invalid token, missing data)
- Get products (positive & negative-  invalid token)
- Delete order history (positive & negative-  invalid token)

**API + UI (hybrid strategy)**
- Create order via API, then verify the `orderId` is displayed in **UI Orders History page**
> combining API setup with UI validation, ensuring frontend-backend consistency
---


## Project Structure
<pre>
ecom-ui-api-automation/
├─ .github/
│  └─ workflows/
│     └─ tests.yml                # CI pipeline (run tests + deploy Pages)
├─ playwright_ecom-ui-api/
│  ├─ assets/
│  ├─ data/
│  │  ├─ credentials.json         # created on CI from repo secrets
│  │  └─ credentials_negative.json
│  ├─ pageObject/
│  ├─ test_api/
│  │  └─ test_framework_web_api.py
│  ├─ test_ui/
│  │  ├─ test_playwrightBasics_ui.py
│  │  ├─ test_UIValidations_1.py
│  │  ├─ test_filter_UI.py       # has a CI-only skip to avoid flaky external data
│  │  ├─ test_Network1_ui.py     # marked as network_edge (no orders)
│  │  ├─ test_Network2_ui.py     # marked as network_edge (unauthorized,bypass login)
│  │  └─ test_network_e2e.py     # Marked as network (cross-layer E2E)
│  ├─ utils/
│  │  └─ apiBaseFramework.py
│  ├─ conftest.py                  # fixtures, video recording, browser options
│  └─ pytest.ini                   # pytest settings (plugins, metadata, etc.)
├─ requirements.txt
└─ README.md
</pre>

---

## Quick Start

```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python -m playwright install --with-deps
```
---
## Provide test credentials

**Option A — Local file**
Create `playwright_ecom-ui-api/data/credentials.json` with:

```json
{
  "user_credentials": [
    {
      "case": "valid-1",
      "userEmail": "test915@gmail.com",
      "userPassword": "Test12345",
      "expected": 200
    },
    {
      "case": "valid-2",
      "userEmail": "test9152@gmail.com",
      "userPassword": "Test12345",
      "expected": 200
    }
  ]
}
```
(Negative cases are in credentials_negative.json and are already in the repo.)

- Option B — CI secrets (see CI section below): the workflow will generate credentials.json from secrets.

---

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
# Only network
pytest -m network
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
Remove-Item -Recurse -Force reports -ErrorAction SilentlyContinue; mkdir reports\videos -Force > $null; pytest -rA -vv --html=reports/index.html --self-contained-html 2>&1 | Tee-Object -FilePath reports\pytest.log

```

```bash
#macOS/Linux
rm -rf reports; mkdir -p reports/videos; set -o pipefail; pytest -rA -vv --html=reports/index.html --self-contained-html 2>&1 | tee reports/pytest.log

```
---

## HTML Report & Videos
- After a local run, open reports/index.html in your browser.
- Playwright recordings are stored in reports/videos/ (one video per test that opened a browser).

---
## Public report
- After a successful run, the latest HTML report is published via GitHub Pages.
- You can find the link in the Actions → tests → deploy job output.

---
## Pytest configuration
We keep a small `pytest.ini` at the repo root:

```ini
[pytest]
addopts = -q --tracing=retain-on-failure
testpaths = playwright_ecom-ui-api
pythonpath = .
python_files = test_*.py
python_functions = test_*

markers =
    ui: UI tests with Playwright
    api: API tests using requests/Postman
    e2e: End-to-end cross-layer flows
```

---
> Disclaimer
>
> The target application is a public demo site provided by RahulShettyAcademy for training and practice purposes.
> 
> This repository is for educational purposes only and has no affiliation with the site owners.
> 
> Test scenarios and cases have been customized and extended beyond the original examples.
> 
> Please use only test data. Do not submit any real personal or payment information.

---

## About the Author

**Lynn Lin**  
SQA Engineer | SDET in Progress | Ex-S&P Fixed Income Analyst  

- Passionate about quality, detail, and automation.
- Skilled in manual testing, API testing (Postman), SQL, and backend test design.
- Python automation scripts and build maintainable pytest + Playwright frameworks 
  (fixtures, parametrization, POM,network intercepts, data-driven tests).
- CI/CD with GitHub Actions
- Open to global opportunities (remote / hybrid).

Reach me on [LinkedIn] https://www.linkedin.com/in/yan-xi-lynn-l-19b27084
Email: linyanxi915@gmail.com


>  This project is part of my QA/SDET portfolio. Feedback and collaboration are welcome!
