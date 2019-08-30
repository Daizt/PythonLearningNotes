/* C Programming Notes */

/* 1. 二维数组作为函数参数 */
// Method_1：
#include <stdio.h>

void foo(int D[][7], int M, int N);

int main()
{
    int D[][7] = {{1,0,0,1,1,0,1},
	              {1,1,0,0,0,1,1},
	              {1,0,1,1,0,0,0},
	              {0,1,1,1,0,0,0},
	              {1,0,0,1,0,1,1},
	              {0,1,0,0,1,1,0},
	              {1,0,1,1,0,1,0}};

	foo(D, 3, 3);
	return 0;
}

void foo(int D[][7], int M, int N)
{
	// 打印出以D[M][N]为顶点的3X3矩阵
	int i;
	for(i=0; i<3; i++){
		printf("[%d, %d, %d]\n", D[M+i][N+0], D[M+i][N+1], D[M+i][N+2]);
	}
}

// Method_2:
#include <stdio.h>

void foo(int (*D)[7], int M, int N);

int main()
{
    int D[][7] = {{1,0,0,1,1,0,1},
	              {1,1,0,0,0,1,1},
	              {1,0,1,1,0,0,0},
	              {0,1,1,1,0,0,0},
	              {1,0,0,1,0,1,1},
	              {0,1,0,0,1,1,0},
	              {1,0,1,1,0,1,0}};

	foo(D, 3, 3);
	return 0;
}

void foo(int (*D)[7], int M, int N)
{
	// 打印出以D[M][N]为顶点的3X3矩阵
	int i;
	for(i=0; i<3; i++){
		printf("[%d, %d, %d]\n", D[M+i][N+0], D[M+i][N+1], D[M+i][N+2]);
	}
}

// Notice:
// 1、int D[][7]和int (*D)[7]都表示D是一个二维数组指针，其数据类型为 int (*)[7];
// 2、不论是声明、传参还是初始化，二维数组的第二维都不能省略；
// 3、我们可以通过强制转化D的类型来间接实现矩阵reshape,
	int Dp[][2] = (int (*)[2]) D;
// 4、int * D[7] 表示指针数组，即数组D中包含7个整形指针；