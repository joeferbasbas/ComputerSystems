#include <string>

#include "VMTranslator.h"

using namespace std;

/**
 * VMTranslator constructor
 */
VMTranslator::VMTranslator() {
    // Your code here
}

/**
 * VMTranslator destructor
 */
VMTranslator::~VMTranslator() {
    // Your code here
}

/** Generate Hack Assembly code for a VM push operation */
string VMTranslator::vm_push(string segment, int offset) {
    string assembly = "";

    if (segment == "static") {
        assembly = assembly + "@Static." + to_string(offset) + "\n" + "D=M\n";  // Access static variable as Static.i
    }
    else if (segment == "local") {
        assembly = assembly + "@LCL\n" + "D=M\n" + "@" + to_string(offset) + "\n" + "A=D+A\n" + "D=M\n";
    }
    else if (segment == "argument") {
        assembly = assembly + "@ARG\n" + "D=M\n" + "@" + to_string(offset) + "\n" + "A=D+A\n" + "D=M\n";
    }
    else if (segment == "this") {
        assembly = assembly + "@THIS\n" + "D=M\n" + "@" + to_string(offset) + "\n" + "A=D+A\n" + "D=M\n";
    }
    else if (segment == "that") {
        assembly = assembly + "@THAT\n" + "D=M\n" + "@" + to_string(offset) + "\n" + "A=D+A\n" + "D=M\n";
    }
    else if (segment == "temp") {
        assembly = assembly + "@5\n" + "D=A\n" + "@" + to_string(offset) + "\n" + "A=D+A\n" + "D=M\n";  // Temp starts at RAM[5]
    }
    else if (segment == "pointer") {
        if (offset == 0) {
            assembly = assembly + "@THIS\n" + "D=M\n";  // pointer 0 is THIS
        }
        else if (offset == 1) {
            assembly = assembly + "@THAT\n" + "D=M\n";  // pointer 1 is THAT
        }
    }
    else if (segment == "constant") {
        assembly = assembly + "@" + to_string(offset) + "\n" + "D=A\n";  // Load constant into D
    }

    // Push the value in D onto the stack
    return assembly + "@SP\n" + "AM=M+1\n" + "A=A-1\n" + "M=D\n";
}


/** Generate Hack Assembly code for a VM pop operation */
string VMTranslator::vm_pop(string segment, int offset){    
     string assembly = "";

    if (segment == "local") {
        assembly += "@LCL\n";                    
        assembly += "D=M\n";                     
        assembly += "@"+to_string(offset)+"\n";  
        assembly += "D=D+A\n";                   
        assembly += "@R13\n";                    
        assembly += "M=D\n";                     
    }
    else if(segment == "argmuent"){
        assembly += "@ARG\n";                    
        assembly += "D=M\n";                     
        assembly += "@"+to_string(offset)+"\n";  
        assembly += "D=D+A\n";                   
        assembly += "@R13\n";                  
        assembly += "M=D\n";  
    }
    else if(segment == "this"){
        assembly += "@THIS\n";                   
        assembly += "D=M\n";                     
        assembly += "@"+to_string(offset)+"\n";  
        assembly += "D=D+A\n";                   
        assembly += "@R13\n";                    
        assembly += "M=D\n";  
    }
    else if(segment == "that"){
        assembly += "@THAT\n";                    
        assembly += "D=M\n";                     
        assembly += "@"+to_string(offset)+"\n";  
        assembly += "D=D+A\n";                   
        assembly += "@R13\n";                    
        assembly += "M=D\n";  
    }
    else if(segment == "temp"){
        assembly += "@5\n";                    
        assembly += "D=M\n";                    
        assembly += "@"+to_string(offset)+"\n";  
        assembly += "D=D+A\n";                   
        assembly += "@R13\n";                    
        assembly += "M=D\n";  
    }
    else if(segment == "pointer"){
        if(offset == 0){
            assembly += "@THIS\n";               
            assembly += "D=A\n";  
        }
        else if(offset == 1){
            assembly += "@THAT\n";               
            assembly += "D=A\n";  
        }
    }
    else if(segment == "static"){

    }
    

    // Pop from stack
    assembly += "@SP\n";                         // Load SP address
    assembly += "AM=M-1\n";                      // SP--, A = RAM[SP]
    assembly += "D=M\n";                         // D = RAM[SP] (top of the stack)
    assembly += "@R13\n";                        // Load address from R13
    assembly += "A=M\n";                         // A = R13
    assembly += "M=D\n";                         // RAM[R13] = D

    return assembly;
}

