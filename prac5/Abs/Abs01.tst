load Abs.asm,
output-file Abs01.out,
compare-to Abs01.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2;

set PC 0,
set RAM[0] 3,
set RAM[1] 3;
repeat 20{
    ticktock;
}
set RAM[1] 3;
output;