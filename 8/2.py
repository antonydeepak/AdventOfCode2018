def metadata(tree):
    children,meta_count = head(tree),head(tree)

    meta_children = []
    for _ in range(children):
        meta_children.append(metadata(tree))

    meta = []
    for _ in range(meta_count):
        meta.append(head(tree))
    
    value = 0
    if children>0:
        for i in meta:
            if i>0 and i<=len(meta_children):
                value += meta_children[i-1]
    else:
        value = sum(meta)
    
    return value

def head(tree):
    return next(tree)

if __name__ == '__main__': #file_name = "test.in"
    # file_name = "test.in"
    file_name = "1.in"
    line = open(file_name, 'r').readline().rstrip()
    tree = map(int, line.split())
    print(metadata(tree))