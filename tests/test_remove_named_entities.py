from src.remove_named_entities import remove_named_entities

def test_basic_removal_named_entities():
    text = "Neither the name of Alok Kumar nor the names of its contributors"
    result = remove_named_entities(text)
    assert "Alice" not in result
    assert "Bob" not in result

def test_ignore_named_entities_which_is_in_legalese():
    text = "DATA POSSIBILITY LIABILITY"
    result = remove_named_entities(text)
    assert text == result




