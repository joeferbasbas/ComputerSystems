@R0
M = 0            

@R1
D = M            
@END
D;JEQ            

@CHECKNEGATIVES
D;JLT

@NEG
D;JLT

@POS
D;JGT








(POS)
@R2
D = M

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


@R0
M = M + D

@R1
D = M + 1
M = D

@NEG
D;JLT

@R0
M = !M
M = M + 1
@END
D;JEQ





(CHECKNEGATIVES)
@R2
D = M
@NEG
D;JLT
@POSSECONDNUM
D;JGT



(POSSECONDNUM)
@R2
D = M

@R0
M = M + D        

@R1        
D = M + 1
M = D

@POSSECONDNUM
D;JLT
@R0
M = !M
M = M + 1


@END
D;JEQ





(END)
@END
0;JMP             
