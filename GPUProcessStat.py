import os
import time

str_command = "nvidia-smi"
out_path = "gpu_process_stat_max_result.txt"
time_interval = 1

result_map = dict()

while True:

    out = os.popen(str_command)
    text_content = out.read()
    out.close()
    
    content = text_content.split("|=============================================================================")
    
    lines = content[1].split("|\n|    ")
    update_tag = False
    for i in range(len(lines)):
        if i+1 == len(lines):
            break
        card = lines[i+1].split('   N/A  N/A')[0]
        pid = lines[i+1].split("      C   ")[0].split(" ")[-1]
        mem = lines[i+1].split("      C   ")[1].split("MiB")[0].split(" ")[-1]
        card_pid = '_'.join([str(card), str(pid)])
        if card_pid in result_map:
            if result_map[card_pid] < mem:
                result_map[card_pid] = mem
                update_tag = True
        else:
            card_pid = '_'.join([str(card), str(pid)])
            result_map[card_pid] = mem
            update_tag = True
    if update_tag:
        fout = open(out_path, "w")
        fout.write(str(result_map))
        fout.close()
        update_tag = False
    time.sleep(time_interval)



    


