import os
import asana

# Construct asana client
client = asana.Client.access_token(os.environ['ASANA_TOKEN'])
client.options['client_name'] = 'kathana'

# Get user info
me = client.users.me()

# Print out information
print(f'My name is {me["name"]}.')
print(me['workspaces'])
