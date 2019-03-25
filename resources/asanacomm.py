import datetime
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
        self.workspace_id = self.fetch_workspace_id(workspace_name)

        if not self.workspace_id:
            raise ValueError(f'There is no "{workspace_name}" workspace.')

        self.projects = self.fetch_projects()

    def fetch_workspace_id(self, workspace_name):
        '''
        Fetches the workspace's id from Asana based on the workspace name since
        the asana api doesn't work off of the workspace name alone.

        Parameters:
            workspace_name <str> String name of the workspace
        '''
        print('Fetching workspace id')

        all_workspaces = self.client.workspaces.find_all()

        for workspace in all_workspaces:
            if workspace['name'] == workspace_name:
                return workspace['gid']

        return None

    def fetch_projects(self):
        '''
        Fetches the id and gid of all projects in the supplied workspace.
        '''
        print('Fetching projects')

        return self.client.projects.find_all(
                {
                    'workspace': self.workspace_id,
                    'archived': False
                })

    def fetch_workspace_tasks(self, since=None):
        '''
        Goes through each project in a workspace and fetches the tasks it
        contains going back to the date given by "since".

        Parameters:
            since <str> ISO 8601 format date, gets tasks completed since then
        '''
        print('Fetching workspace tasks')

        if not since:
            since = self.get_last_monday()

        for project in self.projects:
            print(f'Fetching tasks in {project["name"]}')
            yield self.fetch_project_tasks(project['gid'], since)

    def fetch_project_tasks(self, project_id, since=None):
        '''
        Fetches the data of all the tasks in a particular project that were
        completed since the given date.

        Parameters:
            project_id <str> The unique id of the project
            since <str> ISO 8601 format date, gets tasks completed since then
        '''

        if not since:
            since = self.get_last_monday()

        search_params = {
                'project': project_id,
                'completed_since': since}

        for compact_task in self.client.tasks.find_all(search_params):
            yield self.fetch_task(compact_task['gid'])

    def fetch_task(self, task_id, fields=[]):
        '''
        Fetches the complete information of a particular task.

        Parameters:
            task_id <str> The unique id of a task
            fields <list> String values of the data fields to return
        '''
        if not fields:
            fields = ['id', 'gid', 'completed', 'name', 'notes']

        return self.client.tasks.find_by_id(task_id, fields=fields)

    def get_last_monday(self):
        '''
        Finds the date of the last Monday and returns it as an ISO 8601 format
        string.
        '''
        today = datetime.date.today()

        last_monday = today - datetime.timedelta(days=today.weekday())

        return last_monday.isoformat()
