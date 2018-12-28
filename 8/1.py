def metadata(tree):
    meta = 0
    children,meta_count = head(tree),head(tree)
    for _ in range(children):
        meta += metadata(tree)
    for _ in range(meta_count):
        meta += head(tree)
    return meta

def head(tree):
    return next(tree)

if __name__ == '__main__': #file_name = "test.in"
    # file_name = "test.in"
    file_name = "1.in"
    line = open(file_name, 'r').readline().rstrip()
    tree = map(int, line.split())
    print(metadata(tree))