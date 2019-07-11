rbk -- Resumable Backup

Author: nameten
Created: 2018-04-18
Updated: 2019-07-11

A python tool that can make resumable backup for a huge set of
files. It usually takes long time from several hours to a few days,
where you can not finish such a backup at once and resuming is
required.

Usage
-----

First step, calculate the total size of files to be backuped and
divide them into jobs.

  rbk1_plan.py <path> <target_name> [segment_size=100(M)] [last_rbk_all]

When [last_rbk_all], the file 'rbk_all.dat' created in last backup, is
given, an incremental backup will be executed. Two additional files,
rbk_incremental.dat and rbk_deleted.dat, will be generated in the
working directory. Please check them to ensure that everything is what
you want. The job files (*.job) are created according to
rbk_incremental.dat, instead of rbk_all.dat in normal (full) backup.

If you want to continue an incomplete try, use 'continue' as
<target_name>. Otherwise, the program will refuse to run before you
remove 'rbk_target.dat' in the working directory.
  
Second step, run rbk2_run.py as many times as needed. You can
interrupt a run at any time, for example, by Ctrl-C. The resulting tar
files are in ./output/ directory.

  rbk2_run.py

Last step, do verification if you like. Enter ./output and run
rbk3_verify.py. By default, all tar files in the directory will be
verified. You can verify specific files by providing their names. If
an argument '--all' is given, the verifying process will continue
through the whole file even some difference has already been found.

  rbk3_verify.py [--all] [tar_files]

