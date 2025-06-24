import pytest


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config

from utils import attach

def pytest_addoption(parser):
    parser.addoption(
        '--browser', help='Браузер в котором будут запущены тесты',
        choices= ['firefox', 'chrome'],
        default='chrome'
    )


@pytest.fixture(scope='function')
def setup_browser(request):
    browser_name = request.config.getoption('--browser')
    options = Options()
    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": "127.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser = Browser(Config(driver=lambda: driver))

    yield browser

    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_html(browser)
    attach.add_video(browser)
