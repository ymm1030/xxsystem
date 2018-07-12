def logout(*logs):
    try:
        print(logs)
    except UnicodeError:
        print('A log can not output because of unicode error.')