#!/usr/bin/env python
# MIT License
# 
# Copyright (c) 2017 Sean-Jiun Wang
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import multiprocessing
import subprocess

import click
import concurrent.futures
import tqdm

import utils


def copy(url, dst):
    """Copy a file to a directory using xrdcp.
    
    Returns None if the xrdcp call is successful,
    otherwise it returns the error message.
    """
    try:
        output = subprocess.check_output(['xrdcp', '--posc', '--silent', url, dst], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('input_file', type=click.File('rb'))
@click.argument('dst')
@click.option('-j', '--maxworkers', default=multiprocessing.cpu_count(),
    help='The number of concurrent worker processes.'
)
@click.option('--redirector', default='cms-xrd-global.cern.ch',
    help='The XRootD redirector prepended to bare logical filenames.'
)
def cli(input_file, dst, maxworkers, redirector):
    """Copy files from one XRootD directory to another.

    The INPUT_FILE argument is the path to a text file of logical
    filenames separated by newlines.

    The DST argument is the XRootD URL to the output directory,
    which will be created if it does not exist.

    Note that files are not forcibly copied to the destination!
    """
    urls = [
        line if line.startswith('root') else 'root://{0}/{1}'.format(redirector, line)
        for line in input_file.read().splitlines()
    ]

    utils.makedirs(dst)

    with concurrent.futures.ProcessPoolExecutor(maxworkers) as executor:
        futures = [executor.submit(copy, url, dst) for url in urls]
    
        pbar = tqdm.tqdm(concurrent.futures.as_completed(futures), bar_format='{desc}', unit='job')

        n_good, n_bad = 0, 0
        progress_template = '[{0!s} Succeeded | {1!s} Failed] '

        for future in pbar:
            result = future.result()
            if result is None:
                n_good += 1
            else:
                n_bad += 1
                pbar.write(result.strip())
            pbar.set_description(progress_template.format(n_good, n_bad))


if __name__ == '__main__':

    cli()

