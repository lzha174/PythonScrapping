\* 1D cutting stock *\
Minimize
OBJ: Pat0 + Pat1 + Pat2 + Pat3 + Pat5 + Pat6 + Pat7
Subject To
C0: Pat0 + 3 Pat6 >= 65
C1: Pat1 + 2 Pat7 >= 29
C2: Pat2 + 4 Pat5 >= 70
C3: Pat3 >= 84
Bounds
0 <= Pat0
0 <= Pat1
0 <= Pat2
0 <= Pat3
0 <= Pat5
0 <= Pat6
0 <= Pat7
Generals
Pat0
Pat1
Pat2
Pat3
Pat5
Pat6
Pat7
End
