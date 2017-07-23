import re
import yaml
import pprint


def parse_file(f_name):
    config = open(str(f_name), 'r').read()
    return yaml.load(config)

def parse(yaml_str):
    """
    Generates a python data structure from yaml_str
    yaml_str has to be valid YAML markup.
    """
    return yaml.load(yaml_str)

def pre_process(f_name):
    """
    Generates YAML markup from the data in the config file
    """
    processed = ""
    countable = True

    for line in open(f_name, 'r'):
        first_line = True

        for char in line:
            if countable:
                if char == ' ':
                    processed += char
                if char != ' ':
                    if countable:
                        processed += "- - " + char
                    else:
                        processed += char
                    countable = False
                if char == '\n':
                    countable = True
            else:
                processed += char
        countable = True

    # for line in processed:
        # if first_line:
        #     # line.replace("- - Menu", "- Menu")
        #     processed.replace(processed[0], "- Menu")
        #     # first_line = False

    # processed = re.sub("- - Menu", "- Menu", processed)
    processed = "- Menu\n" + processed

    return processed


if __name__ == "__main__":
    # pprint.pprint(parse_file("menu.config"))
    # Actual use
    # print pre_process("menu.config")
    # print 80*"-"
    # print parse_file("menu.config")

    # Test case
    processed = pre_process("test.config")
    parsed = parse(processed)

    print processed
    print 80*"-"
    print parsed
    print 80*"-"
    pprint.pprint(parsed)


