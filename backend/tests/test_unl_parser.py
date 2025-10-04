from app.etl.unl_parser import parse_unl

def test_parse_unl_basic():
    text = "1|A||\\N\n2|B|C|"
    rows = list(parse_unl(text))
    assert rows[0] == ["1","A",None,None]
    assert rows[1] == ["2","B","C",None]
