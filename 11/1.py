def power(x, y, serialId):
    r = x + 10
    p = r * y
    p += serialId
    p *= r
    p = (p%1000)//100
    return p-5

if __name__ == '__main__':
    serialId = 1788
    # serialId = 42
    cum_sum_square = {}
    for i in range(0, 301):
        cum_sum_square[(0,i)] = 0
        cum_sum_square[(i,0)] = 0

    for i in range(1, 301):#row(y)
        for j in range(1, 301):#col(x)
            # print(j,i)
            value = cum_sum_square[(j-1,i-1)]
            for k in range(1, j):
                value += power(k, i, serialId)
            for k in range(1, i):
                value += power(j, k, serialId)
            cum_sum_square[(j,i)] = value + power(j, i, serialId)
    
    largest_v = -1000000000
    largest_cord = None
    for i in range(1, 299):
        for j in range(1, 299):
            v = cum_sum_square[(j+2,i+2)] + cum_sum_square[(j-1,i-1)] - cum_sum_square[(j+2,i-1)] - cum_sum_square[(j-1,i+2)]
            if v>largest_v:
                largest_v = v
                largest_cord = (j,i)
    print(largest_cord, largest_v)