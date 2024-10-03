// Load the length of the array into D (R2 contains the length)
@R2
D = M          // D = length of the array
D = D - 1      // D = length - 1 (for outer loop counter)
@i
M = D          // Store outer loop counter (i = length - 1)

// Outer loop (runs from i = length-1 to 1)
(OUTER_LOOP)
@i
D = M
@SORT_DONE     // If i == 0, sorting is complete
D;JEQ

// Initialize inner loop counter (j = 0)
@j
M = 0

// Inner loop for comparing and swapping adjacent elements
(INNER_LOOP)
@j
D = M
@i
A = M
D = D - A      // D = j - i, stop inner loop when j == i
@NEXT_OUTER    // Exit inner loop if j >= i
D;JGE

// Calculate the address of A[j]
@R1            // R1 holds the base address of the array
D = M          // D = base address of the array
@j
A = M
D = D + A      // D = base address + j (address of A[j])
@R4            // Store address of A[j] in R4
M = D

// Load the value of A[j] into D
@R4
A = M
D = M          // D = A[j]
@R5
M = D          // Store A[j] in R5 (temporary)

// Calculate the address of A[j+1]
@R1
D = M          // D = base address of the array
@j
A = M
D = D + A      // D = base address + j
D = D + 1      // D = address of A[j+1]
@R6            // Store address of A[j+1] in R6
M = D

// Load the value of A[j+1] into D
@R6
A = M
D = M          // D = A[j+1]
@R7
M = D          // Store A[j+1] in R7 (temporary)

// Compare A[j] and A[j+1]
@R5
D = M
@R7
D = D - M      // D = A[j] - A[j+1]
@NO_SWAP       // If A[j] <= A[j+1], skip the swap
D;JLE

// Swap A[j] and A[j+1]
// Load A[j] into D and write it to A[j+1]
@R5
D = M
@R6
A = M
M = D          // A[j+1] = A[j]

// Load A[j+1] into D and write it to A[j]
@R7
D = M
@R4
A = M
M = D          // A[j] = A[j+1]

(NO_SWAP)
// Increment inner loop counter (j = j + 1)
@j
M = M + 1
@INNER_LOOP    // Repeat inner loop

(NEXT_OUTER)
// Decrement outer loop counter (i = i - 1)
@i
M = M - 1
@OUTER_LOOP    // Repeat outer loop

(SORT_DONE)
// Sorting is done, set R0 to -1 to indicate completion
@R0
M = -1

(END)
@END
0;JMP
