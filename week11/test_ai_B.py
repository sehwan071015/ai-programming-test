import pytest

from load_scores import load_scores


def test_load_scores_returns_names_and_scores_including_boundary_values(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(
        "name,score\nAlice,0\nBob,100\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Alice", 0), ("Bob", 100)]
    assert skipped == []


def test_load_scores_skips_out_of_range_scores_without_changing_source(tmp_path):
    csv_path = tmp_path / "scores.csv"
    original = "name,score\nBelow,-1\nAbove,101\nValid,75\n"
    csv_path.write_text(original, encoding="utf-8", newline="")

    kept, skipped = load_scores(csv_path)

    assert kept == [("Valid", 75)]
    assert skipped == [
        (2, "Below,-1", "점수가 0~100 밖"),
        (3, "Above,101", "점수가 0~100 밖"),
    ]
    assert csv_path.read_text(encoding="utf-8", newline="") == original


def test_load_scores_preserves_csv_quoted_special_characters_in_name(tmp_path):
    csv_path = tmp_path / "special_name.csv"
    csv_path.write_text(
        'name,score\n"Kim, Hana!",90\n',
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Kim, Hana!", 90)]
    assert skipped == []


def test_load_scores_keeps_duplicate_names(tmp_path):
    csv_path = tmp_path / "duplicates.csv"
    csv_path.write_text(
        "name,score\nSame Name,80\nSame Name,95\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Same Name", 80), ("Same Name", 95)]
    assert skipped == []


def test_load_scores_skips_missing_or_non_integer_scores(tmp_path):
    csv_path = tmp_path / "invalid_scores.csv"
    csv_path.write_text(
        "name,score\nMissing,\nNotInteger,absent\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == []
    assert skipped == [
        (2, "Missing,", "점수가 비어 있음"),
        (3, "NotInteger,absent", "점수가 정수가 아님"),
    ]


def test_load_scores_raises_file_not_found_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")