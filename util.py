from google.cloud import ndb


client = ndb.Client()


class API_KEYS(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()
    @staticmethod
    def get(name):
        with client.context():
            NOT_SET_VALUE = "NOT SET"
            retval = API_KEYS.query(API_KEYS.name == name).get()
            if not retval:
                retval = API_KEYS()
                retval.name = name
                retval.value = NOT_SET_VALUE
                retval.put()
            if retval.value == NOT_SET_VALUE:
                raise Exception(('Setting %s not found in the database. A placeholder ' +
                                 'record has been created. Go to the Developers Console for your app ' +
                                 'in App Engine, look up the API_KEYS record with name=%s and enter ' +
                                 'its value in that record\'s value field.') % (name, name))
            return retval.value
