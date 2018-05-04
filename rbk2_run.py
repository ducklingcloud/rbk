# rbk2_run.py
# Given the job files, run 'tar' one by one.
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
import glob

def get_one_job():
    jobs = glob.glob("*.job")
    return jobs[0] if len(jobs) > 0 else None
    
def main():
    # Confirm existing jobs
    if not os.path.isfile("rbk_target.dat"):
        print("No jobs. Please run rbk1_plan.py first.")
        sys.exit()

    if not os.path.isdir("output"):
        os.mkdir("output")
    with open("rbk_target.dat") as f:
        target = f.readline().strip()
        
    while True:
        job_file = get_one_job()
        if job_file is None:
            break;
        tar_file = job_file.replace("rbk_list", target).replace("job", "tar")
        tar_cmd = "tar cf 'output/%s' -T %s" % (tar_file, job_file)
        # print(tar_cmd)
        res = subprocess.run(tar_cmd, shell=True, stderr=subprocess.PIPE)
        if len(res.stderr) > 0:
            print(res.stderr)
        done_file = "output/"+ job_file.replace("job", "txt")
        os.replace(job_file, done_file)
    
# main()

if __name__ == "__main__":
    main()
