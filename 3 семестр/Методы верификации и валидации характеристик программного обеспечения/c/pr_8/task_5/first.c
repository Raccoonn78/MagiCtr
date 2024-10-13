/*@
  requires n > 1;
  ensures 1 <= \result < n;
  ensures n % \result == 0;
  ensures \forall integer d; 1 <= d < n ==> (n % d == 0 ==> d <= \result);
*/
int maxDivisor(int n) {
    int m = 1;
    /*@
      loop invariant 1 <= i < n;
      loop invariant 1 <= m < n;
      loop invariant n % m == 0;
      loop assigns i, m;
      loop variant i;
    */
    for (int i = n - 1; i > 0; i--) {
        if (n % i == 0) {
            if (i > m) {
                m = i;
            }
        }
    }
    return m;
}
