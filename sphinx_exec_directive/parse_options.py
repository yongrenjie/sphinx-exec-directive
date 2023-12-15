def option_boolean(arg):
    if not arg or not arg.strip():
        # no argument given, assume used as a flag
        return True
    elif arg.strip().lower() in ("no", "0", "false"):
        return False
    elif arg.strip().lower() in ("yes", "1", "true"):
        return True
    else:
        raise ValueError(f"Expected boolean value, but got '{arg}'.")


def option_str(arg):
    return str(arg)


def option_language(arg):
    if arg is None:
        return "python"
    else:
        return arg.lower()
