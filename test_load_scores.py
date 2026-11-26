from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    파일 = tmp_path / "blank.csv"
    파일.write_text("이름,점수\n김하나,88\n\n이둘,75\n", encoding="utf-8")
    kept, skipped = load_scores(str(파일))
    assert len(kept) == 2


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    파일 = tmp_path / "comma.csv"
    파일.write_text('이름,점수\n"김, 하나",90\n', encoding="utf-8")
    kept, skipped = load_scores(str(파일))
    assert len(kept) == 1