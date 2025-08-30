from remove_named_entities import remove_named_entities

def test_basic_removal_person():
    text = "Neither the name of Alok Kumar nor the names of its contributors."
    result = remove_named_entities(text)
    assert "Alok Kumar" not in result
    assert "contributors" in result


def test_basic_removal_org():
    text = "This software is provided by OpenAI and contributors."
    result = remove_named_entities(text)
    assert "OpenAI" not in result
    assert "contributors" in result


def test_basic_removal_gpe():
    text = "This license applies in India and worldwide."
    result = remove_named_entities(text)
    assert "India" not in result
    assert "worldwide" in result


def test_ignore_legalese_words():
    text = "DATA POSSIBILITY LIABILITY"
    result = remove_named_entities(text)
    assert text == result


def test_entity_inside_required_phrase():
    text = "Neither the name of {{Alok Kumar}} may be used to endorse products."
    result = remove_named_entities(text)
    assert "Alok Kumar" in result 


def test_text_with_no_entities():
    text = "Redistribution and use in source and binary forms are permitted."
    result = remove_named_entities(text)
    assert text == result


