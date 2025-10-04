from app.etl.name_normalizer import normalize_name

def test_normalize_name():
    assert normalize_name("  Jiří   Novák ") == "jiri novak"
