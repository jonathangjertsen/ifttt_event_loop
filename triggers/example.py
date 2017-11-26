def trigger_example(**args):
    if "do_it" in args and args["do_it"]:
        return True, ("First value", "Second value", "Third value", )
    else:
        return False, (None,)
