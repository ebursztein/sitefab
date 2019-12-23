def get_linter_errors_list(results):
    "Return the list of errors returned by the linter"
    lst = []
    for res in results.info:
        lst.append(res[0])
        print(res)
    return lst
