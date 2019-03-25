import os
from resources.asanacomm import Asanacomm

WORKSPACE = 'Accessibility Web Engine'
OUT_DIR = './reports'


def main():
    acomm = Asanacomm(os.environ['ASANA_TOKEN'], WORKSPACE, OUT_DIR,
                      start_date='2019-03-18', verbose=True)

    acomm.generate_report()
    acomm.write_report_to_file()


if __name__ == '__main__':
    main()
