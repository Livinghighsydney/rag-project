from app.helpers.hashing import hash_file, detect_duplicates


def test_hash_file_returns_64_char_hex(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world")
    result = hash_file(str(f))
    assert isinstance(result, str) and len(result) == 64


def test_identical_content_produces_same_hash(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("same content")
    f2.write_text("same content")
    assert hash_file(str(f1)) == hash_file(str(f2))


def test_different_content_produces_different_hash(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("content one")
    f2.write_text("content two")
    assert hash_file(str(f1)) != hash_file(str(f2))


def test_detect_duplicates_finds_duplicate_pair(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("same content")
    f2.write_text("same content")
    result = detect_duplicates([str(f1), str(f2)])
    assert len(result) == 1


def test_detect_duplicates_returns_empty_when_no_duplicates(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("content one")
    f2.write_text("content two")
    assert detect_duplicates([str(f1), str(f2)]) == {}
