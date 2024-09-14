@R0
M = 0            

@R1
D = M            
@END
D;JEQ            

@NEG
D;JLT

@POS
D;JGT


(POS)
@R2
D = M
@POSNEG
D;JLT

@R0
M = M + D        

@R1        
D = M - 1
M = D

@POS
D;JGT
@R1
D = M          
@END
D;JEQ









(NEG)
@R2
D = M
@NEGPOS
D;JGT

@R0
M = M + D

@R1
D = M + 1
M = D

@NEG
D;JLE

@R0
D = !M
M = D














(NEGPOS)
D = M
@POSNEG
D;JGT

D = !M
@R0
M = M + D        

@R1        
D = M + 1
M = D
@NEGPOS
D;JLE












(POSNEG)
@R2
D = M
@R0
M = M + D        

@R1        
D = M - 1
M = D
@POSNEG
D;JGT


(END)
@END
0;JMP             
