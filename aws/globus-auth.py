import globus_sdk
import boto3

def get_secret():
    secret_name = "Globus"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    print("shhh, ", get_secret_value_response)
    return eval(get_secret_value_response['SecretString'])


def generate_policy(principalId, effect, resource, message=None):
    authResponse = {}
    authResponse['principalId'] = principalId
    if effect and resource:
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = [
            {'Action': 'execute-api:Invoke',
             'Effect': effect,
             'Resource': resource
             }
        ]
    authResponse['policyDocument'] = policyDocument
    authResponse['context'] = {
        'message': message
    }
    return authResponse


def lambda_handler(event, context):
    globus_secrets = get_secret()

    auth_client = globus_sdk.ConfidentialAppAuthClient(
        globus_secrets['API_CLIENT_ID'], globus_secrets['API_CLIENT_SECRET'])

    token = event['headers']['Authorization'].replace("Bearer ", "")

    auth_res = auth_client.oauth2_token_introspect(token, include="identities_set")

    if not auth_res:
        return generate_policy(None, 'Deny', event['methodArn'], message='User not found')

    if not auth_res['active']:
        return generate_policy(None, 'Deny', event['methodArn'],
                               message='User account not active')

    return generate_policy(auth_res['username'], 'Allow', event['methodArn'])


