import argparse
import datetime
import logging
import os
from multiprocessing import Pool

import pandas as pd
from git import GitCommandError, Repo
from termcolor import colored


def git_clone(number, name, url, output_dir):
    dirname = number + '_' + name
    into = os.path.join(output_dir, dirname)
    try:
        Repo.clone_from(url, into)
        print(dirname, colored('OK', 'green'))
    except GitCommandError:
        print(dirname, colored('FAIL', 'red'))
        logging.error(dirname)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output dir')
    parser.add_argument('-n', '--num_processes', type=int,
                        help='number of processes')

    args = parser.parse_args()

    # Create dir
    logdir = os.path.join(args.output, 'logs')
    os.makedirs(logdir, exist_ok=True)

    # Logger
    logfile = datetime.datetime.now().isoformat() + '.log'
    fh = logging.FileHandler(os.path.join(logdir, logfile))
    logger = logging.getLogger()
    logger.addHandler(fh)

    # Process Pool
    pool = Pool(args.num_processes)

    df = pd.read_excel(args.input)

    for index, row in df.iterrows():
        number = row['StudentNumber']
        name = row['Name']
        url = row['GitRepo']

        number = str(number)
        pool.apply_async(git_clone, args=(number, name, url, args.output))
        # git_clone(number, name, url, args.output)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
