import pytest

from load_scores import load_scores


def test_load_scores_keeps_valid_scores_and_inclusive_boundaries(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(
        "\ufeffname,score\nAlice,0\n  Bob  , 100 \n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Alice", 0), ("Bob", 100)]
    assert skipped == []


def test_load_scores_records_invalid_rows_and_ignores_blank_lines(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(
        "name,score\n"
        "Alice,80\n"
        "\n"
        ",80\n"
        "Bob,\n"
        "Cara,abc\n"
        "Dan,-1\n"
        "Eve,101\n"
        "Finn,70,extra\n"
        "Grace\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Alice", 80)]
    assert skipped == [
        (4, ",80", "이름이 비어 있음"),
        (5, "Bob,", "점수가 비어 있음"),
        (6, "Cara,abc", "점수가 정수가 아님"),
        (7, "Dan,-1", "점수가 0~100 밖"),
        (8, "Eve,101", "점수가 0~100 밖"),
        (9, "Finn,70,extra", "열 개수가 2가 아님"),
        (10, "Grace", "열 개수가 2가 아님"),
    ]


@pytest.mark.parametrize("content", ["", "name,score\n", "name,score\n\n"])
def test_load_scores_handles_empty_data(tmp_path, content):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(content, encoding="utf-8", newline="")

    assert load_scores(csv_path) == ([], [])


def test_load_scores_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")