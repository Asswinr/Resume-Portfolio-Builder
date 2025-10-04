from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PersonalInfo:
    name: str = ""
    role: str = ""
    introduction: str = ""

@dataclass
class Skill:
    name: str = ""

@dataclass
class AboutMe:
    biography: str = ""
    skills: List[Skill] = field(default_factory=list)

@dataclass
class Experience:
    company: str = ""
    role: str = ""
    years: str = ""
    description: str = ""

@dataclass
class Education:
    degree: str = ""
    institution: str = ""
    years: str = ""

@dataclass
class Project:
    title: str = ""
    description: str = ""
    link: Optional[str] = None

@dataclass
class Contact:
    email: str = ""
    phone: str = ""
    linkedin: Optional[str] = None
    github: Optional[str] = None
    twitter: Optional[str] = None

@dataclass
class PortfolioData:
    personal_info: PersonalInfo = field(default_factory=PersonalInfo)
    about_me: AboutMe = field(default_factory=AboutMe)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    contact: Contact = field(default_factory=Contact)