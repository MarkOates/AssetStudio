import os
os.system('python3 parse_subagents.py')
os.system('./scripts/rebuild_viewer.sh > /dev/null 2>&1')
os.system('python3 subagent_helper.py')
