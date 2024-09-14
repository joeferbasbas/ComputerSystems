// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

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
@NEGPOS
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
D = !M
@R0
M = M + D        

@R1        
D = M + 1
M = D

(END)
@END
0;JMP             
