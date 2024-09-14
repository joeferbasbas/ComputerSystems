load Mult.asm,
output-file Mult03.out,
compare-to Mult03.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;

set PC 0,
set RAM[0] 4,
set RAM[1] -4,
set RAM[2] -1;
repeat 100{
    ticktock;
}


set RAM[1] -4,
set RAM[2] -1,
output;