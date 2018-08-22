class Attr(object):
    """
    Encapsulates information about an attribute in the JSON encoding of the
    object. It identifies properties of the attribute such as whether it's
    read-only, its type, etc.
    """
    DATE_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, atype=None, rw=True, is_api_list=False):
        self._atype = atype
        self._is_api_list = is_api_list
        self.rw = rw

    def to_json(self, value, preserve_ro):
        """
        Returns the JSON encoding of the given attribute value.

        If the value has a 'to_json_dict' object, that method is called. Otherwise,
        the following values are returned for each input type:
         - datetime.datetime: string with the API representation of a date.
         - dictionary: if 'atype' is ApiConfig, a list of ApiConfig objects.
         - python list: python list (or ApiList) with JSON encoding of items
         - the raw value otherwise
        """
        if hasattr(value, 'to_json_dict'):
            return value.to_json_dict(preserve_ro)
        elif isinstance(value, dict) and self._atype == ApiConfig:
            return config_to_api_list(value)
        elif isinstance(value, datetime.datetime):
            return value.strftime(self.DATE_FMT)
        elif isinstance(value, list) or isinstance(value, tuple):
            if self._is_api_list:
                return ApiList(value).to_json_dict()
            else:
                return [ self.to_json(x, preserve_ro) for x in value ]
        else:
            return value

class ROAttr(Attr):
    """
    Subclass that just defines the attribute as read-only.
    """
    def __init__(self, atype=None, is_api_list=False):
        Attr.__init__(self, atype=atype, rw=False, is_api_list=is_api_list)


class BaseApiObject(object):
    """
    The BaseApiObject helps with (de)serialization from/to JSON.

    The derived class has two ways of defining custom attributes:
     - Overwriting the '_ATTRIBUTES' field with the attribute dictionary
     - Override the _get_attributes() method, in case static initialization of
       the above field is not possible.

    It's recommended that the _get_attributes() implementation do caching to
    avoid computing the dictionary on every invocation.

    The derived class's constructor must call the base class's init() static
    method. All constructor arguments (aside from self and resource_root) must
    be keywords arguments with default values (typically None), or
    from_json_dict() will not work.
    """

    _ATTRIBUTES = { }
    _WHITELIST = ( '_resource_root', '_attributes' )

    @classmethod
    def _get_attributes(cls):
        """
        Returns a map of property names to attr instances (or None for default
        attribute behavior) describing the properties of the object.

        By default, this method will return the class's _ATTRIBUTES field.
        Classes can override this method to do custom initialization of the
        attributes when needed.
        """
        return cls._ATTRIBUTES

    @staticmethod
    def init(obj, resource_root, attrs=None):
        """
        Wraper around the real constructor to avoid issues with the 'self'
        argument. Call like this, from a subclass's constructor:

         - BaseApiObject.init(self, locals())
        """
        # This works around http://bugs.python.org/issue2646
        # We use unicode strings as keys in kwargs.
        str_attrs = { }
        if attrs:
            for k, v in attrs.iteritems():
                if k not in ('self', 'resource_root'):
                    str_attrs[k] = v
        BaseApiObject.__init__(obj, resource_root, **str_attrs)

    def __init__(self, resource_root, **attrs):
        """
        Initializes internal state and sets all known writable properties of the
        object to None. Then initializes the properties given in the provided
        attributes dictionary.

        @param resource_root: API resource object.
        @param attrs: optional dictionary of attributes to set. This should only
                      contain r/w attributes.
        """
        self._resource_root = resource_root

        for name, attr in self._get_attributes().iteritems():
            object.__setattr__(self, name, None)
        if attrs:
            self._set_attrs(attrs, from_json=False)

    def _set_attrs(self, attrs, allow_ro=False, from_json=True):
        """
        Sets all the attributes in the dictionary. Optionally, allows setting
        read-only attributes (e.g. when deserializing from JSON) and skipping
        JSON deserialization of values.
        """
        for k, v in attrs.iteritems():
            attr = self._check_attr(k, allow_ro)
            if attr and from_json:
                v = attr.from_json(self._get_resource_root(), v)
            object.__setattr__(self, k, v)

    def __setattr__(self, name, val):
        if name not in BaseApiObject._WHITELIST:
            self._check_attr(name, False)
        object.__setattr__(self, name, val)

    def _check_attr(self, name, allow_ro):
        if name not in self._get_attributes():
            raise AttributeError('Invalid property %s for class %s.' %
                                 (name, self.__class__.__name__))
        attr = self._get_attributes()[name]
        if not allow_ro and attr and not attr.rw:
            raise AttributeError('Attribute %s of class %s is read only.' %
                                 (name, self.__class__.__name__))
        return attr

    def _get_resource_root(self):
        return self._resource_root

    def _update(self, api_obj):
        """Copy state from api_obj to this object."""
        if not isinstance(self, api_obj.__class__):
            raise ValueError(
                "Class %s does not derive from %s; cannot update attributes." %
                (self.__class__, api_obj.__class__))

        for name in self._get_attributes().keys():
            try:
                val = getattr(api_obj, name)
                setattr(self, name, val)
            except AttributeError, ignored:
                pass

    def to_json_dict(self, preserve_ro=False):
        dic = { }
        for name, attr in self._get_attributes().iteritems():
            if not preserve_ro and attr and not attr.rw:
                continue
            try:
                value = getattr(self, name)
                if value is not None:
                    if attr:
                        dic[name] = attr.to_json(value, preserve_ro)
                    else:
                        dic[name] = value
            except AttributeError:
                pass
        return dic

    def __str__(self):
        """
        Default implementation of __str__. Uses the type name and the first
        attribute retrieved from the attribute map to create the string.
        """
        name = self._get_attributes().keys()[0]
        value = getattr(self, name, None)
        return "<%s>: %s = %s" % (self.__class__.__name__, name, value)

    @classmethod
    def from_json_dict(cls, dic, resource_root):
        obj = cls(resource_root)
        obj._set_attrs(dic, allow_ro=True)
        return obj



class ApiHdfsReplicationResult(BaseApiObject):
    _ATTRIBUTES = {
        'progress'            : ROAttr(),
        'counters'            : ROAttr(),
        'numBytesDryRun'      : ROAttr(),
        'numFilesDryRun'      : ROAttr(),
        'numFilesExpected'    : ROAttr(),
        'numBytesExpected'    : ROAttr(),
        'numFilesCopied'      : ROAttr(),
        'numBytesCopied'      : ROAttr(),
        'numFilesSkipped'     : ROAttr(),
        'numBytesSkipped'     : ROAttr(),
        'numFilesDeleted'     : ROAttr(),
        'numFilesCopyFailed'  : ROAttr(),
        'numBytesCopyFailed'  : ROAttr(),
        'setupError'          : ROAttr(),
        'jobId'               : ROAttr(),
        'jobDetailsUri'       : ROAttr(),
        'dryRun'              : ROAttr(),
        'snapshottedDirs'     : ROAttr(),
        'failedFiles'         : ROAttr(),
        'runAsUser'           : ROAttr(),
        'remainingTime'       : ROAttr(),
    }