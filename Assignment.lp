\* Assignment model *\
Maximize
OBJ: 6 Assign_john_c1 + 4 Assign_john_c2 + Assign_john_c3 + 5 Assign_mike_c1
 + 2 Assign_mike_c2 + 5 Assign_mike_c3 + 8 Assign_oddo_c1 + Assign_oddo_c2
 + 7 Assign_oddo_c3
Subject To
must_assign_john: Assign_john_c1 + Assign_john_c2 + Assign_john_c3 = 1
must_assign_mike: Assign_mike_c1 + Assign_mike_c2 + Assign_mike_c3 = 1
must_assign_oddo: Assign_oddo_c1 + Assign_oddo_c2 + Assign_oddo_c3 = 1
must_assign_room_c1: Assign_john_c1 + Assign_mike_c1 + Assign_oddo_c1 = 1
must_assign_room_c2: Assign_john_c2 + Assign_mike_c2 + Assign_oddo_c2 = 1
must_assign_room_c3: Assign_john_c3 + Assign_mike_c3 + Assign_oddo_c3 = 1
Binaries
Assign_john_c1
Assign_john_c2
Assign_john_c3
Assign_mike_c1
Assign_mike_c2
Assign_mike_c3
Assign_oddo_c1
Assign_oddo_c2
Assign_oddo_c3
End
