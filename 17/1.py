# this seems tricky.
'''
After thinking for a long time, I think the best way is to do a DFS approach exploring the flow of water.
Atleast the major states of the system should be captured - clay, sand & moving water. Not sure if we need
to seaprate the notion of both moving water and still water because a) the answer does not differentiate b)
it is hard to get it right because you have to go back and forth multiple times. 
On further thought we have to separate this notion, because we can only build another water layer on top of
existing one if it is a still water.
We can start from the source and explore every node
Every node has three actions is has to take- go down, go left, go right.
    You can go down only when there is sand
    You can go left only if the left node has clay or still water down
    You can only go right if the right node has a clay or still water down
    When you are bounded on left or right you can mark the side you are bounded.
        This can get cascaded and finally the parent that has both left and right marked can mark that entire span to be bounded. This makes a still water
'''