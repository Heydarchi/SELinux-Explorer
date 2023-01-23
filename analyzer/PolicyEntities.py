from dataclasses import dataclass

class FileTypeEnum(Enum):
    UNDEFINED = 0
    OTHER_CONTEXT = 1
    TE_FILE = 2
    FILE_CONTEXTS = 3
    SEAPP_CONTEXTS = 4
    SERVICE_CONTEXTS = 5
    HWSERVICE_CONTEXTS = 6
    VNDSERVICE_CONTEXTS = 7
    PROPERTY_CONTEXTS = 8

    def __str__(self):
        return str(self.value)
        
@dataclass
class PolicyFiles:
    fileName: str
    description: str
    
@dataclass
class Controls:
    className: str
    permissions: list()

#allow source target:class permissions
@dataclass
class Rule:
    source: str
    target: str
    clas: str
    permissions: list()

#user:role:type:sensitivity[:categories]
@dataclass
class SecurityContext:
    user: str
    role: str
    type: str
    level: str
    categories: str


#pathname_regexp [file_type] security_context
@dataclass
class Context:
    pathName: str
    fileType: str
    securityContext: SecurityContext

