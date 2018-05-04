# rbk3_verify.py
# For each tar file, verify with list_file.
# By Nameten on 2018-04-19

# Usage:
# rbk1_plan.py <path> <target_name> [segment_size=100(M)]
# rbk2_run.py                             // normal to run many times
# rbk3_verify.py [tar_files]              // optional

# Design:
# rbk_all.dat -- rbk_target.dat
# -> rbk_list_0001.job
# -> output/xxx_0001.tar -- output/rbk_list_0001.txt
# -> rbk_verify.dat -- rbk_verify_0001.tmp


import os, sys
import subprocess
import glob, re

def verify(output_file, origin_file):
    # Check if there is a leading "/" in origin_file.
    # If any, use another diff_cmd
    f = open(origin_file)
    if f.readline()[0]=="/":
        # For some special files added by macos, diff needs -I
        # e.g. "home/a/._README.txt"
        diff_cmd = "cut -c 2- '%s' | diff -I '.*/\._.*' -q '%s' -" \
                   % (origin_file, output_file)        
    else:
        diff_cmd = "diff -I '.*/\._.*' -q '%s' '%s'" \
                   % (output_file, origin_file)
    f.close()

    res = subprocess.run(diff_cmd, shell=True, stdout=subprocess.PIPE)
    if len(res.stdout) > 0:
        return False
    else:
        return True
    
def main():
    if len(sys.argv) >= 2:
        files = sys.argv[1:]
    else:
        files = glob.glob("*.tar")
    count = len(files)
    for tar_file in files:
        m = re.match(".*_(\d{4}).tar$", tar_file)
        if m:
            list_file = "rbk_list_"+ m.group(1) +".txt"
            if not os.path.isfile(list_file):
                print("------->No list for "+ tar_file)
                count -= 1
                continue
            tar_cmd = "tar tf '%s' > rbk_verify.tmp" % tar_file
            # print(tar_cmd)
            res = subprocess.run(tar_cmd, shell=True, stderr=subprocess.PIPE)
            if len(res.stderr) > 0:
                print(res.stderr)
            if not verify("rbk_verify.tmp", list_file):
                print("------->Bad: "+ tar_file)
                count -= 1
        else:
            print("------->Not rbk file: "+ tar_file)
            count -= 1

    print("Total %d files are ok." % count)

if __name__ == "__main__":
    main()
