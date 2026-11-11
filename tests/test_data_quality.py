import pandas as pd
from src.data_quality import analyze_dataframe, clean_dataframe


def test_analyze_dataframe_counts_missing_and_duplicates():
    df = pd.DataFrame({"name": ["A", "A", "B"], "amount": [10, 10, None]})
    report = analyze_dataframe(df)
    assert report["missing_cells"] == 1
    assert report["duplicate_rows"] == 1
    assert 0 <= report["quality_score"] <= 100


def test_clean_dataframe_fills_missing_and_removes_duplicates():
    df = pd.DataFrame({
        "name": [" Alice ", "Alice", "Bob"],
        "amount": [10.0, 10.0, None],
    })
    cleaned, report = clean_dataframe(df)
    assert len(cleaned) == 2
    assert cleaned["name"].isna().sum() == 0
    assert cleaned["amount"].isna().sum() == 0
    assert report["duplicates_removed"] == 1


def test_original_dataframe_is_not_modified():
    df = pd.DataFrame({"name": [" A ", None], "value": [1.0, None]})
    original = df.copy(deep=True)
    clean_dataframe(df)
    pd.testing.assert_frame_equal(df, original)


def test_all_null_columns_are_filled_deterministically():
    df = pd.DataFrame({"amount": pd.Series([None, None], dtype="float64"), "category": [None, None]})
    cleaned, report = clean_dataframe(df, remove_duplicates=False)
    assert cleaned["amount"].tolist() == [0.0, 0.0]
    assert cleaned["category"].tolist() == ["Unknown", "Unknown"]
    assert cleaned.isna().sum().sum() == 0
    assert report["missing_filled"] == 4


def test_empty_dataframe_analysis_is_safe():
    report = analyze_dataframe(pd.DataFrame())
    assert report["rows"] == 0
    assert report["columns"] == 0
    assert report["quality_score"] == 100


def test_cleaning_does_not_remove_rows_when_deduplication_disabled():
    df = pd.DataFrame({"name": ["A", "A"], "value": [1, 1]})
    cleaned, report = clean_dataframe(df, remove_duplicates=False)
    assert len(cleaned) == 2
    assert report["duplicates_removed"] == 0
