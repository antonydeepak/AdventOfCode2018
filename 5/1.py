def does_react(a, b):
    return (ord(a) + 32 == ord(b)) or (ord(a) - 32 == ord(b))

if __name__ == '__main__':
    input_path = "1.in"
    line = open(input_path, 'r').readline().rstrip('\n')
    stack = []
    for c in line:
        if len(stack)>0 and does_react(stack[-1], c):
            stack.pop()
        else:
            stack.append(c)
    print(len(stack))