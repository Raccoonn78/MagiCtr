/*@
  requires \valid(arr + (0 .. n-1));
  requires n > 0;
  ensures \result == -1 || arr[\result] == key;
*/
int bsearch(int* arr, int n, int key) {
    int low = 0, high = n - 1;
    /*@
      loop invariant 0 <= low && high < n;
      loop assigns low, high;
    */
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == key) {
            return mid;
        } else if (arr[mid] < key) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}
