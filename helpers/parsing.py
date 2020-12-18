def tokenize_parenthesized_expression(string):
    '''Yields tokens from a parenthesized expression, treating each parenthesized
    piece as one token. Supports recursive parenthesization.
    Example: tokenize_parenthesized_expression('a + (b * c) + d') would yield
    'a'
    '+'
    '(b * c)'
    '+'
    'd'
    '''
    paren_count = 0
    current = ''
    for idx, part in enumerate(string.split()):
        if part[0] == '(':
            paren_count += part.count('(')
            current += f' {part}'
            continue
        if part[-1] == ')':
            current += f' {part}'
            paren_count -= part.count(')')
            if paren_count == 0:
                yield current.strip()
                current = ''
            continue
        if paren_count > 0:
            current += f' {part}'
            continue
        yield part
    assert(paren_count == 0)
