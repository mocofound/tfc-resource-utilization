# tfc-resource-utilization


## About
Python script for gathering workspace and resource utilization metrics

### Prereqs
```
export TFC_TOKEN=mcQWOpWlHHFNgg
python3 -m venv ./venv    
source ./venv/bin/activate
python3 -m pip install requests
python3 -m pip install pandas
```

### How to Use
```
python3 tfc-resource-utilization.py
```

### Output

```
Workspaces per Month (Created and Cumulative):
      Month  Workspaces Created  Cumulative Workspaces
0   2018-12                 1.0                      1
1   2019-01                 2.0                      3
2   2019-02                 4.0                      7
...
53  2023-05                 0.0                     72
54  2023-06                38.0                    110
55  2023-07                 0.0                    110
56  2023-08                 0.0                    110
57  2023-09                 2.0                    112
58  2023-10                 2.0                    114
59  2023-11                 0.0                    114
60  2023-12                 0.0                    114
61  2024-01                 0.0                    114
62  2024-02                 0.0                    114
63  2024-03                 0.0                    114
64  2024-04                 0.0                    114
65  2024-05                 0.0                    114
66  2024-06                 0.0                    114

Resources per Month (Count and Cumulative):
      Month  Number of Resources  Cumulative Resources
0   2018-12                  0.0                   0.0
1   2019-01                  0.0                   0.0
2   2019-02                  0.0                   0.0
3   2019-03                  0.0                   0.0
4   2019-04                  0.0                   0.0
5   2019-05                  0.0                   0.0
6   2019-06                  0.0                   0.0
7   2019-07                  1.0                   1.0
...
60  2023-12                  0.0                 228.0
61  2024-01                  0.0                 228.0
62  2024-02                  0.0                 228.0
63  2024-03                  0.0                 228.0
64  2024-04                  0.0                 228.0
65  2024-05                  0.0                 228.0
66  2024-06                  0.0                 228.0

Current Resources per Workspace:
                                         Workspace Name  Current Number of Resources
0                                tfc-agent-pool-creator                          0.0
1                                        vended_azure_1                          0.0
2                              vended_alex_workspace_10                          0.0
3                                          krys_Test_ws                          0.0
4                                            hashivault                          0.0
5                                              tfc-waas                          1.0
```
