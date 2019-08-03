import cplex
from sortedcontainers import SortedList
nbPeople = 2
nbJobs = 2
happyniess = [[1,3], [5,1]]

#problem variables
assignvars = []

class Staff:
    def __init__(self, cost):
        self.cost = cost
        self.counter = 1

    def __lt__(self, other):
        return self.cost < other.cost

    # return comparison
    def __le__(self, other):
        return self.cost <= other.cost

    # return comparison
    def __eq__(self, other):
        return self.cost == other.cost

    # return comparison
    def __ne__(self, other):
        return self.cost != other.cost

    # return comparison
    def __gt__(self, other):
        return self.cost > other.cost

    # return comparison
    def __ge__(self, other):
        return self.cost >= other.cost
    def __str__(self):
        return "cost is " + str(self.cost)



    def __iter__(self):
        return self

# return comparison
def varIndex(i,j):
    return i * nbPeople + j * (nbJobs - 1)
def setupProblem(c):
    c.objective.set_sense(c.objective.sense.maximize)
    allAssignvars = []
    allCosts = []
    for i in range(nbPeople):
        assignvars.append([])
        for j in range(nbJobs):
            varName = "assign person" + "_" + str(i) + " to job " + str(j)
            assignvars[i].append(varName)

            allAssignvars.append(varName)
            allCosts.append(happyniess[i][j])

    c.variables.add(names=allAssignvars, types= ['B'] * len(allAssignvars), obj=allCosts)
    print (c.variables.get_names())

    #each person can only be assigned to only one job, sum over j  assignvars[i][j] = 1 for each i
    for i in range(nbPeople):
        thevars = []
        thecoefs = []
        for j in range(nbJobs):
            print (i,j)
            thevars.append(assignvars[i][j])
            thecoefs.append(1)
        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(thevars, thecoefs)],
            senses=["E"],
            rhs=[1])

    #each job can only be assigned to one person, sum over i assignvars[i][j] = 1 for each j
    for j in range(nbJobs):
        thevars = []
        thecoefs=[]
        for j in range(nbPeople):
            thevars.append(assignvars[i][j])
            thecoefs.append(1)
        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(thevars, thecoefs)],
            senses=["E"],
            rhs=[1])




def simpleAssign():
    c = cplex.Cplex()
    setupProblem(c)
    c.solve()

    print()
    print("Solution status :", c.solution.get_status())
    print("objective            : {0:.2f}".format(
        c.solution.get_objective_value()))

    print("Solution values:")
    for i in range(nbPeople):
        print("   {0}: ".format(i), end='')
        for j in range(nbJobs):
            print("{0:.2f}\t".format(
                c.solution.get_values(varIndex(i, j))),
                end='')
        print()

    sl = SortedList(['e', 'a', 'c', 'd', 'b'])
    print(sl)

    s1 = Staff(20)
    s2 = Staff(10)
    staff = [s1]
    staff.append(s2)
    for i in staff:
        print(i)

    sk = SortedList([s1,s2])
    for i in sk:
        print(i)
    print(sk)
    sk.remove(s2)
    print(sk)
