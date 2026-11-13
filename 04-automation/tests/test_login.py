"""登录模块 UI 自动化用例。

对应手工用例：01-test-cases/form-authentication*.md
对应缺陷单：02-bug-reports/BUG-001-登录失败无限流.md

标记说明：
  @pytest.mark.xfail —— 已知缺陷，用例按“正确行为”写断言，当前实现做不到，
  因此标记为预期失败。缺陷修复后该用例会变成 XPASS，届时移除标记即可。
"""
import pytest
from conftest import (
    LOGIN_URL,
    BASE_URL,
    VALID_USER,
    VALID_PASSWORD,
    login,
)

USERNAME_HINT = "Your username is invalid!"
PASSWORD_HINT = "Your password is invalid!"
SUCCESS_HINT = "You logged into a secure area!"


def test_TC_LOGIN_001_正确账号登录成功(page):
    """正确账号密码应跳转 /secure 并显示成功提示。"""
    flash = login(page, VALID_USER, VALID_PASSWORD)
    assert "/secure" in page.url, f"登录成功后应跳转 /secure，实际 URL={page.url}"
    assert SUCCESS_HINT in flash, f"应提示 {SUCCESS_HINT}，实际={flash!r}"
    assert "Logged in as tomsmith" in page.inner_text("body")


def test_TC_LOGIN_002_密码错误提示正确且不跳转(page):
    """密码错误应停留 /login，并提示密码无效。"""
    flash = login(page, VALID_USER, "wrong-password")
    assert page.url.rstrip("/").endswith("/login"), f"应停留 /login，实际 URL={page.url}"
    assert PASSWORD_HINT in flash, f"应提示 {PASSWORD_HINT}，实际={flash!r}"


def test_TC_LOGIN_003_失败后输入框被清空(page):
    """登录失败后表单应重置，避免把上一次的错误值留在框里。"""
    flash = login(page, VALID_USER, "wrong-password")
    assert PASSWORD_HINT in flash
    assert page.input_value("#username") == "", "失败后用户名输入框应被清空"
    assert page.input_value("#password") == "", "失败后密码输入框应被清空"
    assert page.locator("#flash").count() > 0, "页面上应存在提示条元素"


@pytest.mark.xfail(
    strict=True,
    reason="已知缺陷：用户名未做 trim，前导空格导致登录失败（应视为同一账号）",
)
def test_TC_LOGIN_004_用户名前导空格应被忽略(page):
    """` tomsmith`（前导一个空格）应与 `tomsmith` 等价，应能登录成功。

    当前实现返回 'Your username is invalid!' —— 说明未做 trim。
    """
    flash = login(page, f" {VALID_USER}", VALID_PASSWORD)
    assert "/secure" in page.url, f"前导空格不应影响登录，实际 URL={page.url}，提示={flash!r}"


@pytest.mark.xfail(
    strict=True,
    reason="已知缺陷 BUG-001：连续失败无任何限流/锁定，可被暴力破解",
)
def test_TC_LOGIN_005_连续失败五次后应触发限制(page):
    """连续 5 次密码错误后，第 6 次即使密码正确也不应直接放行。

    当前实现：5 次失败后第 6 次正确密码直接登录成功，全程无限流、无验证码、无锁定。
    """
    for _ in range(5):
        login(page, VALID_USER, "wrong-password")
    flash = login(page, VALID_USER, VALID_PASSWORD)
    assert "/secure" not in page.url, (
        f"连续失败 5 次后不应直接放行，实际 URL={page.url}，提示={flash!r}。"
        "若仍直接登录成功，说明无限流，对应 BUG-001。"
    )


def test_TC_LOGIN_006_退出登录后会话失效(page):
    """Logout 应回到 /login，且直接访问 /secure 会被拦截。"""
    login(page, VALID_USER, VALID_PASSWORD)
    assert "/secure" in page.url

    page.goto(f"{BASE_URL}/logout")
    page.wait_for_load_state("domcontentloaded")
    assert page.url.rstrip("/").endswith("/login"), f"退出后应回到 /login，实际={page.url}"
    assert "You logged out of the secure area!" in page.inner_text("#flash")

    page.goto(f"{BASE_URL}/secure")
    page.wait_for_load_state("domcontentloaded")
    assert page.url.rstrip("/").endswith("/login"), f"未登录访问 /secure 应被重定向，实际={page.url}"
    assert "You must login to view the secure area!" in page.inner_text("#flash")
