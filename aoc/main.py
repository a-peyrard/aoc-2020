"""
Empty main...
"""
import logging

import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)

log = logging.getLogger(__name__)


def main():
    log.info("nothing to run, see sub-modules for problems, and check the tests directory to execute the problems")


if __name__ == "__main__":
    main()
