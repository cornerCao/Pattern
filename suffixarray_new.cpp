/* 
 * Memo: 多串最长公共子串 后缀数组 
 * Input: 输入字符串个数和字符串数组，这里为了避免unicode，把字符用ord转换成了int型
 * Output: 输出公共子串长度*覆盖字符串数最大的结果的长度和起始位置
*/  
#include <Python.h>
#include <iostream>  
#include <cstdio>  
#include <fstream>
#include <cstdlib>  
#include <cmath>  
#include <cstring>  
#include <stack>
#include <vector>
#include <exception>
const int MAXL = 0x1000f, MAXN = 5002;
class StkEle{
public:
    int _height;
    int _loc;
    bool _ba[MAXN];
    StkEle(){
        _height = 0;
        _loc = 0;
        memset(_ba, 0, sizeof(_ba));
    }
    StkEle(int h, int l, int idx1, int idx2){
        _height = h;
        _loc = l;
        memset(_ba, 0, sizeof(_ba));
        _ba[idx1] = true;
        _ba[idx2] = true;
    }
};
struct RetRes//返回值结构体
{
    int len;
    int covernum;
    int pos;
}retres;
struct SuffixArray  //后缀数组
{  
    struct RadixElement  
    {  
        int id;
        int k[2];  
    };
    struct RadixElement RE[MAXL];
    struct RadixElement RT[MAXL];  
    int N;
    int A[MAXL];
    int SA[MAXL];
    int Rank[MAXL];
    int Height[MAXL];
    int C[MAXL];  
    void radix_sort() 
    {  
        int i = 0;
        int y = 0;  
        for (y = 1; y >= 0; y--)  
        {  
            memset(C, 0, sizeof(C));  
            for (i = 1; i <= N; i++)
            { 
                C[RE[i].k[y]]++;  
            }
            for (i = 1; i < MAXL; i++)
            {
                C[i] += C[i-1];  
            }
            for (i = N; i >= 1; i--)
            {
                RT[C[RE[i].k[y]]--] = RE[i];  
            }
            for (i = 1; i <= N; i++)
            {
                RE[i] = RT[i];  
            }
        }  
        for (i = 1; i <= N; i++)  
        {  
            Rank[RE[i].id] = Rank[RE[i-1].id];  
            if (RE[i].k[0] != RE[i-1].k[0] || RE[i].k[1] != RE[i-1].k[1])
            {
                Rank[RE[i].id]++;  
            }
        }  
    }  
    void calc_sa()  
    {  
        int i = 0;
        int k = 0;  
        RE[0].k[0] = -1;  
        for (i = 1; i <= N; i++)  
        {
            RE[i].id = i;
            RE[i].k[0] = A[i];
            RE[i].k[1] = 0;
        }  
        radix_sort();  
        for (k = 1; k+1 <= N; k *= 2)  
        {  
            for (i = 1; i <= N; i++)  
            {
                RE[i].id = i;
                RE[i].k[0] = Rank[i];
                RE[i].k[1] = i+k <= N? Rank[i+k]: 0;
            }  
            radix_sort();  
        }  
        for (i = 1; i <= N; i++)  
        {
            SA[Rank[i]] = i;  
        }
    }  
    void calc_height()  
    {  
        int i = 0;
        int k = 0;
        int h = 0;  
        for (i = 1; i <= N; i++)  
        {  
            if (Rank[i] == 1)  
            {
                h = 0;  
            }
            else  
            {  
                k = SA[Rank[i] - 1];  
                if (--h < 0)
                {
                    h = 0;  
                }
                for (; A[i+h] == A[k + h]; h++)
                {
                    int a = 1;//dummy
                }
            }  
            Height[Rank[i]] = h;  
        }  
    }  
}g_sa;  
int g_n;
int g_bel[MAXL];   
void init(int strnum, int* strarr)  //init global array
{  
    int i = 0;  
    g_sa.N = 0;  
    int startidx = 0;
    g_n = strnum;
    for (i = 1; i <= g_n; i++)  
    {  
        int len = *(strarr + startidx); 
        for (int p = 1; p <= len; p++)
        {
            int tmp = *(strarr + startidx + p);
            g_sa.A[++g_sa.N] = tmp;
            g_bel[g_sa.N] = i;
        }    
        startidx += (len + 1);
        if (i < g_n)  
        {
            g_sa.A[++g_sa.N] = 1000 + i;  
        }
    } 
}  
void mysolve()  
{  
    int i = 0;
    int j = 0;
    int k = 0;  
    std::stack<StkEle>stk;
    g_sa.calc_sa();  
    g_sa.calc_height();  
    int maxlen = 0;
    int maxcover = 0;
    int maxidx = 0;
    for (i = 1; i <= g_sa.N; i++)  
    {
        if (stk.empty() || g_sa.Height[i] >= stk.top()._height)
        {
            stk.push(StkEle(g_sa.Height[i], i - 1, g_bel[g_sa.SA[i]], g_bel[g_sa.SA[i - 1]]));
        }
        else
        {
            bool ba[MAXN];
            int cover = 0;
            memset(ba, 0, sizeof(ba));
            while (!stk.empty() && (g_sa.Height[i] < stk.top()._height))
            {
                StkEle top(stk.top());
                stk.pop();
                for (int i = 1; i <= g_n; i++)
                {
                    if (ba[i] == false && top._ba[i] == true)
                    {
                        cover += 1;
                        ba[i] = true;
                    }
                }
                if (top._height * cover > maxlen * maxcover)
                {
                    maxlen = top._height;
                    maxcover = cover;
                    maxidx = top._loc;
                }
            }
            ba[g_bel[g_sa.SA[i]]] = true;
            ba[g_bel[g_sa.SA[i - 1]]] = true;
            StkEle tmp(g_sa.Height[i], i - 1, g_bel[g_sa.SA[i]], g_bel[g_sa.SA[i - 1]]);
            memcpy(&tmp._ba[0], &ba[0], sizeof(ba));
            stk.push(tmp);
        }
    }
            bool ba[MAXN];
            int cover2 = 0;
            memset(ba, 0, sizeof(ba));
            while (!stk.empty())
            {
                StkEle top2(stk.top());
                stk.pop();
                for (int i = 1; i <= g_n; i++)
                {
                    if (ba[i] == false && top2._ba[i] == true)
                    {
                        cover2 += 1;
                        ba[i] = true;
                    }
                }
              //  v.push_back(resele(top.height,cover,top.loc));
                if (top2._height * cover2 > maxlen * maxcover)
                {
                    maxlen = top2._height;
                    maxcover = cover2;
                    maxidx = top2._loc;
                }
            }
            int respos = 0;
            for (int i = 1; i <= g_sa.N; i++)
            {
                if (maxidx == g_sa.Rank[i])
                {
                    respos = i;
                }
            }
            retres.len = maxlen;
            retres.covernum = maxcover;
            retres.pos = respos;
            return;
}  
/*
extern "C"{
    RetRes solve(int strnum, int* strarr)
    {

            init(strnum, strarr);
            RetRes retres = mysolve();
            return retres;     
    }
}*/
static PyObject* solve(PyObject* self, PyObject* args){
    PyObject* py_tuple;
    int* strarr;
    int strnum;
    int len;
    if (!PyArg_ParseTuple(args, "iiO", &strnum, &len, &py_tuple))
        return NULL;
    strarr = (int*)malloc(len*4);
    while(len--){
        strarr[len] = (int)PyInt_AsLong(PyTuple_GetItem(py_tuple,len));
    }
    init(strnum, strarr);
    mysolve();
    return Py_BuildValue("iii", retres.len, retres.covernum, retres.pos);
}
static PyMethodDef solve_methods[] = {
    {"solve", (PyCFunction)solve, METH_VARARGS},
    {NULL, NULL}
};
PyMODINIT_FUNC initLCS(){
    Py_InitModule3("LCS", solve_methods,"solve lcs problem");
}
