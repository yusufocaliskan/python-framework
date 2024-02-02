
from src.utils.helpers import generate_client_id, generate_secret_key


def generateAClient(dbInstance):
    client_id = generate_client_id()
    secret_key = generate_secret_key()

    result = dbInstance.client.update_one(
        {'clientId': client_id},
        {'$setOnInsert': {'clientId': client_id, 'secretKey': secret_key}},  # Update
        upsert=True
    )
    if (result.upserted_id is None):
        return False
    return True
