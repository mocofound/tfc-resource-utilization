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
Cumulative Workspaces per Month:
     Month  Cumulative Number of Workspaces
    
0  2019-01                                1
1  2019-11                                2
2  2020-02                                4
3  2020-03                                5
4  2020-06                                7
5  2020-09                                8
6  2022-02                                9
7  2023-06                               16
8  2023-09                               18
9  2023-10                               20

Cumulative Resources per Month:
     Month  Cumulative Number of Resources
0  2019-11                              20
1  2020-02                              47
2  2020-03                              67
3  2020-06                              85
4  2020-09                              91
5  2022-02                              93
6  2023-06                             100

Cumulative Resources per Workspace per Month:
           Workspace ID    Month  Cumulative Number of Resources
0   ws-52xssn82VGDCgWKx  2019-11                              20
1   ws-DVc1pnoaT5vVfVwU  2023-06                               1
2   ws-LnX3CgC5p4YXqaWY  2022-02                               2
3   ws-YmVetWWTeURxCwhU  2020-09                               6
4   ws-ohs2DAkvTkeKKEez  2020-02                              20
5   ws-su3jSSgSWo9Lncy5  2020-06                               9
6   ws-tHKjtBYUPnpUYieX  2020-03                              20
7   ws-tMoCnn7xU6WfJqyj  2020-06                               9
8   ws-xZSkWtUVyg41nhnN  2023-06                               2
9   ws-yMwoxLbnck7NbWHV  2023-06                               4
10  ws-zEG4YBQkoiQwHhLc  2020-02                               7
```
