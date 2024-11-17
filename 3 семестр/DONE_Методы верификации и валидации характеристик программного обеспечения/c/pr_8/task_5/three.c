/*@
  requires n >= 0;
  ensures \result * \result <= n < (\result + 1) * (\result + 1);
*/
int isqrt(int n) {
    int a = 0;
    int b = 1;
    int c = 1;
    /*@
      loop invariant b <= n + 1;
      loop invariant a * a <= n;
      loop assigns a, b, c;
      loop variant n - b;
    */
    for(; b <= n; a++) {
        c += 2;
        b += c;
    }
    return a;
}
