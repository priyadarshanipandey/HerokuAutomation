import pytest
from selenium import webdriver

@pytest.fixture
def environment_details():
    url = "http://the-internet.herokuapp.com/"
    return url

