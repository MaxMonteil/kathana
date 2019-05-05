from services import AsanaService, EmailService, WritingService
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
        start_date=args.start_date,
        verbose=not args.quiet,
    )

    asana_service.generate_report()

    if args.output_path == 'stdout':
        print(asana_service[args.output])
    else:
        WritingService.write(
            report=asana_service[args.output],
            report_format=args.output,
            out_dir=args.output_path,
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
        "-q", "--quiet", help="Supress logging messages", action="store_true"
    )

    parser.add_argument(
        "--output",
        help="Format in which to generate the report, defaults to markdown",
        choices=REPORT_FORMATS,
        default=DEFAULT_FORMAT,
    )

    parser.add_argument(
        "--output-path",
        help="The file path to ouput the results. Default is 'stdout'",
        default="stdout",
    )

    parser.add_argument(
        "-e",
        "--email",
        help="send report to receiver and cc emails",
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--start-date",
        help="Date from which to start generating report, defaults to last Monday " +
        "(format YYYY-MM-DD)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
