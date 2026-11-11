"""Core data quality analysis and cleaning utilities for CleanSheet."""

from __future__ import annotations

from typing import Any
import pandas as pd


def analyze_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """Return dataset-level and per-column quality metrics."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    total_cells = int(df.shape[0] * df.shape[1])
    missing_by_column = df.isna().sum().astype(int)
    missing_cells = int(missing_by_column.sum())
    duplicate_rows = int(df.duplicated().sum())

    missing_pct = (missing_cells / total_cells * 100) if total_cells else 0.0
    duplicate_pct = (duplicate_rows / len(df) * 100) if len(df) else 0.0

    # Transparent heuristic: missing cells contribute 70%, duplicate rows 30%.
    score = round(max(0.0, 100.0 - (missing_pct * 0.7) - (duplicate_pct * 0.3)))
    score = min(100, max(0, score))

    rows = []
    for column in df.columns:
        series = df[column]
        rows.append({
            "Column": str(column),
            "Data type": str(series.dtype),
            "Missing": int(series.isna().sum()),
            "Missing %": round(float(series.isna().mean() * 100), 2),
            "Unique values": int(series.nunique(dropna=True)),
        })

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": missing_cells,
        "missing_pct": round(missing_pct, 2),
        "duplicate_rows": duplicate_rows,
        "duplicate_pct": round(duplicate_pct, 2),
        "quality_score": score,
        "missing_by_column": missing_by_column,
        "column_report": pd.DataFrame(rows),
    }


def clean_dataframe(
    df: pd.DataFrame,
    numeric_strategy: str = "Median",
    text_strategy: str = "Most frequent value",
    trim_text: bool = True,
    remove_duplicates: bool = True,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Clean a copy of a DataFrame using explicit, user-selected strategies.

    All-null columns are handled deterministically: numeric columns use zero
    for numeric strategies, while non-numeric columns use ``Unknown``.
    The input frame is never mutated.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    allowed_numeric = {"Median", "Mean", "Zero", "Drop rows"}
    allowed_text = {"Most frequent value", "Fill with 'Unknown'", "Drop rows"}
    if numeric_strategy not in allowed_numeric:
        raise ValueError(f"numeric_strategy must be one of {sorted(allowed_numeric)}")
    if text_strategy not in allowed_text:
        raise ValueError(f"text_strategy must be one of {sorted(allowed_text)}")

    cleaned = df.copy(deep=True)
    original_rows = len(cleaned)
    original_missing = int(cleaned.isna().sum().sum())

    if trim_text:
        text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
        for column in text_columns:
            # Preserve nulls and avoid applying string methods to non-strings.
            cleaned[column] = cleaned[column].map(
                lambda value: value.strip() if isinstance(value, str) else value
            )

    numeric_columns = cleaned.select_dtypes(include="number").columns.tolist()
    non_numeric_columns = [c for c in cleaned.columns if c not in numeric_columns]

    if numeric_strategy == "Drop rows":
        if numeric_columns:
            cleaned = cleaned.dropna(subset=numeric_columns)
    else:
        for column in numeric_columns:
            if cleaned[column].isna().any():
                if not cleaned[column].notna().any():
                    fill_value = 0
                elif numeric_strategy == "Median":
                    fill_value = cleaned[column].median()
                elif numeric_strategy == "Mean":
                    fill_value = cleaned[column].mean()
                else:
                    fill_value = 0
                # An all-null numeric column has no mean/median. Use 0 so
                # the selected fill strategy still produces a complete column.
                if pd.isna(fill_value):
                    fill_value = 0
                cleaned[column] = cleaned[column].fillna(fill_value)

    if text_strategy == "Drop rows":
        if non_numeric_columns:
            cleaned = cleaned.dropna(subset=non_numeric_columns)
    else:
        for column in non_numeric_columns:
            if cleaned[column].isna().any():
                if text_strategy == "Fill with 'Unknown'":
                    fill_value = "Unknown"
                else:
                    modes = cleaned[column].mode(dropna=True)
                    fill_value = modes.iloc[0] if not modes.empty else "Unknown"
                cleaned[column] = cleaned[column].fillna(fill_value)

    before_dedup = len(cleaned)
    if remove_duplicates:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    else:
        cleaned = cleaned.reset_index(drop=True)

    missing_after = int(cleaned.isna().sum().sum())
    rows_removed = original_rows - len(cleaned)
    duplicates_removed = before_dedup - len(cleaned)

    return cleaned, {
        "rows_removed": int(rows_removed),
        "duplicates_removed": int(duplicates_removed),
        "missing_filled": int(max(0, original_missing - missing_after)),
    }


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Encode a DataFrame as UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode("utf-8-sig")


def format_bytes(size: int) -> str:
    """Format a byte count for display."""
    if size < 1024:
        return f"{size} B"
    if size < 1024**2:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024**2):.1f} MB"
