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
class Permissive(JSONWizard):
    name: str = ""


class TypeAlias(JSONWizard):
    name: str = ""
    alias: str = ""


@dataclass
class Controls(JSONWizard):
    class_name: str
    permissions: List[str] = field(default_factory=list)


class RuleEnum(Enum):
    ALLOW = "allow"
    NEVER_ALLOW = "neverallow"
    DONT_AUDIT = "dontaudit"
    AUDIT_ALLOW = "auditallow"
    AUDIT_DENY = "auditdeny"

    def __str__(self):
        return str(self.value)


class NotSupportedRuleEnum(Enum):
    ALLOWXPERM = "allowxperm"
    EXPANDATTRIBUTE = "expandattribute"
    EXPANDTYPEATTRIBUTE = "expandtypeattribute"


# allow source target:class permissions
@dataclass
class Rule(JSONWizard):
    rule: str = ""
    source: str = ""
    target: str = ""
    class_type: str = ""
    permissions: List[str] = field(default_factory=list)

    def to_string(self):
        return (
            self.rule
            + " source: "
            + self.source
            + " target: "
            + self.target
            + " class_type: "
            + self.class_type
            + "\n\t permissions: "
            + " ".join(self.permissions)
        )


# user:role:type:sensitivity[:categories]
@dataclass
class SecurityContext(JSONWizard):
    user: str = ""
    role: str = ""
    type: str = ""
    level: str = ""
    categories: str = ""

    def to_string(self):
        return (
            "user: "
            + self.user
            + " role: "
            + self.role
            + " type: "
            + self.type
            + " level: "
            + self.level
            + " categories: "
            + self.categories
        )


@dataclass
class TypeDef(JSONWizard):
    name: str = ""
    alises: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)

    def to_string(self):
        return (
            self.name
            + ": "
            + "\n\t types: ".join(self.types)
            + "\n\t alises: ".join(self.alises)
        )


@dataclass
class Attribute(JSONWizard):
    name: str = ""
    attributes: List[str] = field(default_factory=list)

    def to_string(self):
        return self.name + ": " + "\n\t attributes: ".join(self.attributes)


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
    type_def: TypeDef = field(default_factory=TypeDef)
    attribute: Attribute = field(default_factory=Attribute)
    is_permissive: bool = False

    def to_string(self):
        return (
            "name: "
            + self.name
            + " user: "
            + self.user
            + " seinfo: "
            + self.seinfo
            + " is_system_server: "
            + str(self.is_system_server)
            + " is_ephemeral_app: "
            + str(self.is_ephemeral_app)
            + " is_priv_app: "
            + str(self.is_priv_app)
            + " min_target_sdk_version: "
            + str(self.min_target_sdk_version)
            + " from_run_as: "
            + str(self.from_run_as)
            + " domain: "
            + self.domain
            + " type: "
            + self.type
            + " level_from: "
            + self.level_from
            + " is_permissive: "
            + str(self.is_permissive)
            + " \n\ttype_def: "
            + str(self.type_def.to_string())
            + " \n\tattribute: "
            + str(self.attribute.to_string())
        )


# pathname_regexp [file_type] security_context
@dataclass
class Context(JSONWizard):
    path_name: str = ""
    file_type: str = ""
    security_context: SecurityContext = None
    type_def: TypeDef = field(default_factory=TypeDef)
    domain_name: str = ""
    is_permissive: bool = False

    def to_string(self):
        return (
            self.path_name
            + " file_type: "
            + self.file_type
            + " domain_name:"
            + self.domain_name
            + " security_conetext: "
            + str(self.security_context.to_string())
            + "\n\t type_def:"
            + str(self.type_def.to_string())
        )


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
    permissives: List[Permissive] = field(default_factory=list)
    type_aliases: List[TypeAlias] = field(default_factory=list)


@dataclass
class DrawerClass(JSONWizard):
    participants: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
