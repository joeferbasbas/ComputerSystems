// Calculates the absolute value of R1 and stores the result in R0.
// (R0, R1 refer to RAM[0], and RAM[1], respectively.)

// Put your code here.
@R1        
D = M      

@END       
D;JGE      

D = -D     

(END)
@R0        
M = D      


