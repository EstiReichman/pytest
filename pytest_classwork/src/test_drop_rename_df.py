from license_search import drop_reanme_df
import pytest
import pandas as pd



def test_drop_rename_df(monkeypatch):
    expected = 'my fake dropped and renamed df'
    def mock_drop(columns):
        return expected
    
    def mock_rename(columns):
        return expected

  

    monkeypatch.setattr('license_search.lincenses_df.drop', mock_drop)
    monkeypatch.setattr('license_search.lincenses_df.rename', mock_rename)

    actual =drop_reanme_df()
    assert actual == expected


