import re

def email(mail):
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', mail)

    if match:
        print("valid email :::")
    else:
        print("not valid:::")

email('string')
email('strdsdsing@wp.pl')