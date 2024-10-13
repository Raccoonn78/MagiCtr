/*@
  requires n > 1;
  ensures 1 <= \result <= n;
  ensures n % \result == 0;
  ensures \forall integer d; 1 <= d <= n ==> (is_prime(d) && n % d == 0 ==> d <= \result);
*/
int maxPrimeFactor(int n) {
    int min = 1;
    /*@
      loop invariant 1 <= min <= n;
      loop assigns min, n;
      loop variant n;
    */
    do {
        n /= min;
        min = n;
        /*@
          loop invariant 1 < i < n;
          loop assigns i, min;
          loop variant i;
        */
        for (int i = n - 1; i > 1; i--) {
            if (i * i <= n && n % i == 0) {
                min = i;
            }
        }
    } while (min < n);
    return n;
}
