def longest_repeating_subsequence(S):
    n = len(S)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

  
    for i in range(1, n + 1):
        for j in range(1, n + 1):
       
            if S[i - 1] == S[j - 1] and i != j:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])


    lrs_length = dp[n][n]
    lrs = [""] * lrs_length
    i, j = n, n
    index = lrs_length - 1

    while i > 0 and j > 0:
        if dp[i][j] == dp[i - 1][j - 1] + 1:
            lrs[index] = S[i - 1]
            index -= 1
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j]:  
            i -= 1
        else:  # Move left
            j -= 1

    return dp, lrs_length, "".join(lrs)


S = "AABCBDC"

cost_matrix_lrs, lrs_length, lrs_sequence = longest_repeating_subsequence(S)

print("Cost matrix for LRS:")
for row in cost_matrix_lrs:
    print(row)

print(f"\nLength of LRS: {lrs_length}")
print(f"LRS is: {lrs_sequence}")