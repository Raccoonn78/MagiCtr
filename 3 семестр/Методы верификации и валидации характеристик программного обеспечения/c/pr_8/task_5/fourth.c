/*@
  requires n > 0;
  requires \valid(cost + (0 .. n-1)) && \valid(value + (0 .. n-1));
  requires k >= 0;
  ensures \result == -1 || (0 <= \result < n && value[\result] >= k);
  ensures \forall integer i; 0 <= i < n ==> (value[i] >= k ==> cost[\result] <= cost[i]);
*/
int minCostForGivenValue(int n, int *cost, int *value, int k) {
    int r = -1;
    /*@
      loop invariant 0 <= i <= n;
      loop invariant -1 <= r < n;
      loop invariant \forall integer j; 0 <= j < i ==> (value[j] >= k ==> r == -1 || cost[r] <= cost[j]);
      loop assigns i, r;
      loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        if (value[i] >= k) {
            if (r == -1 || cost[i] < cost[r]) {
                r = i;
            }
        }
    }
    return r;
}
