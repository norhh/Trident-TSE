#include <stdio.h>

#ifndef TRIDENT_OUTPUT
#define TRIDENT_OUTPUT(id, typestr, value) value
#endif

int main(int argc, char *argv[]) {
  int x = atoi(argv[1]);
  for (int i=0; i<3; i++)
    __trident_choice_int("10", (int*[]){&x}, (char*[]){"x"}, 1, (int*[]){&x}, (char*[]){"x"}, 1);
  return TRIDENT_OUTPUT("x", "i32", x);
}
