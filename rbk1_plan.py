# rbk1_plan
# First step, collect info and make plan
# By Nameten on 2018-04-18

# Usage:
# rbk1_plan.py <path> <target_name> [segment_size=100(M)]
# rbk2_run.py                                     // normal to run many times
# rbk3_verify.py [--all] [tar_files]              // optional

# Design:
# rbk_all.dat -- rbk_target.dat
# -> rbk_list_0001.job
# -> output/xxx_0001.tar -- output/rbk_list_0001.txt
# -> rbk_verify.tmp [diff or line_by_line]


import os, sys
import subprocess

find_cmd_tmpl = ("find $destdir \( -type f -o -type d -empty \) -ls "
                 "> rbk_all.dat")
destdir       = "/kd/dvlp/fes-scheduler-log-analyzing"
segment_unit  = 10*1000*1000     # input_arg in MByte
target        = "target"

def get_args():
    global destdir, target, segment_unit
    num = len(sys.argv)
    if num >= 3:
        destdir = "\""+ sys.argv[1] +"\""
        target = sys.argv[2]
        if num > 3:
            segment_unit = int(sys.argv[3])*1000*1000
    else:
        print("Usage: rbk1_plan.py <path> <target> [segment_size in MB]")
        sys.exit()

def segment():
    with open("rbk_all.dat") as f:
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
    # Check existing and warn
    if os.path.isfile("rbk_target.dat"):
        print("Something exists. Please remove rbk_target.dat and *.job "
              "and try again if you want to start a new one.")
        sys.exit()
        
    get_args()
    f = open("rbk_target.dat", "w")
    f.write(target +"\n")
    f.close()
    
    find_cmd = find_cmd_tmpl.replace("$destdir", destdir)
    # print(find_cmd)
    res = subprocess.run(find_cmd, shell=True, stderr=subprocess.PIPE)
    if len(res.stderr) > 0:
        print(res.stderr)

    segment()

    
# main()

if __name__ == "__main__":
    main()
