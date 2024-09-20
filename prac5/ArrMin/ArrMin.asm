// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R1
D = M

@R0
M = D

(LOOP)
@R1
A = A + 1
D = M
@R0
D = D - M

@LESS
D;JLT

@NEXT
D;JGT


(LESS)
@R1
D = M
@R0
M = D
@R2
D = M - 1

@LOOP
D;JGT





(NEXT)
@R0
M = A
@R2
D = M - 1

@LOOP
D;JGT