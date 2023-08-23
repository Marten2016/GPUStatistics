import os
import time

str_command = "nvidia-smi"
out_path = "gpu_device_stat_result.txt"
time_interval = 5

result_map = dict()

while True:

    out = os.popen(str_command)
    text_content = out.read()
    out.close()
    
    content_0 = text_content.split("|===============================+======================+======================|")
    #content_1 = content_0[1].split("+-------------------------------+----------------------+----------------------+\n                                                                               \n+-----------------------------------------------------------------------------+")
    
    lines = content_0[1].split("+-------------------------------+----------------------+----------------------+")
    
    update_tag = False
    for i in range(len(lines)):
        if i >= len(lines)-1:
            break
        device = lines[i].split("  Tesla V100S-PCI...  Off")[0].split(" ")[-1]
        #device = lines[i].split("  Tesla V100-PCIE...  Off")[0].split(" ")[-1]
        mem = lines[i].split("MiB / ")[0].split(" ")[-1]
        if device in result_map:
            if result_map[device] < mem:
                result_map[device] = mem
                update_tag = True
        else:
            result_map[device] = mem
            update_tag = True
    if update_tag:
        fout = open(out_path, "w")
        fout.write(str(result_map))
        fout.close()
        update_tag = False
    time.sleep(time_interval)
