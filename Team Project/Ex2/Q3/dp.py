def dp(n, memo={}):
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Check if the result is already memoized
    if n in memo:
        return memo[n]

    # Calculate the result recursively and memoize it
    memo[n] = dp(n - 1, memo) + dp(n - 2, memo)

    return memo[n]


# Example usage
n = 5
print("dp({}) = {}".format(n, dp(n)))
