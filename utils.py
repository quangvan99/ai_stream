from bson import ObjectId

def parse_json(data):
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in data.items()}
