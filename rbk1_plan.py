#!/usr/bin/env python3

# rbk1_plan
# First step, collect info and make plan
# By Nameten on 2018-04-18
# Updated on 2019-07-09

# Usage:
# rbk1_plan.py <path> <target_name> [segment_size=100(M)] [last_rbk_all]
# rbk2_run.py                                     // normal to run many times
# rbk3_verify.py [--all] [tar_files]              // optional

# Design:
# rbk_all.dat, rbk_target.dat, [ rbk_incremental.dat, rbk_deleted.dat ]
# -> rbk_list_0001.job
# -> output/xxx_0001.tar , output/rbk_list_0001.txt
# -> rbk_verify.tmp [diff or line_by_line]


import os, sys
import subprocess
import re

fn_rbk_target      = "rbk_target.dat"
fn_rbk_all         = "rbk_all.dat"
fn_rbk_all_raw     = "rbk_all_raw.dat"
fn_rbk_incremental = "rbk_incremental.dat"
fn_rbk_deleted     = "rbk_deleted.dat"

find_cmd_tmpl = "find $destdir \( -type f -o -type d -empty \) -ls >"+ \
    fn_rbk_all_raw
sort_cmd      = "sort -u -k 11 -o "+ fn_rbk_all +" "+ fn_rbk_all_raw
destdir       = "/kd/dvlp/fes-scheduler-log-analyzing"
segment_unit  = 10*1000*1000     # input_arg in MByte
target        = "target"
last_rbk_all  = ""

def get_args():
    global destdir, target, segment_unit, last_rbk_all
    num = len(sys.argv)
    if num >= 3:
        destdir = "\""+ sys.argv[1] +"\""
        target = sys.argv[2]
        if num > 3:
            segment_unit = int(sys.argv[3])*1000*1000
        if num > 4:
            last_rbk_all = sys.argv[4]
    else:
        print("Usage: rbk1_plan.py <path> <target> [segment_size in MB] [last rbk_all.dat for incremental]")
        print("       Special target: 'continue'")
        sys.exit()

def segment(list_fn: str):
    with open(list_fn) as f:
        seq = 1; sum = 0
        flag_segment = True
        for l in f:
            if flag_segment:
                list_file = open("rbk_list_%04d.job" % seq, "w",
                                 buffering=4096*1024)
                flag_segment = False
            fields = l.split(maxsplit=10)
            list_file.write(fields[10])
            sum += int(fields[6])
            if sum >= segment_unit:
                list_file.close()
                sum = 0
                seq += 1
                flag_segment = True

        # Maybe close twice, but it's ok
        list_file.close()

def main():
    get_args()

    # Check existing and warn
    if os.path.isfile(fn_rbk_target):
        if target != "continue":
            print("Something exists. Please remove "+ fn_rbk_target +" and *.job and try again if you want to start a new one.")
            sys.exit(0)
    else:
        f = open(fn_rbk_target, "w")
        f.write(target +"\n")
        f.close()

    if target != "continue" or not os.path.isfile(fn_rbk_all_raw):
        find_cmd = find_cmd_tmpl.replace("$destdir", destdir)
        res = subprocess.run(find_cmd, shell=True, stderr=subprocess.PIPE)
        # -> rbk_all_raw.dat
        if len(res.stderr) > 0:
            print(res.stderr)
            sys.exit(1)
    if target != "continue" or not os.path.isfile(fn_rbk_all):
        res = subprocess.run(sort_cmd, shell=True, stderr=subprocess.PIPE)
        # -> rbk_all.dat
        if len(res.stderr) > 0:
            print(res.stderr)
            sys.exit(1)

    if last_rbk_all != "":
        file_incremental = open(fn_rbk_incremental, "w")
        file_deleted = open(fn_rbk_deleted, "w")
        with open(last_rbk_all) as f_last:
            with open(fn_rbk_all) as f_now:
                l_last = f_last.readline()
                l_now  = f_now.readline()
                flag_last = flag_now = True
                while l_last != "" and l_now != "":
                    if flag_last:
                        fields_last = l_last.split(maxsplit=10)
                        path_last = fields_last[10]
                        flag_last = False
                    if flag_now:
                        fields_now  = l_now.split(maxsplit=10)
                        path_now = fields_now[10]
                        flag_now = False
                    if path_last < path_now:
                        file_deleted.write(l_last)
                        l_last = f_last.readline()
                        flag_last = True 
                    elif path_last > path_now:
                        file_incremental.write(l_now)
                        l_now = f_now.readline()
                        flag_now = True
                    else:
                        if l_last != l_now and \
                           ("".join(fields_last[0:9]) != \
                            "".join(fields_now[0:9]) or \
                            not re.fullmatch("[0-9]{4}", fields_now[9]) or \
                            not re.fullmatch("[0-9:]{5}", fields_last[9])):
                            file_incremental.write(l_now)
                        l_last = f_last.readline()
                        l_now  = f_now.readline()
                        flag_last = flag_now = True

                while l_last != "":
                    file_deleted.write(l_last)
                    l_last = f_last.readline()
                while l_now != "":
                    file_incremental.write(l_now)
                    l_now = f_now.readline()

        file_deleted.close()
        file_incremental.close()
        segment(fn_rbk_incremental)
    else:
        segment(fn_rbk_all)


# main()

if __name__ == "__main__":
    main()
