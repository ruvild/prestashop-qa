import json


def test_product(default_product):
    response = default_product
    data = response.model_dump()
    print(json.dumps(data, indent=4))
