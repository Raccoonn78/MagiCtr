// Модель Promela для нахождения НОД
mtype = { start, gcd, end };

active proctype GCD() {
    int a, b;
    int result;
    
    // Инициализация значений
    a = 48;
    b = 18;
    
    do
    :: (b != 0) ->
        int temp = b;
        b = a % b;
        a = temp;
    :: (b == 0) ->
        result = a;
        break;
    od;
    
    // Печать результата (можно заменить на вызов функции)
    printf("НОД равен %d\n", result);
}

init {
    run GCD();
}
