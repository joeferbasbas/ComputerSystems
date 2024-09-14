load Mult.asm,
output-file Mult05.out,
compare-to Mult05.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;

set PC 0,
set RAM[0] -9,
set RAM[1] 3,
set RAM[2] -3;
repeat 100{
    ticktock;
}


set RAM[1] 3,
set RAM[2] -3,
output;