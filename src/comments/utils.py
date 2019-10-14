import uuid


def uuid_generator():
    a = uuid.uuid4()
    web = 'id'
    return "{}{}".format(web, a)
