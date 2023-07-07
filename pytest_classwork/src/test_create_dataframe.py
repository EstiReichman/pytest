from license_search import create_dataframe
import pytest
import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC



def test_create_df(monkeypatch):
    expected = 'my fake df'
  

    monkeypatch.setattr('license_search.pd.DataFrame', lambda columns: expected)
    actual =create_dataframe()
    assert actual == expected

