import json


class ClientException(Exception):
    pass


def lambda_handler(event, context):
    metadata = event['body-json']

    if not metadata:
        raise ClientException(
            "{\"failure\":true, \"errorMessage\": \"POST data empty or not JSON\"")

    # NaN, Infinity, and -Infinity cause issues in Search, and have no use in MDF
    try:
        json.dumps(metadata, allow_nan=False)
    except Exception as e:
        raise ClientException(
            "{\"failure\":true, \"errorMessage\": \"Submission must be valid JSON\"")

    # If this is an incremental update, fetch the original submission
    if metadata.get("incremental_update"):
        # source_name and title cannot be updated
        metadata.get("mdf", {}).pop("source_name", None)
        metadata.get("dc", {}).pop("titles", None)

        # update must be True
        if not metadata.get("update"):
            raise ClientException(
                "{\"failure\":true, \"errorMessage\": \"You must be updating a submission (set update=True) when incrementally updating\"")
        # @TODO
        # Lookup previous submission in Dynamo

    # Validate input JSON
    # resourceType is always going to be Dataset, don't require from user
    if not metadata.get("dc") or not isinstance(metadata["dc"], dict):
        metadata["dc"] = {}
    if not metadata["dc"].get("resourceType"):
        try:
            metadata["dc"]["resourceType"] = {
                "resourceTypeGeneral": "Dataset",
                "resourceType": "Dataset"
            }
        except Exception:
            pass

    # Move tags to dc.subjects
    if metadata.get("tags"):
        tags = metadata.pop("tags", [])
        if not isinstance(tags, list):
            tags = [tags]
        if not metadata["dc"].get("subjects"):
            metadata["dc"]["subjects"] = []
        for tag in tags:
            metadata["dc"]["subjects"].append({
                "subject": tag
            })

    return {
        'source_id': '123-44-55-66'
    }
