from pathlib import Path
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )
    parser.addoption(
        "--url_name", action="store", default="https://rahulshettyacademy.com/client", help="server selection"
    )

@pytest.fixture(scope="session")
def user_credentials(request):
    return request.param

@pytest.fixture(scope="session")
def user_credentials_negative(request):
    return request.param

@pytest.fixture
def browserInstance(playwright,request):
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

@pytest.fixture
def app_url(request):
    return request.config.getoption("--url_name")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    out = Path("reports/videos")
    out.mkdir(parents=True, exist_ok=True)
    return {
        **browser_context_args,
        "record_video_dir": str(out),
        "record_video_size": {"width": 1280, "height": 720},
    }