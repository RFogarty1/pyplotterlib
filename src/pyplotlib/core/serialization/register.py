
from . import registration_funct as regFunctHelp

_SERIALIZATION_REGISTER = dict()

registerForSerialization = regFunctHelp.RegisterClassDecorator(_SERIALIZATION_REGISTER)


