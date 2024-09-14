load Abs.asm,
output-file Abs03.out,
compare-to Abs03.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2;

set PC 0,
set RAM[0] 2000,
set RAM[1] 2000;
repeat 15{
    ticktock;
}
output;