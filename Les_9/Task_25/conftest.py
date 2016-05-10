
import pytest
import json
import os.path
import ftputil
from fixture.application import Application


fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
       fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    web_config = load_config(request.config.getoption("--target"))['webadmin']
    fixture.session.ensure_login(username=web_config['user'], password=web_config['password'])
    return fixture

# @pytest.fixture(scope="session", autouse=True)
# def configure_server(request):
#     install_server_configuration(config['ftp'],['host'], config['ftp'],['username'], config['ftp'],['password'])
#     def fin():
#         restore_server_configuraton (config['ftp'],['host'], config['ftp'],['username'], config['ftp'],['password'])
#     request.addfinalizer(fin)
# def install_server_configuration(host):
#     pass

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

