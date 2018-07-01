# trick because you can't import modules with dashes in their name.

tmp = __import__('analyze-deps')
globals().update(vars(tmp))