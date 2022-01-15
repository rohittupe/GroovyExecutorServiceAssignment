import base64
import logging
import random, string
import pytest
from pytest_config import user_details as ud
from pytest_config import environment_details as env
from py.xml import html


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--environment", action="store", default="local", help="Default environment")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test to run only smoke tests",
    )
    config.addinivalue_line(
        "markers", "regression: mark test to run only regression tests"
    )
    config._metadata["Environment"] = config.getoption('--environment')


@pytest.fixture()
def environment_details(request):
    environment = request.config.getoption("--environment")
    details = env.env_details[environment]
    return details


@pytest.fixture()
def user_details(request):
    config = ud.user_details
    users = {}
    for user, details in config.items():
        username = details.get("username")
        password = ud.decode_string(details.get("password"))
        encoded = base64.b64encode(str(username + ':' + password).encode()).decode()
        details.update({"auth": encoded})
        users[user] = details
    return users


def generate_random_string(length=1):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def pytest_html_report_title(report):
    report.title = "Groovy Code Executor Report"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("The report contains tests for Groovy Code Executor service.")])


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Test Description"))


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)