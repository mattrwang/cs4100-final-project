import os

# Returns list of all lines in files in supplied directory
def read_files(d):
    output = []
    if (os.path.exists(d)):
        for _, _, files in os.walk(d):
            for f in files:
                #print("reading", f)
                file = open(os.path.join(d, f), 'r')
                output.extend(file.read().splitlines())
    return output