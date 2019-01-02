if __name__ == '__main__':
    until = 990941
    recipes = [3, 7]
    e1 = 0
    e2 = 1
    n = len(recipes)
    while n<(until+10):
        # sum
        total = recipes[e1] + recipes[e2]

        # break down and append
        first,second = total//10,total%10
        if first>0:
            recipes.append(first)
        recipes.append(second)

        # move
        n = len(recipes)
        e1 = (e1+recipes[e1]+1)%n
        e2 = (e2+recipes[e2]+1)%n
    print(recipes[(len(recipes)-10):])