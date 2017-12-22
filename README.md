# pyxrdcp

The files composing the real and simulated datasets analyzed by the Compact Muon Solenoid (CMS) experiment are distributed globally and in large part accessed using the XRootD protocol. A common task is the bulk transfer of files from one data center to another in order to reduce the latency for those analysts further from CERN and provide a measure of redundancy. In such a large collaboration, there are probably tools which already exist for this purpose, but in my ignorance of them I've created this quick and dirty wrapper around the `xrdcp` command line utility.

## Installation

This was developed, tested, and used at **cmslpc**, but it should work for **lxplus** or any other environment where the following dependencies are installed:

* Python 2.7 (and various Python packages...)
* xrdcp
* voms-proxy-init

*All* of these are taken care of by setting up a CMSSW environment, e.g. `CMSSW_9_4_0_pre3`.

I'm not distributing this as a Python package, so you should either copy the files in the repository to your working area or download and unpack the tarball of the standalone version packaged using pyinstaller.

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
  This is the XRootD used when transforming logical filenames to XRootD URLs. The default is the global redirector `cms-xrd-global.cern.ch`.

And if you forget all this or want to see the usage syntax quickly, just invoke the command with the usual `-h` or `--help` option.

If you downloaded the files, you can invoke the command line utility as the Python script that it is:

```bash
python pyxrdcp filelist.txt root://cmseos.fnal.gov///store/user/some_user/some_dataset -j 4 --redirector xrootd-cms.infn.it
```

If you downloaded the tarball, simply unpack it and use the executable:

```bash
./pyxrdcp filelist.txt root://eosuser.cern.ch///store/user/s/some_user/some_dataset -j 8 --redirector cmsxrootd.fnal.gov
```

Either way, you should see a progress tracker for the number of copy jobs completed and the number of successful and failed jobs.

## Troubleshooting

* The underlying call to `xrdcp` uses the `--silent` and `--posc` options and not `--force` (if the file already exists at the destination, the copy will fail).
* Any messages that would've been emitted to stderr are redirected to stdout and will stack above the progress tracker, so no debugging information is lost.
* The executable can hang if it is trying to access remote files that require a VOMS proxy (the underlying call to `xrdcp` will prompt the user for a password). Easiest way to avoid that is to always have a valid VOMS proxy created.
