"""Playwright + pytest 公共夹具。

复用本机已安装的 Microsoft Edge（channel="msedge"），不额外下载浏览器；
若本机装了 Chrome，把 channel 改成 "chrome" 即可。
"""
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://the-internet.herokuapp.com"
LOGIN_URL = f"{BASE_URL}/login"

VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    pg.set_default_timeout(10000)
    yield pg
    ctx.close()


def login(page, username, password):
    """执行一次登录操作，返回 flash 提示文字（若有）。"""
    page.goto(LOGIN_URL)
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_load_state("domcontentloaded")
    flash = page.locator("#flash")
    if flash.count() > 0:
        return flash.inner_text().strip()
    return ""
