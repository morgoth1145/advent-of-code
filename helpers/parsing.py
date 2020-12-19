def get_parenthesized_expression_parse_tree(expression, operators='+-*/'):
    '''Returns a simple parse tree from a parenthesized expression, grouping
    each parenthesized piece into a sublist. Supports recursive parenthesizetion.
    Example: tokenize_parenthesized_expression('a + (b * c) + d') would return
    ['a', '+', ['b', '*', 'c'], '+', 'd']
    '''
    stack = [[]]
    last_idx = 0
    for idx, c in enumerate(expression):
        if c == '(':
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            stack.append([])
            last_idx = idx+1
        elif c == ')':
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            subtree = stack.pop()
            stack[-1].append(subtree)
            last_idx = idx+1
        elif c in operators:
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            stack[-1].append(c)
            last_idx = idx+1
        elif c.isspace():
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            last_idx = idx+1
    if last_idx != len(expression):
        stack[-1].append(expression[last_idx:])
    assert(len(stack) == 1)
    return stack[0]

def eval_parenthesized_expression(expression, list_merger, operators='+-*/'):
    '''Returns a fully evaluated parenthesized expression, given a list merger
    function to handle each level of parenthesization. Supports recursive
    parentesization.
    Example: eval_parenthesized_expression('a + (b * c) + d', merger) would
    be equivalent to the following:
    temp = merger(['b', '*', 'c'])
    merger(['a', '+', temp, '+', 'd'])
    '''
    stack = [[]]
    last_idx = 0
    for idx, c in enumerate(expression):
        if c == '(':
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            stack.append([])
            last_idx = idx+1
        elif c == ')':
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            subtree = stack.pop()
            stack[-1].append(list_merger(subtree))
            last_idx = idx+1
        elif c in operators:
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            stack[-1].append(c)
            last_idx = idx+1
        elif c.isspace():
            if last_idx != idx:
                stack[-1].append(expression[last_idx:idx])
            last_idx = idx+1
    if last_idx != len(expression):
        stack[-1].append(expression[last_idx:])
    assert(len(stack) == 1)
    return list_merger(stack[0])
