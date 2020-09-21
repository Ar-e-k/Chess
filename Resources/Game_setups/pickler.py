from pickle import dump

def pic(file, values):
    f=open(file, "wb")
    dump(values, f)
    f.close()
