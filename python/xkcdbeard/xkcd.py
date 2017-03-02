from subprocess import check_call
import logging

logger = logging.getLogger(__name__)


def get_latest():
    logger.debug("Updating xkcd db")
    check_call("xkcd-dl --update-db", shell=True)
    logger.debug("Getting all xkcd comics.")
    check_call("xkcd-dl -l --path=.", shell=True)


def get_specific(num):
    logger.debug("Getting comic {}".format(num))
    check_call("xkcd-dl -d {} --path=.".format(num), shell=True)
