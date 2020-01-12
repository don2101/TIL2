from abc import ABCMeta, abstractmethod


# 팩터리 메서드를 통해 생성될 클래스들의 추상 클래스(Product 역할)
# 각 섹션에 대한 추상클래스
class Section(metaclass=ABCMeta):
    @abstractmethod
    def describe(self):
        pass


class PersonalSection(Section):
    def describe(self):
        print("Personal Section")


class AlbumSection(Section):
    def describe(self):
        print("Album Section")


class PatentSection(Section):
    def describe(self):
        print("Patent Section")


class PublicationSection(Section):
    def describe(self):
        print("Publication Section")


# 클래스를 생성하는 추상 클래스(Creator 역할)
class Profile(metaclass=ABCMeta):
    def __init__(self):
        self.sections = []
        self.create_profile()
    
    @abstractmethod
    def create_profile(self):
        pass
    
    def get_sections(self):
        return self.sections
    
    def add_sections(self, section):
        self.sections.append(section)


class LinkedIn(Profile):
    def create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(PatentSection())
        self.add_sections(PublicationSection())
        

class FaceBook(Profile):
    def create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(AlbumSection)


if __name__ == '__main__':
    linkedin_profile = LinkedIn()
    print('Profile: ', type(linkedin_profile).__name__)
    print('Sections of profile: ', linkedin_profile.get_sections())

    facebook_profile = FaceBook()
    print('Profile: ', type(facebook_profile).__name__)
    print('Sections of profile: ', facebook_profile.get_sections())

