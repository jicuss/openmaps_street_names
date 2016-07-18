import count_street_names
import argparse
import datetime
import logging
import os
__version__ = '1.0.0rc0'


def streetCountMain():
    default_log_path = os.path.abspath(os.path.join(__file__,'..','..', 'logs'))
    parser = argparse.ArgumentParser(description="OpenMap Street Name Parser")
    parser.add_argument('group', help='Tableau Group to run')
    parser.add_argument('-d', '--logFolder', default=default_log_path, help='Location of the log folder.  Default is {}'.format(default_log_path))
    parser.add_argument('-l', '--logLevel', default='DEBUG', choices=["DEBUG", "INFO", "ERROR", "CRITICAL"], help='This is the logging level used by the logging module, the default is INFO.')
    parser.add_argument('-f', '--logFile', default='streetnames.log', help='Name of the log file to use.  Default is streetnames.log')
    args = parser.parse_args()
    level = logging.INFO

    logFileNameLocation = args.logFolder + "/" + str(datetime.datetime.now().isoformat()) + "-" + args.logFile

    if args.logLevel == "DEBUG":
        level = logging.DEBUG
    elif args.logLevel == "INFO":
        level = logging.INFO
    elif args.logLevel == "ERROR":
        level = logging.ERROR
    elif args.logLevel == "CRITICAL":
        level = logging.CRITICAL

    count_street_names.main(args.group, level, logFileNameLocation)
