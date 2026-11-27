import runpy
import sys

import pytest
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


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("점수, 유효한가", [
    (0, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(점수, 유효한가, tmp_path):
    파일 = tmp_path / "임시.csv"
    파일.write_text(f"이름,점수\n김하나,{점수}\n", encoding="utf-8")
    kept, skipped = load_scores(str(파일))
    assert (len(kept) == 1) == 유효한가


def test_이름이_비면_건너뛴다(tmp_path):
    파일 = tmp_path / "noname.csv"
    파일.write_text("이름,점수\n,88\n", encoding="utf-8")
    kept, skipped = load_scores(str(파일))
    assert kept == []
    assert len(skipped) == 1


def test_직접_실행하면_결과를_출력한다(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["load_scores.py", "scores.csv"])
    runpy.run_module("load_scores", run_name="__main__")
    출력 = capsys.readouterr().out
    assert "읽은 줄 : 5개" in 출력