import pprint

def log(file_name="default.log", msg="Default text"):
    """
    Logs the specified message to specified file.
    Overwrites the whole file each time
    """
    f = open(file_name, "w+")
    pretty = pprint.pformat(msg)
    f.write(pretty)
    f.close()

def perm_log(file_name="default.log", title="Default title", msg="Default text"):
    """
    Logs the specified message to specified file.
    Appends to the file each time
    """
    f = open(file_name, "a")
    f.write(3*"\n"+str(title)+"\n"+80*"-"+"\n")
    f.write(msg)
    f.close()

