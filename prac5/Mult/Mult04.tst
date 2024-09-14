load Mult.asm,
output-file Mult04.out,
compare-to Mult04.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;

set PC 0,
set RAM[0] -2,
set RAM[1] -2,
set RAM[2] 1;
repeat 100{
    ticktock;
}


set RAM[1] -2,
set RAM[2] 1,
output;