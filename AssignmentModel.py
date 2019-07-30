from pulp import *

rooms = ['c1', 'c2', 'c3']
people = ['john', 'mike', 'oddo']
""" start from first row, first col, second col and then wrap to second row """
scores = [6, 4, 1, 5, 2, 5, 8, 1, 7]

# The problem variables are created
assignments = LpVariable.dicts("Assign", (people, rooms), 0, 1, LpInteger)

print(assignments)

for p in people:
    for r in rooms:
        print (assignments[p][r])
prob = LpProblem("Assignment model", LpMaximize)

prob += sum(scores[i * 3 + j] * assignments[person][room] for i, person in enumerate(people) for j, room in enumerate(rooms))

print(prob)
# constaints
# a person must be asigned to a room
for p in people:
    prob += sum([assignments[p][room] for room in rooms]) == 1, "must_assign_%s"%p

print(prob)

# a room can only be assigned with one person
for r in rooms:
    prob += sum([assignments[p][r] for p in people]) == 1, "must_assign_room_%s"%r

print(prob)



# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print ("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print (v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print ("Total objetive is ", value(prob.objective))