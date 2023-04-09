from dataclasses import dataclass, field
from enum import Enum
from typing import List
from dataclass_wizard import JSONWizard


DOMAIN_EXECUTABLE = "_exec"


class InheritanceEnum(Enum):
    EXTENDED = 1
    IMPLEMENTED = 2
    DEPENDED = 3


@dataclass
class Inheritance(JSONWizard):
    name: str
    relationship: InheritanceEnum


@dataclass
class UmlRelationMap(JSONWizard):
    name: str = ""
    relationship: InheritanceEnum = InheritanceEnum.DEPENDED


class FileTypeEnum(Enum):
    TE_FILE = 1, ".te"
    FILE_CONTEXTS = 2, "file_contexts"
    SEAPP_CONTEXTS = 3, "seapp_contexts"
    SERVICE_CONTEXTS = 4, "service_contexts"
    HWSERVICE_CONTEXTS = 5, "hwservice_contexts"
    VNDSERVICE_CONTEXTS = 6, "vndservice_contexts"
    PROPERTY_CONTEXTS = 7, "property_contexts"
    # OTHER_CONTEXT = 8,"contexts"
    UNDEFINED = 9, ""

    # GENFS_CONTEXTS = 10, "genfs_contexts"

    def __str__(self):
        return str(self.value)

    def __init__(self, rank, label):
        self.rank = rank
        self.label = label


@dataclass
class Controls(JSONWizard):
    className: str
    permissions: List[str] = field(default_factory=list)


class RuleEnum(Enum):
    ALLOW = 0, "allow"
    NEVER_ALLOW = 1, "neverallow"

    def __str__(self):
        return str(self.value)

    def __init__(self, rank, label):
        self.rank = rank
        self.label = label

# allow source target:class permissions


@dataclass
class Rule(JSONWizard):
    rule: str = ""
    source: str = ""
    target: str = ""
    classType: str = ""
    permissions: List[str] = field(default_factory=list)

# user:role:type:sensitivity[:categories]


@dataclass
class SecurityContext(JSONWizard):
    user: str = ""
    role: str = ""
    type: str = ""
    level: str = ""
    categories: str = ""


@dataclass
class TypeDef(JSONWizard):
    name: str = ""
    types: List[str] = field(default_factory=list)


@dataclass
class Attribute(JSONWizard):
    name: str = ""
    attributes: List[str] = field(default_factory=list)


@dataclass
class SeAppContext(JSONWizard):
    neverAllow: bool = False
    isSystemServer: bool = False
    isEphemeralApp: bool = False
    user: str = ""
    seinfo: str = ""
    name: str = ""
    isPrivApp: bool = False
    minTargetSdkVersion: int = 0
    fromRunAs: bool = False
    domain: str = ""
    type: str = ""
    levelFrom: str = ""
    levelFrom: str = ""
    typeDef: TypeDef = TypeDef()
    attribute: Attribute = Attribute()

# pathname_regexp [file_type] security_context


@dataclass
class Context(JSONWizard):
    pathName: str = ""
    fileType: str = ""
    securityContext: SecurityContext = None
    typeDef: TypeDef = TypeDef()
    domainName: str = ""


@dataclass
class PolicyMacro:
    name: str = ""
    rulesString: List[str] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)


@dataclass
class PolicyMacroCall:
    name: str = ""
    params: List[str] = field(default_factory=list)


@dataclass
class PolicyFiles(JSONWizard):
    fileName: str = ""
    description: str = ""
    fileType: FileTypeEnum = FileTypeEnum.UNDEFINED
    typeDef: List[TypeDef] = field(default_factory=list)
    attribute: List[Attribute] = field(default_factory=list)
    contexts: List[Context] = field(default_factory=list)
    seApps: List[SeAppContext] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    macros: List[PolicyMacro] = field(default_factory=list)
    macroCalls: List[PolicyMacroCall] = field(default_factory=list)


@dataclass
class DrawerClass(JSONWizard):
    participants: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
