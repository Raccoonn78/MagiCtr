/*@
  requires b > 0;
  ensures a == \result * b + \result % b;
*/
int idiv(int a, int b) {
    int q = 0;
    int r = a;
    /*@
      loop invariant r >= 0;
      loop invariant a == q * b + r;
      loop assigns q, r;
      loop variant r;
    */
    while (r >= b) {
        q++;
        r -= b;
    }
    return q;
}
