from io import StringIO
from pathlib import Path
import asana
import datetime


class AsanaService:
    """
    A class to communicate with Asana. It fetches all the tasks in a workspace
    upto a date and generates a markdown report.

    Parameters:
        token <str> Personal Access Token (PAT) of user
        workspace_name <str> Name of the workspace to analyze
        start_date <str> Date from which to fetch tasks
        verbose <bool> Whether or not to output progress statements
    Attributes:
        _client <Asana Client> The connection client for Asana
        _raw_report <dict> Raw response from the Asana api
    """

    def __init__(self, token, workspace_name, start_date=None, verbose=False):
        self._verbose = verbose

        if start_date is None:
            self._start_date = self._get_last_monday()
        else:
            self._start_date = start_date

        self._log("Connecting to Asana...")
        self._client = self._init_client(token)

        self._log("\tGathering workspace information.")
        self._workspace = workspace_name
        self._workspace_id = self._fetch_workspace_id(workspace_name)

        if not self._workspace_id:
            raise ValueError(f'There is no "{workspace_name}" workspace.')

        self._raw_report = {}
        self._md_report = StringIO()

        self._log("\tGathering projects.")
        self._projects = self._fetch_projects()

        self._log("Kathana initialization complete.\n")

    def _init_client(self, token):
        """
        Initializes connection to the Asana client.

        Parameters:
            token <str> The Personal Access Token (PAT) of the user
        """
        client = asana.Client.access_token(token)
        client.options["client_name"] = "Kathana"

        return client

    def get_report(self):
        """Return the markdown format report."""
        return self._md_report.getvalue()

    def get_report_date(self):
        """Return the date from which the report is generated."""
        return self._start_date

    def _fetch_workspace_id(self, workspace_name):
        """
        Fetches the workspace's id from Asana based on the workspace name since
        the asana api doesn't work off of the workspace name alone.

        Parameters:
            workspace_name <str> String name of the workspace
        """
        all_workspaces = self._client.workspaces.find_all()

        for workspace in all_workspaces:
            if workspace["name"] == workspace_name:
                return workspace["gid"]

        return None

    def _fetch_projects(self):
        """
        Fetches the id and gid of all projects in the supplied workspace.
        """
        return self._client.projects.find_all(
            {"workspace": self._workspace_id, "archived": False}
        )

    def _fetch_workspace_tasks(self, since):
        """
        Goes through each project in a workspace and fetches the tasks it
        contains going back to the date given by "since".

        Parameters:
            since <str> ISO 8601 format date, gets tasks completed since then
        """
        self._log("Fetching workspace tasks")

        for project in self._projects:
            self._log(f'\tFetching tasks in {project["name"]}')
            yield self._fetch_project_tasks(project["gid"], since)

    def _fetch_project_tasks(self, project_id, since):
        """
        Fetches the data of all the tasks in a particular project that were
        completed since the given date.

        Parameters:
            project_id <str> The unique id of the project
            since <str> ISO 8601 format date, gets tasks completed since then
        """
        search_params = {"project": project_id, "completed_since": since}

        for compact_task in self._client.tasks.find_all(search_params):
            yield self._fetch_task(compact_task["gid"])

    def _fetch_task(self, task_id, fields=[]):
        """
        Fetches the complete information of a particular task.

        Parameters:
            task_id <str> The unique id of a task
            fields <list> String values of the data fields to return
        """
        if not fields:
            fields = ["id", "gid", "completed", "name", "notes", "due_on"]

        return self._client.tasks.find_by_id(task_id, fields=fields)

    def _get_last_monday(self):
        """
        Finds the date of the last Monday and returns it as an ISO 8601 format
        string.
        """
        today = datetime.date.today()

        last_monday = today - datetime.timedelta(days=today.weekday())

        return last_monday.isoformat()

    def generate_report(self):
        """
        Calls all fetching methods to gather tasks in workspace from the start
        date and generates a report object.
        """
        self._log("Gathering report data...")
        report_data = self._fetch_workspace_tasks(self._start_date)

        self._raw_report = {
            "date": self._start_date,
            "project": self._workspace,
            "completed": [],
            "planned": [],
        }

        for project_tasks in report_data:
            for task in project_tasks:
                status = "completed" if task["completed"] else "planned"

                self._raw_report[status].append(
                    {
                        "name": task["name"],
                        "description": task["notes"],
                        "due_on": task["due_on"] if task["due_on"] else "-1",
                    }
                )

        # Sort planned tasks by due date
        sorted(self._raw_report["planned"], key=lambda i: i["due_on"])

        self._log("Done!")

        return self

    def write_report_to_file(self, output_directory):
        """
        """
        if not self._raw_report:
            raise RuntimeError("self.generate_report has not been run yet.")

        file_name = self._start_date.replace(" ", "") + "-report.md"
        file_path = Path.joinpath(Path(output_directory), file_name)

        if not Path.exists(file_path):
            Path.touch(file_path, exist_ok=True)

        # initialize (if not already done) the md format report from the raw report
        self._create_md_report()

        self._log("\nWriting report to file...")
        with open(file_path, "w") as out:
            out.write(self._md_report.getvalue())

        self._log(f"Done!")
        self._log("\nReport written here:", end=" ")
        self._log(Path.joinpath(Path.cwd(), file_path))

    def _create_md_report(self):
        """
        Writes the generated report to the output file given during class
        initialization.
        """
        if self._md_report.tell() == 0:
            self._md_report.write(
                f"# Progress report for the week of {self._start_date}\n\n"
            )

            self._md_report.write(
                "This is the progress report for the team working on the "
            )
            self._md_report.write(f'{self._raw_report["project"]} project.\n\n')

            self._md_report.write("## Completed Tasks\n\n")

            for task in self._raw_report["completed"]:
                self._md_report.write(f'### {task["name"]}\n\n')
                self._md_report.write(f'{task["description"]}')
                if task["description"]:
                    self._md_report.write("\n\n")

            self._md_report.write("## Planned Tasks\n\n")

            for task in self._raw_report["planned"]:
                if task["due_on"] != "-1":
                    self._md_report.write(f'### {task["name"]}\n\n')
                    self._md_report.write(f'> Due: {task["due_on"]}\n\n')
                    self._md_report.write(f'{task["description"]}')
                    if task["description"]:
                        self._md_report.write("\n\n")

            self._md_report.write("---\nReport generated with ❤ by [Kathana]")
            self._md_report.write("(https://github.com/MaxMonteil/kathana).")

    def _log(self, *args, **kwargs):
        """
        Wrapper for the `print()` function to allow control over verbosity.

        Parameters:
            Whatever `print()` usually takes
        """
        if self._verbose:
            print(*args, **kwargs)
