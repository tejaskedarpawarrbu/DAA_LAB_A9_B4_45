def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    direction = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                direction[i][j] = 0 
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                    direction[i][j] = 1 
                else:
                    dp[i][j] = dp[i][j - 1]
                    direction[i][j] = 2  

    lcs_length = dp[m][n]
    lcs = [""] * lcs_length
    i, j = m, n
    index = lcs_length - 1

    while i > 0 and j > 0:
        if direction[i][j] == 0:  
            lcs[index] = X[i - 1]
            index -= 1
            i -= 1
            j -= 1
        elif direction[i][j] == 1: 
            i -= 1
        else: 
            j -= 1

    return dp, lcs_length, "".join(lcs)


X = "AGCCCTAAGGGCTACCTAGCTT"
Y = "GACAGCCTACAAGCGTTAGCTTG"

cost_matrix, final_cost_lcs, lcs_sequence = longest_common_subsequence(X, Y)

print("Cost matrix with all costs:")
for row in cost_matrix:
    print(row)

print(f"\nFinal cost of LCS (length): {final_cost_lcs}")
print(f"LCS is: {lcs_sequence}")