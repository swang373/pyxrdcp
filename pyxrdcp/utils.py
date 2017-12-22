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
import re
import subprocess


XROOTD_URL_RE = re.compile(r'^(?P<redirector>root://[^/]+)//(?P<path>.*)$')


class URLParsingError(Exception):
    pass


def parse_url(url):
    """Return the redirector and path of an XRootD URL."""
    match = XROOTD_URL_RE.match(url)
    if match:
        return match.group('redirector'), match.group('path')
    else:
        raise URLParsingError('Unable to parse {0} as an XRootD URL'.format(url))


def makedirs(url):
    """Recursively create an XRootD directory."""
    redirector, path = parse_url(url)
    subprocess.check_call(['xrdfs', redirector, 'mkdir', '-p', path])