/** Generate Hack Assembly code for a VM add operation */
string VMTranslator::vm_add(){
    string assembly;
    assembly += "@SP\n";
    assembly += "AM=M-1\n";      // SP--, A = RAM[SP]
    assembly += "D=M\n";         // D = RAM[SP] (first operand)
    assembly += "@SP\n";
    assembly += "AM=M-1\n";      // SP--, A = RAM[SP-1]
    assembly += "M=D+M\n";       // RAM[SP-1] = RAM[SP-1] + D
    assembly += "@SP\n";
    assembly += "M=M+1\n";       // SP++
    return assembly;
}

/** Generate Hack Assembly code for a VM sub operation */
string VMTranslator::vm_sub(){
    return "";
}

/** Generate Hack Assembly code for a VM neg operation */
string VMTranslator::vm_neg(){
    string assembly;
    assembly += "@SP\n";
    assembly += "A=M-1\n";      // Load top of the stack
    assembly += "M=-M\n";       // Negate the value at the top of the stack
    return assembly;
}

/** Generate Hack Assembly code for a VM eq operation */
string VMTranslator::vm_eq(){
    static int eq_label_counter = 0;
    string label = "EQ_TRUE_" + to_string(eq_label_counter++);
    string end_label = "EQ_END_" + to_string(eq_label_counter);

    string assembly;
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP]
    assembly += "D=M\n";           // D = RAM[SP]
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP-1]
    assembly += "D=M-D\n";         // Subtract (first - second)
    assembly += "@"+label+"\n";    // Jump to true label if D == 0
    assembly += "D;JEQ\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=0\n";           // False (set to 0)
    assembly += "@"+end_label+"\n";
    assembly += "0;JMP\n";         // Unconditional jump to end

    assembly += "("+label+")\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=-1\n";          // True (set to -1)
    
    assembly += "("+end_label+")\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";         // SP++

    return assembly;
}

/** Generate Hack Assembly code for a VM gt operation */
string VMTranslator::vm_gt(){
    static int eq_label_counter = 0;
    string label = "EQ_TRUE_" + to_string(eq_label_counter++);
    string end_label = "EQ_END_" + to_string(eq_label_counter);

    string assembly;
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP]
    assembly += "D=M\n";           // D = RAM[SP]
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP-1]
    assembly += "D=M-D\n";         // Subtract (first - second)
    assembly += "@"+label+"\n";    // Jump to true label if D == 0
    assembly += "D;JGT\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=0\n";           // False (set to 0)
    assembly += "@"+end_label+"\n";
    assembly += "0;JMP\n";         // Unconditional jump to end

    assembly += "("+label+")\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=-1\n";          // True (set to -1)
    
    assembly += "("+end_label+")\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";         // SP++

    return assembly;
}

/** Generate Hack Assembly code for a VM lt operation */
string VMTranslator::vm_lt(){
    static int eq_label_counter = 0;
    string label = "EQ_TRUE_" + to_string(eq_label_counter++);
    string end_label = "EQ_END_" + to_string(eq_label_counter);

    string assembly;
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP]
    assembly += "D=M\n";           // D = RAM[SP]
    assembly += "@SP\n";
    assembly += "AM=M-1\n";        // SP--, A = RAM[SP-1]
    assembly += "D=M-D\n";         // Subtract (first - second)
    assembly += "@"+label+"\n";    // Jump to true label if D == 0
    assembly += "D;JLT\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=0\n";           // False (set to 0)
    assembly += "@"+end_label+"\n";
    assembly += "0;JMP\n";         // Unconditional jump to end

    assembly += "("+label+")\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=-1\n";          // True (set to -1)
    
    assembly += "("+end_label+")\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";         // SP++

    return assembly;
}

/** Generate Hack Assembly code for a VM and operation */
string VMTranslator::vm_and(){
    
}

/** Generate Hack Assembly code for a VM or operation */
string VMTranslator::vm_or(){
    return "";
}

/** Generate Hack Assembly code for a VM not operation */
string VMTranslator::vm_not(){
    return "";
}

/** Generate Hack Assembly code for a VM label operation */
string VMTranslator::vm_label(string label){
    return "(" + label + ")\n"; 
}

/** Generate Hack Assembly code for a VM goto operation */
string VMTranslator::vm_goto(string label){
    return "@" + label + "\n0;JMP\n"; 
}

/** Generate Hack Assembly code for a VM if-goto operation */
string VMTranslator::vm_if(string label){
    string assembly;
    assembly += "@SP\n";
    assembly += "AM=M-1\n";          // SP--, A = RAM[SP]
    assembly += "D=M\n";             // D = RAM[SP]
    assembly += "@" + label + "\n";
    assembly += "D;JNE\n";           // Jump if D != 0
    return assembly;
}

