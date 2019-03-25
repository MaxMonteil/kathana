import os
from pprint import pprint
from resources.asanacomm import Asanacomm

WORKSPACE = 'Accessibility Web Engine'


def main():
    acomm = Asanacomm(os.environ['ASANA_TOKEN'], WORKSPACE)

    for project in acomm.projects:
        pprint(project, indent=4)


if __name__ == '__main__':
    main()
