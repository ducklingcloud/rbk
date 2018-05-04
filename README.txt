rbk -- Resumable Backup

Author: nameten
Created: 2018-04-18

A python tool that can make resumable backup for a huge set of
files. It usually takes long time from several hours to a few days,
where you can not finish such a backup at once and resuming is
required.

Usage
-----

First step, calculate the total size of files to be backuped and
divide them into jobs.

  rbk1_plan.py <path> <target_name> [segment_size=100(M)]
  
Second step, run rbk2_run.py as many times as needed. You can
interrupt a run at any time. The resulting tar files are in ./output/
directory.

  rbk2_run.py

Last step, do verify if you like. Enter ./output and run
rbk3_verify.py. By default, all tar files in the directory will be
verified. You can verify specific files by providing their names. If
an argument '--all' is given, the verifying process will continue through
the whole file even some difference has already been found.

  rbk3_verify.py [--all] [tar_files]