/** Generate Hack Assembly code for a VM function operation */
string VMTranslator::vm_function(string function_name, int n_vars){
    string assembly = "(" + function_name + ")\n";  // Define the function label
    for (int i = 0; i < n_vars; ++i) {
        assembly += "@SP\n";       // Initialize all local variables to 0
        assembly += "A=M\n";
        assembly += "M=0\n";
        assembly += "@SP\n";
        assembly += "M=M+1\n";
    }
    return assembly;
}

/** Generate Hack Assembly code for a VM call operation */
string VMTranslator::vm_call(string function_name, int n_args){
    static int call_counter = 0; // To generate unique labels for return addresses
    string return_label = "RETURN_" + to_string(call_counter++);

    string assembly;

    // 1. Push return address onto the stack
    assembly += "@" + return_label + "\n";
    assembly += "D=A\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=D\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";

    // 2. Push LCL, ARG, THIS, THAT onto the stack (save the caller's state)
    assembly += "@LCL\n";
    assembly += "D=M\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=D\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";

    assembly += "@ARG\n";
    assembly += "D=M\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=D\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";

    assembly += "@THIS\n";
    assembly += "D=M\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=D\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";

    assembly += "@THAT\n";
    assembly += "D=M\n";
    assembly += "@SP\n";
    assembly += "A=M\n";
    assembly += "M=D\n";
    assembly += "@SP\n";
    assembly += "M=M+1\n";

    // 3. Reposition ARG: ARG = SP - n_args - 5
    assembly += "@SP\n";
    assembly += "D=M\n";
    assembly += "@" + to_string(n_args + 5) + "\n"; // n_args + 5
    assembly += "D=D-A\n";
    assembly += "@ARG\n";
    assembly += "M=D\n";

    // 4. Set LCL = SP
    assembly += "@SP\n";
    assembly += "D=M\n";
    assembly += "@LCL\n";
    assembly += "M=D\n";

    // 5. Jump to the function
    assembly += "@" + function_name + "\n";
    assembly += "0;JMP\n";

    // 6. Insert the return address label
    assembly += "(" + return_label + ")\n";

    return assembly;
}

/** Generate Hack Assembly code for a VM return operation */
string VMTranslator::vm_return(){
    string assembly;

    // 1. Store return address in a temporary variable (R14 = return address)
    assembly += "@LCL\n";              // Get LCL (current function’s local base)
    assembly += "D=M\n";
    assembly += "@R13\n";              // Use R13 to store the frame (LCL)
    assembly += "M=D\n";
    assembly += "@5\n";                // Return address is at LCL - 5
    assembly += "A=D-A\n";             
    assembly += "D=M\n";               // D = return address
    assembly += "@R14\n";              // Store return address in R14
    assembly += "M=D\n";

    // 2. Move return value to ARG[0]
    assembly += "@SP\n";               // Get the top of the stack
    assembly += "A=M-1\n";             // A = RAM[SP-1] (top of the stack)
    assembly += "D=M\n";               // D = return value
    assembly += "@ARG\n";              // ARG is the base of the caller's arguments
    assembly += "A=M\n";
    assembly += "M=D\n";               // ARG[0] = return value

    // 3. Reposition SP = ARG + 1
    assembly += "@ARG\n";
    assembly += "D=M+1\n";             // SP = ARG + 1
    assembly += "@SP\n";
    assembly += "M=D\n";

    // 4. Restore the saved state of the caller (THAT, THIS, ARG, LCL)
    assembly += "@R13\n";              // R13 = LCL (frame)
    assembly += "A=M-1\n";             // Restore THAT = *(frame - 1)
    assembly += "D=M\n";
    assembly += "@THAT\n";
    assembly += "M=D\n";

    assembly += "@R13\n";
    assembly += "A=M-1\n";
    assembly += "A=A-1\n";             // Restore THIS = *(frame - 2)
    assembly += "D=M\n";
    assembly += "@THIS\n";
    assembly += "M=D\n";

    assembly += "@R13\n";
    assembly += "A=M-1\n";
    assembly += "A=A-1\n";
    assembly += "A=A-1\n";             // Restore ARG = *(frame - 3)
    assembly += "D=M\n";
    assembly += "@ARG\n";
    assembly += "M=D\n";

    assembly += "@R13\n";
    assembly += "A=M-1\n";
    assembly += "A=A-1\n";
    assembly += "A=A-1\n";
    assembly += "A=A-1\n";             // Restore LCL = *(frame - 4)
    assembly += "D=M\n";
    assembly += "@LCL\n";
    assembly += "M=D\n";

    // 5. Jump to return address (R14)
    assembly += "@R14\n";
    assembly += "A=M\n";
    assembly += "0;JMP\n";

    return assembly;
}