def trigger_example(do_it):
    if do_it:
        return True, ("First value", "Second value", "Third value", )
    else:
        return False, (None,)
