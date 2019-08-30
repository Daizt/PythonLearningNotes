// 给定一个五子棋棋盘状态，判断哪一方（‘0’方或者‘1’方）获胜，如都未满足五子相连则为平局。

#include <stdio.h>

int check(int D[][7], int M, int N);
int _check(int D[][7], int x, int y);

int main()
{
    int D[][7] = {{1,0,0,1,1,0,1},
                  {1,1,0,0,0,1,1},
                  {1,0,1,1,0,0,0},
                  {0,1,1,1,0,0,0},
                  {1,0,0,1,0,1,1},
                  {0,1,0,0,1,1,0},
                  {1,0,1,1,0,1,0}};
    int retval;

    retval = check(D, 7, 7);

    if (retval == -1){
        printf("Draw!\n");
    }else{
        printf("%d wins!\n", retval);
    }

    return 0;
}

int check(int D[][7], int M, int N)
{
    int i, j, retval;

    for (i=0; i<M-4; i++){
        for (j=0; j<N-4; j++){
            retval = _check(D, i, j);
            printf("D[%d][%d] check result: %d\n", i, j, retval);
            if(retval != -1){
                return retval;
            }
        }
    }
    // draw
    return -1;
}

int _check(int D[][7], int x, int y)
{
    int i, j, count1, count2;

    // check rows & columns
    count1 = 0;
    count2 = 0;
    for (i=0; i<5; i++){
        for (j=0; j<5; j++){
            count1 += D[i+x][j+y];
            count2 += D[j+x][i+y];
        }
        if (count1==0 || count2==0){
            return 0;
        }
        if (count1==5 || count2==5){
            return 1;
        }
        count1 = 0;
        count2 = 0;
    }
    // check diagonal
    count1 = 0;
    count2 = 0;
    for (i=0; i<5; i++){
        count1 += D[i+x][i+y];
        count2 += D[4-i+x][i+y];
    }
    if (count1==0 || count2==0){
        return 0;
    }
    if (count1==5 || count2==5){
        return 1;
    }
    // draw
    return -1;
}

