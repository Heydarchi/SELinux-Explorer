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
    class_name: str
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
    class_type: str = ""
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
    never_allow: bool = False
    is_system_server: bool = False
    is_ephemeral_app: bool = False
    user: str = ""
    seinfo: str = ""
    name: str = ""
    is_priv_app: bool = False
    min_target_sdk_version: int = 0
    from_run_as: bool = False
    domain: str = ""
    type: str = ""
    level_from: str = ""
    level_from: str = ""
    type_def: TypeDef = field(default_factory=TypeDef)
    attribute: Attribute = field(default_factory=Attribute)

# pathname_regexp [file_type] security_context


@dataclass
class Context(JSONWizard):
    path_name: str = ""
    file_type: str = ""
    security_context: SecurityContext = None
    type_def: TypeDef = field(default_factory=TypeDef)
    domain_name: str = ""


@dataclass
class PolicyMacro:
    name: str = ""
    rules_string: List[str] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)


@dataclass
class PolicyMacroCall:
    name: str = ""
    params: List[str] = field(default_factory=list)


@dataclass
class PolicyFile(JSONWizard):
    file_name: str = ""
    description: str = ""
    file_type: FileTypeEnum = FileTypeEnum.UNDEFINED
    type_def: List[TypeDef] = field(default_factory=list)
    attribute: List[Attribute] = field(default_factory=list)
    contexts: List[Context] = field(default_factory=list)
    se_apps: List[SeAppContext] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    macros: List[PolicyMacro] = field(default_factory=list)
    macro_calls: List[PolicyMacroCall] = field(default_factory=list)


@dataclass
class DrawerClass(JSONWizard):
    participants: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
