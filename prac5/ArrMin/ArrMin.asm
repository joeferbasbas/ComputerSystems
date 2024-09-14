// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R1
D = M

@R0
M = D
(LOOP)
@R2
D = M
@END
D;JEQ

@R1
A = M
D = M

@R0
D = D - M

@LESS
D;JLT

@NEXT
0;JMP

(LESS)
@R1        // Load the current element address again
A = M      // A = RAM[R1], point to the current element
D = M      // D = RAM[R1], load the current element value into D

@R0        // Update R0 with the new smallest value
M = D      // M = D, store the new smallest value in R0

(NEXT)
@R1        // Move to the next element in the array
M = M + 1  // Increment R1 to point to the next element in the array

@R2        // Decrement the counter (R2)
M = M - 1  // R2 = R2 - 1, decrease the number of elements left to check

@LOOP
0;JMP

(END)


