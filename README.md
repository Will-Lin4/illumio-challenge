# Illumio Coding Challenge

## Testing
I tried to come up with two tests. First test I tried out was the edge case test. I tried to test possible edge cases, like seeing if a rule is allowed if it stands on the border of some range, changing up the direction, etc. The second test I tried to do was a stress test. I quickly wrote a function that generated random rules. I generated ~500k random rules in one instance and the program ran fairly quickly. Other than those two tests, I did not have a sufficient amount of time to test for more edge cases and other more thorough tests. If I had more time, I would have done so.

## Code Choice
I decided to use a BST to store the rules. Each node of this BST is also linked to another BST. (a mix of a linked list and a BST) For every possible range interval, like port range and range for each part of the ip address, there was a link. It went from port range -> ip[0] range -> ip[1] range -> ip[2] range -> ip[3] range. For ranges, each node of the BST had the value of the lower end of a range. When checking if a value is in range, both lower and upper end of the range are compared, inclusively. The code terminates immediately if it finds a rule to prevent further searching. The reason I chose to use a BST instead of some normal list was for the superior runtime O(logn) for searching.

I implemented the traversal of the BSTs with iterative methods. Using recursion would have made the code a lot cleaner and easier to read. However, there is a risk of the rule set getting too big (~500k nodes can be quite large in depth), so the recursion limit would have been exceeded, leading to a crash.

## More Optimizations
There were a number of optimizations and refinements that weren't implemented because of time constraints. A possible optimization would have been to use some type of self-balancing BST rather than a normal BST. In the case that some adversary or by unlucky ordering inserts rules in a particular order (like strictly increasing order), the BST would no longer be balanced, making the runtime O(n) for searches. Using something like an LLRB would mitigate this risk. Another refinement that would be to have the option of knowing what rules were passed. Implementing this in the program shouldn't be too difficult if it were to be added on later. This would make testing rules significantly easier.

## Note to Reviewer
There are comments throughout the code explaining the process. If you have any questions about what I did, I will be happy to explain further.

## Team Interest
Platform Team