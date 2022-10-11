# NOTE: before running this script, uncomment L116 in grid.py or add a break after pygame.display.update() because we don't want to wait for
# the user to manually close the GUI window for each test_case

import subprocess

def avg_path(choice):
    path_sum = 0.0
    for i in range(1, 51):
        cmd_call = subprocess.Popen(f"python grid.py {choice} grids/test_case_{i}.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in cmd_call.stdout.readlines():
            if line.startswith("AStar") or line.startswith("ThetaStar"):
                words = line.split()
                path_sum += float(words[-1])
                print(f"i: {i}, length: {words[-1]}, sum so far: {path_sum}")
                break
    print("\nFINISHED\n")
    return path_sum/50

def avg_time(choice):
    time_sum = 0.0
    for i in range(1,51):
        # NOTE: the command line argument is specific to using a PowerShell command in Windows (no in-built command for Command Prompt)
        # For Linux/UNIX use: command = f"time python grid.py {choice} grids/test_case_{i}.txt"
        command = f"powershell -Command Measure-command {{python grid.py {choice} grids/test_case_{i}.txt}}"
        cmd_call = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in cmd_call.stdout.readlines():
            if line.startswith("TotalSeconds"):
                words = line.split()
                time_sum += float(words[-1])
                print(f"i: {i}, time: {words[-1]}, sum so far: {time_sum}")
                break
    print("\nFINISHED\n")
    return time_sum/50

astar_path_avg = avg_path("astar")
astar_time_avg = avg_time("astar")
thetastar_path_avg = avg_path("thetastar")
thetastar_time_avg = avg_time("thetastar")

print(f"AStar avg path length: {astar_path_avg}\n\n")
print(f"ThetaStar avg path length: {thetastar_path_avg}\n\n")
# results for latest test:
# AStar avg path length: 44.21188309203678
# ThetaStar avg path length: 41.991167311730436
# ThetaStar's path is 5% lesser. Also, if estimating by comparing the values, thetastar path is 2-3 units smaller than astar

print(f"AStar avg execution time: {astar_time_avg}\n\n")
print(f"ThetaStar avg execution time: {thetastar_time_avg}\n\n")
# results for latest test:
# AStar avg execution time: 1.3736262079999997
# ThetaStar avg execution time: 1.3905123780000002
# AStar's execution time is 1.21% faster. More importantly, if estimating by comparing the values, AStar takes 7-10ms lesser than ThetaStar
