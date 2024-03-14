from pulp import LpProblem, LpVariable, LpMaximize, lpSum

def lp(efficiency, cap, investment_duration, start_period):

    n_periods = 5
    n_strategies = 5

    # Create a linear programming problem
    model = LpProblem(name="ex3", sense=LpMaximize)

    x = {
        t: {
            s: LpVariable(name=f"loss_{t+2010}_{s+1}", lowBound=0)
            for s in range(n_strategies)
        }
        for t in range(n_periods)
    }

    g = {
        t: {
            s: LpVariable(name=f"gain_{t+2010}_{s+1}", lowBound=0)
            for s in range(n_strategies)
        }
        for t in range(n_periods+1)
    }

    # Objective function
    model += 1 - lpSum(lpSum(x[t][s] for s in range(n_strategies)) for t in range(n_periods)) \
                    + lpSum(lpSum(g[t][s] for s in range(n_strategies)) for t in range(n_periods+1))

    # Constraints

    # Investement - gain relationship
    for t in range(n_periods):
        model += lpSum(lpSum(x[t][s] for s in range(n_strategies)) for t in range(t+1)) \
                 <= lpSum(lpSum(g[t][s] for s in range(n_strategies)) for t in range(t+1)) + 1

    # Gain constraints
    for s in range(n_strategies):
        for t in range(start_period[s] + investment_duration[s]):
            model += g[t][s] == 0

    for s in range(n_strategies):
        for t in range(start_period[s] + investment_duration[s], n_periods+1):
            model += g[t][s] == x[t-investment_duration[s]][s] * (efficiency[s]+1)
    # Investment constraints
    for t in range(n_periods):
        for s in range(n_strategies):
            model += x[t][s] <= cap[s]

    for s in range(n_strategies):
        for t in range(start_period[s]):
            model += x[t][s] == 0

    # Do not allow to make the same investment more than once

    # integer variable
    u = {
        t: {
            s: LpVariable(name=f"indicator_{t+2010}_{s+1}", cat="Binary")
            for s in range(n_strategies)
        }
        for t in range(n_periods)
    }

    M = 1000  # large enough number

    for s in range(n_strategies):
        model += lpSum(u[t][s] for t in range(n_periods)) <= 1

    for s in range(n_strategies):
        for t in range(n_periods):
            model += x[t][s] <= M * u[t][s]


    # Solve the problem
    model.solve()
    print("Objective Value: ")
    print(model.objective)

    print("Variables: ")
    for x in model.variables():
        print(f"{x.name} = {x.value()}")
    print("Objective function value: ", model.objective.value())
    print(model.constraints)


    return

efficiency = [0.2, 0.25, 0.4, 0.25, 0.15]
cap = [10, 0.4, 0.4, 0.4, 0.3, 10]
investment_duration = [1, 3, 3, 2, 1]
start_period = [0, 1, 2, 2, 0]

lp(efficiency, cap, investment_duration, start_period)


