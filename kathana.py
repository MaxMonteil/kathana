from pathlib import Path
from services import AsanaService, EmailService, write_report_to_file
import argparse
import os

WORKSPACE = "Accessibility Web Engine"
OUT_DIR = "./reports"
REPORT_FORMATS = AsanaService.FORMATS
DEFAULT_FORMAT = AsanaService.DEFAULT_FORMAT


def main(args):
    asana_service = AsanaService(
        token=os.environ["ASANA_TOKEN"],
        workspace_name=WORKSPACE,
        verbose=not args.quiet,
    )

    asana_service.generate_report()

    if args.output:
        print(asana_service[args.format])

    if args.write:
        write_report_to_file(
            report=asana_service[args.format],
            report_format=args.format,
            out_dir=(Path(args.write) or OUT_DIR),
            start_date=asana_service.start_date,
        )

    if args.email:
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
            subject=f"Project UK TechHub report from {asana_service.report_date}",
            report=asana_service.html_report,
        )

        email_service.send_email()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate an Asana report.")
    parser.add_argument(
        "-q", "--quiet", help="supress logging messages", action="store_true"
    )

    parser.add_argument(
        "-f",
        "--format",
        help="format to in which to save or send the report",
        choices=REPORT_FORMATS,
        default=DEFAULT_FORMAT,
    )

    parser.add_argument(
        "-w",
        "--write",
        help="write report to dir or file, filename defaults "
        "to <start_date>_report.<format>",
        metavar="FILE|DIR",
    )

    parser.add_argument(
        "-o", "--output", help="print report to stdout", action="store_true"
    )

    parser.add_argument(
        "-e",
        "--email",
        help="send report to receiver and cc emails",
        action="store_true",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
