#include <stdio.h>

/*@ 
  requires a >= 0 && b >= 0;
  ensures \result == \old(a) || \result == \old(b);
  ensures \result > 0;
  ensures a % \result == 0 && b % \result == 0;
  assigns a, b;
*/
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

/*@ 
  assigns \nothing;
*/
int main() {
    int num1, num2;
    printf("Введите два целых числа: ");
    scanf("%d %d", &num1, &num2);

    int result = gcd(num1, num2);
    printf("НОД чисел %d и %d равен %d\n", num1, num2, result);

    return 0;
}
