from dataclasses import dataclass

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

