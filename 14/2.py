if __name__ == '__main__':
    recipes = [3, 7]
    e1 = 0
    e2 = 1
    desired = 990941
    to_be_matched = 100000
    to_be_matched_digits = 6
    # desired = 59414
    # to_be_matched = 10000
    # to_be_matched_digits = 5
    matched = to_be_matched
    
    while True:
        # sum
        total = recipes[e1] + recipes[e2]

        # break down and append
        first,second = total//10,total%10
        if first>0:
            recipes.append(first)
            if (desired//matched)%10 == first:
                matched //= 10
                if matched == 0:
                    break
            else:
                matched = to_be_matched
        recipes.append(second)
        if (desired//matched)%10 == second:
            matched //= 10
            if matched == 0:
                break
        else:
            matched = to_be_matched

        # move
        n = len(recipes)
        e1 = (e1+recipes[e1]+1)%n
        e2 = (e2+recipes[e2]+1)%n
    print(len(recipes)-to_be_matched_digits)