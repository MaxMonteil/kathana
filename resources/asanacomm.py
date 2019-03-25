import asana


class Asanacomm:
    '''
    A class to handle communications with Asana.

    Parameters:
        token <str> Personal Access Token (PAT) of user
    '''

    def __init__(self, token, workspace_name):
        self.client = asana.Client.access_token(token)
        self.client.options['client_name'] = 'kathana'
        self.workspace = self.fetch_workspace(workspace_name)

        if not self.workspace:
            raise ValueError(f'There is no "{workspace_name}" workspace.')

        self.projects = self.fetch_project_ids(self.workspace['gid'])

    def fetch_workspace(self, workspace_name):
        '''
        Fetches the full workspace information, especially the workspace ID,
        from Asana based on the workspace name since the asana api requires it.

        Parameters:
            workspace_name <str> String name of the workspace
        '''

        all_workspaces = self.client.workspaces.find_all()

        for workspace in all_workspaces:
            if workspace['name'] == workspace_name:
                return workspace

        return None

    def fetch_project_ids(self, workspace_id):
        '''
        Fetches the id and gid of all projects in the supplied workspace.

        Parameters:
            workspace_id <str> The unique id of the workspace
        '''

        return self.client.projects.find_all(
                params={
                    'workspace': workspace_id,
                    'archived': False
                    })
