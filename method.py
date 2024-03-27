import json


def verify(path: str) -> bool:
    """
    Returns false if an input JSON Resource field 
    contains a single asterisk and true in any other case
    """
    try:       
        with open(path) as content:
            input = json.load(content)
            resource = input.get('PolicyDocument').get('Statement')[0].get('Resource')
            return resource != '*'
    except Exception:
        return False


if __name__ == '__main__':
    print(verify('example.json'))
