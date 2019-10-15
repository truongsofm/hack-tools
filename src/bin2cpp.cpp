// write ( encrypted ) binary file to stdout
#include <iostream>
#include <string>
#include <fstream>
#include <time.h>
void main(int argc, char * argv[]){
    if(argc==1){
        printf("Usage : %s <file>\n", argv[0]);
        return;
    }
    srand( (unsigned) time(NULL) );  
    const int XOR_KEY_SIZE = 256;
    char * XOR_KEY = new char[XOR_KEY_SIZE];
    printf("#define XOR_KEY_SIZE %d\n", XOR_KEY_SIZE);
    printf("#define XOR_KEY \"");
    for(int i = 0; i < XOR_KEY_SIZE; i++ ) {
        XOR_KEY[i] = (char)rand()%256;
        printf("\\x%X", (unsigned char)XOR_KEY[i]);
    }
    printf("\"\n");
    printf("// %s\n", argv[1]);
    printf("static char pe_byte[] = {");
    using namespace std;
    char c; int pe_size = 0;
    ifstream f (argv[1], ios::binary);
    if(!f) return;
    while (f.get(c)) {
        if(pe_size!=0) printf(",");
        if((pe_size)%XOR_KEY_SIZE==0) putchar('\n');
        printf("%4d", _rotl8(c^_rotl8(XOR_KEY[pe_size%XOR_KEY_SIZE], pe_size%8), pe_size%8));
        pe_size++;
    }
    f.close();
    printf("\n};\n");
    // printf("int pe_size = %d;\n", pe_size);
    return;
    // for(int i=0; i<pe_size; i++){
    //    pe_byte[i] =  pe_byte[i]^(int)(_rotr8(XOR_KEY[i%XOR_KEY_SIZE], 8-i%8));
    // }
}
