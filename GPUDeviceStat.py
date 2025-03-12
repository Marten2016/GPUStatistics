import os
import sys
import time

str_command = "nvidia-smi"
out_max_path = "./gpu_device_stat_max_result.txt"
out_min_path = "./gpu_device_stat_min_result.txt"
out_avg_path = "./gpu_device_stat_avg_result.txt"

time_interval = 5

result_max_map = dict()
result_min_map = dict()
result_avg_map = dict()
avg_count = 0

while True:

    out = os.popen(str_command)
    text_content = out.read()
    out.close()
    
    content_0 = text_content.split("|===============================+======================+======================|")
    lines = content_0[1].split("+-------------------------------+----------------------+----------------------+")
    
    update_max_tag = False
    update_min_tag = False
    update_avg_tag = False
    avg_count += 1

    for i in range(len(lines)):
        if i >= len(lines)-1:
            break
        #modify "Tesla V100S-PCI" to real type of nvidia
        device = lines[i].split("  Tesla V100S-PCI...  Off")[0].split(" ")[-1]
        #device = lines[i].split("  Tesla V100-PCIE...  Off")[0].split(" ")[-1]
        mem = int(lines[i].split("MiB / ")[0].split(" ")[-1])
        
        #update max mem
        if device in result_max_map:
            if result_max_map[device] < mem:
                result_max_map[device] = mem
                update_max_tag = True
        else:
            result_max_map[device] = mem
            update_max_tag = True
            
        #update min mem
        if device in result_min_map:
            if result_min_map[device] > mem:
                result_min_map[device] = mem
                update_min_tag = True
        else:
            result_min_map[device] = mem
            update_min_tag = True
            
        #update avg mem,record the sum and count
        #mem_float = float(mem)/1024
        if device in result_avg_map:
            prevalue = result_avg_map[device].split(":")
            if int(prevalue[0]) >= sys.maxsize - 32768 or avg_count >= sys.maxsize - 1:
                print("too long to save, finish avg job!")
                continue
            sum_value = int(prevalue[0]) + int(mem)
            avg_mem = (int(prevalue[0]) * avg_count + mem)//(avg_count +1)
            result_avg_map[device] = ':'.join([str(avg_mem), str(avg_count)])
            update_avg_tag = True
        else:
            result_avg_map[device] = ':'.join([str(mem), str(avg_count)])
            update_avg_tag = True
            
    #write result to file    
    if update_max_tag:
        fxout = open(out_max_path, "w")
        fxout.write(str(result_max_map))
        fxout.close()
    if update_min_tag:
        fnout = open(out_min_path, "w")
        fnout.write(str(result_min_map))
        fnout.close()
    if update_avg_tag:
        fgout = open(out_avg_path, "w")
        fgout.write(str(result_avg_map))
        fgout.close()
    
    time.sleep(time_interval)
