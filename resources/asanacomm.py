from pathlib import Path
import asana
import datetime


class Asanacomm:
    '''
    A class to communicate with Asana. It fetches all the tasks in a workspace
    upto a date and generates a markdown report.

    Parameters:
        token <str> Personal Access Token (PAT) of user
        workspace_name <str> Name of the workspace to analyze
        output_directory <str> Directory in which to ouput report
    '''

    def __init__(self, token, workspace_name, output_directory):
        self.client = self.init_client(token)
        self.workspace_id = self.fetch_workspace_id(workspace_name)
        self.output_directory = Path(output_directory)

        if not self.workspace_id:
            raise ValueError(f'There is no "{workspace_name}" workspace.')

        self.projects = self.fetch_projects()

    def init_client(self, token):
        print('Connecting to Asana...')
        client = asana.Client.access_token(token)
        client.options['client_name'] = 'Kathana'

        return client

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

    def fetch_workspace_tasks(self, since):
        '''
        Goes through each project in a workspace and fetches the tasks it
        contains going back to the date given by "since".

        Parameters:
            since <str> ISO 8601 format date, gets tasks completed since then
        '''
        print('Fetching workspace tasks')

        for project in self.projects:
            print(f'Fetching tasks in {project["name"]}')
            yield self.fetch_project_tasks(project['gid'], since)

    def fetch_project_tasks(self, project_id, since):
        '''
        Fetches the data of all the tasks in a particular project that were
        completed since the given date.

        Parameters:
            project_id <str> The unique id of the project
            since <str> ISO 8601 format date, gets tasks completed since then
        '''
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
            fields = ['id', 'gid', 'completed', 'name', 'notes', 'due_on']

        return self.client.tasks.find_by_id(task_id, fields=fields)

    def get_last_monday(self):
        '''
        Finds the date of the last Monday and returns it as an ISO 8601 format
        string.
        '''
        today = datetime.date.today()

        last_monday = today - datetime.timedelta(days=today.weekday())

        return last_monday.isoformat()

    def generate_report(self, start_date=None):
        '''
        smth
        '''
        if not start_date:
            start_date = self.get_last_monday()

        file_name = start_date.replace(" ", "") + '-report.md'
        file_path = Path.joinpath(self.output_directory, file_name)

        if not Path.exists(file_path):
            Path.touch(file_path, exist_ok=True)

        print('Generating report...')
        report_data = self.fetch_workspace_tasks(start_date)

        report = {
                    'date': start_date,
                    'completed': [],
                    'planned': []
                 }

        for project_tasks in report_data:
            for task in project_tasks:
                status = 'completed' if task['completed'] else 'planned'

                report[status].append({
                    'name': task['name'],
                    'description': task['notes'],
                    'due_on': task['due_on']})

        print('Done!')
        print('Writing report to file...')
        with open(file_path, 'w') as out:
            out.write(f'# Progress report for {start_date}\n\n')

            out.write('## Completed Tasks\n\n')

            for task in report['completed']:
                out.write(f'### {task["name"]}\n\n')
                out.write(f'task["description"]\n\n')

            out.write('## Planned Tasks\n\n')

            for task in report['planned']:
                out.write(f'### {task["name"]}\n\n')
                if task["due_on"]:
                    out.write(f'> Due on: task["due_on"]\n')
                out.write(f'task["description"]\n\n')

        print(f'Done! Report written at {file_path}')
