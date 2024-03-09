from pulp import LpProblem, LpVariable, lpSum, LpMinimize

def lp(costs, output, demands):
    # Create a MILP problem
    model = LpProblem(name="ex2", sense=LpMinimize)

    # Variables
    x = {
        factory: {
            storage_unit: LpVariable(name=f"x_{factory+1}_{storage_unit+1}", lowBound=0)
            for storage_unit in range(0, 4)
        }
        for factory in range(0, 3)
    }

    #  Objective function
    model += lpSum(x[factory][storage_unit] * costs[factory][storage_unit] for factory in range(0, 3) for storage_unit in range(0, 4))

    # Output Constraints
    for factory in range(0, 3):
        model += lpSum(x[factory][storage_unit] for storage_unit in range(0, 4)) <= output[factory]
    # Demand Constraints
    for storage_unit in range(0, 4):
        model += lpSum(x[factory][storage_unit] for factory in range(0, 3)) >= demands[storage_unit]


    # Solve the problem
    model.solve()

    # Display the results
    print("Variables: ")
    for x in model.variables():
        print(f"{x.name} = {x.value()}")

def main():

    # Costs of transporting from factory to storage unit
    costs = {}
    costs[0] = [1.5, 1.8, 1.9, 1.3]
    costs[1] = [2.1, 1.4, 1.5, 1.7]
    costs[2] = [2.5, 1.2, 1.7, 2.2]

    output = {}
    output[0] = 500
    output[1] = 750
    output[2] = 700

    demands = {}
    demands[0] = 300
    demands[1] = 600
    demands[2] = 200
    demands[3] = 450

    # Solve the lp problem and its dual
    lp(costs, output, demands)

if __name__ == "__main__":
    main()