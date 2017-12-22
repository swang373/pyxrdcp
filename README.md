# pyxrdcp

The files composing the real and simulated datasets analyzed by the Compact Muon Solenoid (CMS) experiment are distributed globally and in large part accessed using the XRootD protocol. A common task is the bulk transfer of files from one data center to another in order to reduce the latency for those analysts further from CERN and provide a measure of redundancy. In such a large collaboration, there are probably tools which already exist for this purpose, but in my ignorance of them I've created this quick and dirty wrapper around the `xrdcp` command line utility.

## Installation

This was developed, tested, and used at **cmslpc**, but it should work for **lxplus** or any other environment where the following dependencies are installed:

* Python 2.7 (and various Python packages...)
* xrdcp
* voms-proxy-init

*All* of these are taken care of by setting up a CMSSW environment, e.g. `CMSSW_9_4_0_pre3`, and then creating a Python virtual environment based on the interpreter distributed with CMSSW using the following commands:

```bash
virtualenv -p "$(which python)" venv

# Activate the virtual environment (must be done every time)
source venv/bin/activate

# Deactivate an active virtual environment
deactivate
```

Once the virtual environment is activated, installing is simply

```bash
pip install pyxrdcp
```

If you must build it manually, download the release tarball, unpack it, and install using setuptools:

```bash
# Example to be filled in
```

If all else fails, you can simply download the `pyxrdcp.py` and `utils.py` files within the `pyxrdcp` directory of the repository and drop them in your working directory. They should work assuming the depencies are satisfied.

## Usage

The command line utility has two arguments:

* `INPUT_FILE`
  This is the path to a file containing logical filenames of the source files separated by newlines. The logical filenames are automatically converted to full XRootD URLs. Note that `stdin` (-) is also accepted, so one can pipe in the output of `das_client` invoked with the `--limit=0` option.
* `DST`
  This is the destination directory to which the source files are copied and must be a valid XRootD URL. The directory is created if it does not exist.

There are also two options:

* `-j`, `--maxworkers`
  The number of concurrent workers executing copy jobs. The default is the number of available cores.
* `--redirector`
  This is the XRootD redirector used to transform logical filenames to XRootD URLs. The default is the global redirector `cms-xrd-global.cern.ch`.

And if you forget all this or want to see the usage syntax quickly, just invoke the command with the usual `-h` or `--help` option.

A few examples of calling the command:

```bash
pyxrdcp filelist.txt root://cmseos.fnal.gov///store/user/some_user/some_dataset --redirector xrootd-cms.infn.it

pyxrdcp filelist.txt root://eosuser.cern.ch///store/user/s/some_user/some_dataset -j 8 --redirector cmsxrootd.fnal.gov
```

You should see a progress tracker for the number of copy jobs completed and the number of successful and failed jobs.

## Troubleshooting

* The underlying call to `xrdcp` uses the `--silent` and `--posc` options and not `--force` (if the file already exists at the destination, the copy will fail).
* Any messages that would've been emitted to stderr are redirected to stdout and will stack above the progress tracker, so no debugging information is lost.
* The executable will hang if it is trying to access remote files that require a VOMS proxy but one isn't available (the underlying call to `xrdcp` will prompt the user for a password). The easiest way to avoid that is to have a valid VOMS proxy before executing the command.
