from pathlib import Path


def write(*, report, report_format, out_dir, report_date, verbose=True):
    log = print if verbose else lambda *a, **k: None

    out_dir = Path(out_dir)
    if not out_dir.exists():
        if out_dir.suffix:
            out_dir.parent.mkdir(parents=True, exist_ok=True)
        else:
            out_dir.mkdir(parents=True, exist_ok=True)

    if not out_dir.suffix:
        file_name = report_date + "-report." + report_format
        out_dir = out_dir.joinpath(file_name)

    log("\nWriting report to file...")
    with open(out_dir, "w") as out:
        out.write(report)

    log("Done!")
    log(f"\nReport written to: {out_dir.absolute()}")
