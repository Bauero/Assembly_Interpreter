###     REGISTER ERRORS

class RegisterNotImplemented (Exception):
    pass
class RegisterTooSmallToMove (Exception):
    pass
class RegisterSizeTooSmall (Exception):
    pass
class OperationNotPossible (Exception):
    pass
class RegisterCantEffectiveAddress (Exception):
    pass


###     NUMBER ERROR

class WrongNumberBase (Exception):
    pass

class NumberTooBig (Exception):
    pass

###     OTHER ERRORS

class OperandSizeNotSpecified (Exception):
    pass

class EffectiveAddressError (Exception):
    pass

class EffectiveAddresNotExist (Exception):
    pass

