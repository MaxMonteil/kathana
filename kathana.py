import os
from services import AsanaService
from services import EmailService

WORKSPACE = "Accessibility Web Engine"
OUT_DIR = "./reports"


def main():
    asana_service = AsanaService(
        token=os.environ["ASANA_TOKEN"],
        workspace_name=WORKSPACE,
        verbose=True,
    )

    asana_service.generate_report().write_report_to_file(OUT_DIR)

    email_service = EmailService(
        from_email=os.environ["OWNER_EMAIL"],
        to_emails="mbdeir@aub.edu.lb",
        cc_emails=[
            "mnh34@mail.aub.edu",
            "mmd56@mail.aub.edu",
            "mhk46@mail.aub.edu",
            "wze03@mail.aub.edu",
            "mmm110@mail.aub.edu",
            "mmm114@mail.aub.edu",
        ],
        subject=f'Project UK TechHub report from {asana_service.get_report_date()}',
        md_report=asana_service.get_report(),
    )

    email_service.send_email()


if __name__ == "__main__":
    main()
