from dataclasses import dataclass, field
from enum import Enum
from typing import List

class FileTypeEnum(Enum):
    TE_FILE = 1,".te"
    FILE_CONTEXTS = 2,"file_contexts"
    SEAPP_CONTEXTS = 3,"seapp_contexts"
    SERVICE_CONTEXTS = 4,"service_contexts"
    HWSERVICE_CONTEXTS = 5,"hwservice_contexts"
    VNDSERVICE_CONTEXTS = 6,"vndservice_contexts"
    PROPERTY_CONTEXTS = 7,"property_contexts"
    OTHER_CONTEXT = 8,"contexts"
    UNDEFINED = 9,""

    def __str__(self):
        return str(self.value)
    
    def __init__(self, rank, label):
        self.rank = rank
        self.label = label

@dataclass
class PolicyFunction:
    name: str
    params: list()
    rules: list()

@dataclass
class Controls:
    className: str
    permissions: list()


class RuleEnum(Enum):
    ALLOW = 0, "allow"
    NEVER_ALLOW = 1, "neverallow"

    def __str__(self):
        return str(self.value)
    
    def __init__(self, rank, label):
        self.rank = rank
        self.label = label

#allow source target:class permissions
@dataclass
class Rule:
    rule: str = ""
    source: str = ""
    target: str = ""
    classType: str = ""
    permissions: List[str] = field(default_factory=list)

#user:role:type:sensitivity[:categories]
@dataclass
class SecurityContext:
    user: str = ""
    role: str = ""
    type: str = ""
    level: str = ""
    categories: str = ""

@dataclass
class SeAppContext:
    neverAllow: bool = False
    isSystemServer: bool = False
    isEphemeralApp:  bool = False
    user:  str = ""
    seinfo:  str = ""
    name:  str = ""
    isPrivApp:  bool = False
    minTargetSdkVersion:  int = 0
    fromRunAs:  bool = False
    domain: str = ""
    type: str = ""
    levelFrom: str = ""
    levelFrom: str = ""


#pathname_regexp [file_type] security_context
@dataclass
class Context:
    pathName: str = ""
    fileType: str = ""
    securityContext: SecurityContext = None
@dataclass
class TypeDef:
    name: str = ""
    types: List[str] = field(default_factory=list)

@dataclass
class PolicyFiles:
    fileName: str = ""
    description: str = ""
    fileType: FileTypeEnum = FileTypeEnum.UNDEFINED
    typeDef: List[TypeDef]= field(default_factory=list)
    contexts: List[Context]= field(default_factory=list)
    seApps: List[SeAppContext]= field(default_factory=list)
    rules: List[Rule]= field(default_factory=list)
    functions: List[PolicyFunction]= field(default_factory=list)