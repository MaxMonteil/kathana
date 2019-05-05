from pathlib import Path


def write(
    self, *, report, report_format, out_dir, start_date, verbose=True
):
    log = print if verbose else lambda *a, **k: None

    out_dir = Path(out_dir)
    if not out_dir.suffix:
        file_name = start_date.replace(" ", "") + "-report." + report_format
        file_path = Path.joinpath(out_dir, file_name)

    if not Path.exists(file_path):
        Path.touch(file_path, exist_ok=True)

    log("\nWriting report to file...")
    with open(file_path, "w") as out:
        out.write(report)

    log(f"Done!")
    log("\nReport written here:", end=" ")
    log(Path.joinpath(Path.cwd(), file_path))
