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
    TE_FILE_2 = 9, "_te"
    UNDEFINED = 20, ""
    TE_FILE_3 = 9, "te_"

    # GENFS_CONTEXTS = 10, "genfs_contexts"

    def __str__(self):
        return str(self.value)

    def __init__(self, rank, label):
        self.rank = rank
        self.label = label


@dataclass
class Permissive(JSONWizard):
    name: str = ""
    where_is_it: str = ""


class TypeAlias(JSONWizard):
    name: str = ""
    alias: str = ""
    where_is_it: str = ""


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
    where_is_it: str = ""

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + self.rule
            + "\n source: "
            + self.source
            + "\n target: "
            + self.target
            + "\n class_type: "
            + self.class_type
            + "\n\t permissions: "
            + "\n ".join(self.permissions)
        )


# user:role:type:sensitivity[:categories]
@dataclass
class SecurityContext(JSONWizard):
    user: str = ""
    role: str = ""
    type: str = ""
    level: str = ""
    categories: str = ""
    where_is_it: str = ""

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + " user: "
            + self.user
            + "\n role: "
            + self.role
            + "\n type: "
            + self.type
            + "\n level: "
            + self.level
            + "\n categories: "
            + self.categories
        )


@dataclass
class TypeDef(JSONWizard):
    name: str = ""
    alises: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)
    where_is_it: str = ""

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + self.name
            + ": "
            + "\n\t types: ".join(self.types)
            + "\n\t alises: ".join(self.alises)
        )


@dataclass
class Attribute(JSONWizard):
    name: str = ""
    attributes: List[str] = field(default_factory=list)
    where_is_it: str = ""

    def to_string(self):
        return ( "where_is_it: "
                 + self.where_is_it
                 + "\n\n"
                 + self.name + ": "
                 + "\n\t attributes: ".join(self.attributes) )


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
    where_is_it: str = ""

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + "name: "
            + self.name
            + "\n user: "
            + self.user
            + "\n seinfo: "
            + self.seinfo
            + "\n is_system_server: "
            + str(self.is_system_server)
            + "\n is_ephemeral_app: "
            + str(self.is_ephemeral_app)
            + "\n is_priv_app: "
            + str(self.is_priv_app)
            + "\n min_target_sdk_version: "
            + str(self.min_target_sdk_version)
            + "\n from_run_as: "
            + str(self.from_run_as)
            + "\n domain: "
            + self.domain
            + "\n type: "
            + self.type
            + "\n level_from: "
            + self.level_from
            + "\n is_permissive: "
            + str(self.is_permissive)
            + "\n \n\ttype_def: \t"
            + str(self.type_def.to_string()).replace("\n", "\n\t")
            + "\n \n\tattribute: \t"
            + str(self.attribute.to_string()).replace("\n", "\n\t")
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
    where_is_it: str = ""

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + self.path_name
            + "\n file_type: "
            + self.file_type
            + "\n domain_name: "
            + self.domain_name
            + "\n security_conetext: \t"
            + str(self.security_context.to_string()).replace("\n", "\n\t")
            + "\n\t type_def: \t"
            + str(self.type_def.to_string()).replace("\n", "\n\t")
        )


@dataclass
class PolicyMacro:
    name: str = ""
    where_is_it: str = ""
    rules_string: List[str] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)

    def to_string(self):
        return (
            "where_is_it: "
            + self.where_is_it
            + "\n\n"
            + self.name
            + "\n rules_string: \n\t\t"
            + "\n\t\t ".join(self.rules_string)
        )


@dataclass
class PolicyMacroCall:
    name: str = ""
    params: List[str] = field(default_factory=list)
    where_is_it: str = ""


@dataclass
class PolicyFile(JSONWizard):
    where_is_it: str = ""
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
