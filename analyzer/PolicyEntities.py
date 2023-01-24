from dataclasses import dataclass
from enum import Enum

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

