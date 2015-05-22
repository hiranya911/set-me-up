import os
import shutil

class JavaDependency:
    def __init__(self, groupId, artifactId, version, scope='compile'):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.scope = scope

    def write(self, indent = ''):
        template = """{4}<dependency>
  {4}<groupId>{0}</groupId>
  {4}<artifactId>{1}</artifactId>
  {4}<version>{2}</version>{3}
{4}</dependency>"""
        scope = ''
        if self.scope != 'compile':
            scope = '\n  {1}<scope>{0}</scope>'.format(self.scope, indent)
            
        return template.format(self.groupId, self.artifactId, self.version, scope, indent)

class JavaProject:
    def __init__(self, name, groupId, artifactId, version = '1.0.0'):
        self.name = name
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.dependencies = [
            JavaDependency('commons-io', 'commons-io', '2.0'),
            JavaDependency('junit', 'junit', '3.8', 'test')
        ]

    def write(self):
        template = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

  <modelVersion>4.0.0</modelVersion>

  <groupId>{0}</groupId>
  <artifactId>{1}</artifactId>
  <version>{2}</version>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.2</version>
        <configuration>
          <source>1.7</source>
          <target>1.7</target>
        </configuration>
      </plugin>
    </plugins>
  </build>

{3}

</project>"""
        deps = '  <dependencies>'
        for d in self.dependencies:
            deps += '\n' + d.write('    ')
        deps += '\n  </dependencies>'
        return template.format(self.groupId, self.artifactId, self.version, deps)

def get_input(prompt, default_val = None):
    while True:
        prompt_str = None
        if default_val:
            prompt_str = '{0} ({1}): '.format(prompt, default_val)
        else:
            prompt_str = '{0}: '.format(prompt)

        output = raw_input(prompt_str)
        if output == '' and default_val:
            output = default_val
            
        if output != '':
            if ' ' in output:
                print 'Whitespaces not allowed'
            else:
                return output
        
    
def init_java_src():
    name = get_input('Project Name')
    groupId = get_input('Maven Group ID')
    artifactId = get_input('Maven Artifact ID', name)
    version = get_input('Version', '1.0.0')

    if os.path.exists(name):
        shutil.rmtree(name)

    p = JavaProject(name, groupId, artifactId, version)        
    os.makedirs(name)
    os.makedirs(os.path.join(name, 'src', 'main', 'java'))
    os.makedirs(os.path.join(name, 'src', 'main', 'resources'))
    os.makedirs(os.path.join(name, 'src', 'test', 'java'))

    f = open(os.path.join(name, 'pom.xml'), 'w')
    f.write(p.write())
    f.close()
    
if __name__ == '__main__':
    init_java_src()
