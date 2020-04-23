Name:           antlr3
Epoch:          1
Version:        3.5.2
Release:        21
Summary:        ANother Tool for Language Recognition
License:        BSD
URL:            http://www.antlr3.org/
Source0:        https://github.com/antlr/antlr3/archive/%{version}.tar.gz
Source1:        http://www.antlr3.org/download/antlr-javascript-runtime-3.1.zip

Patch0001:      0001-java8-fix.patch

BuildRequires:  maven-local mvn(org.antlr:antlr) mvn(org.antlr:antlr3-maven-plugin) mvn(org.antlr:ST4)
BuildRequires:  mvn(org.antlr:stringtemplate) mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api) mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api) mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin) autoconf automake libtool

Obsoletes:      antlr3-gunit < 3.2-15

%description
ANother Tool for Language Recognition, is a language tool that provides
a framework for constructing recognizers, interpreters, compilers, and
translators from grammatical descriptions containing actions in a variety
of target languages.

%package        tool
Summary:        ANother Tool for Language Recognition
BuildArch:      noarch
Provides:       %{name} = %{epoch}:%{version}-%{release}  ant-%{name} = %{epoch}:%{version}-%{release}
Obsoletes:      %{name} < %{epoch}:%{version}-%{release}  ant-%{name} < %{epoch}:%{version}-%{release}
Requires:       %{name}-java = %{epoch}:%{version}-%{release}

%description tool
ANother Tool for Language Recognition, is a language tool that provides
a framework for constructing recognizers, interpreters, compilers, and
translators from grammatical descriptions containing actions in a variety
of target languages.

%package        java
Summary:        Java run-time support for ANTLR-generated parsers
Provides:       %{name}-java = %{epoch}:%{version}-%{release}
BuildArch:      noarch

%description    java
Java run-time support for ANTLR-generated parsers

%package        java-help
Summary:        API documentation for antlr3
BuildArch:      noarch
Provides:       %{name}-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-javadoc < %{epoch}:%{version}-%{release}

%description java-help
The antlr3-java-help package contains API documentation for antlr3.

%package        javascript
Version:        3.1
Release:        3.5.2.21
Summary:        Javascript run-time support for ANTLR-generated parsers
BuildArch:      noarch

%description    javascript
Javascript run-time support for ANTLR-generated parsers

%package        C
Version:        3.4
Release:        3.5.2.21
Summary:        C run-time support for ANTLR-generated parsers

%description    C
C run-time support for ANTLR-generated parsers

%package        C-devel
Version:        3.4
Release:        3.5.2.21
Summary:        Header files for the C bindings for ANTLR-generated parsers
Requires:       %{name}-C = %{epoch}:3.4-3.5.2.21

%description    C-devel
Header files for the C bindings for ANTLR-generated parsers

%package        C-help
Version:        3.4
Release:        3.5.2.21
Summary:        API documentation for the C run-time support for ANTLR-generated parsers
BuildArch:      noarch
BuildRequires:  graphviz doxygen
Requires:       %{name}-C = %{epoch}:3.4-3.5.2.21

Provides:       %{name}-C-docs = %{epoch}:3.4-3.5.2.21
Obsoletes:      %{name}-C-docs < %{epoch}:3.4-3.5.2.21

%description    C-help
This package contains doxygen documentation with instruction on how to
use the C target in ANTLR and complete API description of the C run-time
support for ANTLR-generated parsers.

%package C++-devel
Summary:        C++ runtime support for ANTLR-generated parsers

%description C++-devel
C++ runtime support for ANTLR-generated parsers.

%prep
%setup -q -n antlr3-3.5.2 -a 1
sed -i "s,\${buildNumber},`cat %{_sysconfdir}/openEuler-release` `date`," \
    tool/src/main/resources/org/antlr/antlr.properties
%patch0001 -p1

find -type f -a -name *.jar -exec rm -f {} ';'
find -type f -a -name *.class -exec rm -f {} ';'

%pom_disable_module antlr3-maven-archetype
%pom_disable_module gunit
%pom_disable_module gunit-maven-plugin
%pom_disable_module antlr-complete

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

sed -i 's/jsr14/1.6/' \
    antlr3-maven-archetype/src/main/resources/archetype-resources/pom.xml \
    antlr3-maven-plugin/pom.xml gunit/pom.xml gunit-maven-plugin/pom.xml \
    pom.xml runtime/Java/pom.xml tool/pom.xml

%pom_xpath_remove pom:resource/pom:filtering

%mvn_package :antlr-runtime java
%mvn_package : tool

%mvn_file :antlr antlr3
%mvn_file :antlr-runtime antlr3-runtime
%mvn_file :antlr-maven-plugin antlr3-maven-plugin


%build
%mvn_build -f

cd runtime/C
autoreconf -i
%configure --disable-abiflags --enable-debuginfo --enable-64bit
sed -i "s#CFLAGS = .*#CFLAGS = $RPM_OPT_FLAGS#" Makefile
%make_build
doxygen -u
doxygen
cd -

cd antlr-ant/main/antlr3-task/
export CLASSPATH=$(build-classpath ant)
javac -encoding ISO-8859-1 antlr3-src/org/apache/tools/ant/antlr/ANTLR3.java
jar cvf ant-antlr3.jar -C antlr3-src org/apache/tools/ant/antlr/antlib.xml \
    -C antlr3-src org/apache/tools/ant/antlr/ANTLR3.class
cd -

%install
install -d $RPM_BUILD_ROOT/%{_mandir}
install -d $RPM_BUILD_ROOT/%{_datadir}/antlr
%mvn_install
install -m 644 antlr-ant/main/antlr3-task/ant-antlr3.jar \
        -D $RPM_BUILD_ROOT%{_javadir}/ant/ant-antlr3.jar
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ant/ant-antlr3 antlr3" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-antlr3

%jpackage_script org.antlr.Tool '' '' 'stringtemplate4/ST4.jar:antlr3.jar:antlr3-runtime.jar' antlr3 true

DIR1=$(pwd)
cd runtime/C
%make_install
DIR2=$(pwd)
cd api/man/man3
for file in `ls -1 * | grep -vi "^antlr3"`; do mv $file antlr3-$file; done
sed -i -e 's,^\.so man3/pANTLR3,.so man3/antlr3-pANTLR3,' `grep -rl 'man3/pANTLR3' .`
gzip *
cd ${DIR2}
mv api/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rm -rf api/man
cd ${DIR1}

cd antlr-javascript-runtime-3.1
install -pm 644 *.js $RPM_BUILD_ROOT%{_datadir}/antlr/
cd -

install -d $RPM_BUILD_ROOT/%{_includedir}/%{name}
install -pm 644 runtime/Cpp/include/* $RPM_BUILD_ROOT/%{_includedir}/


%files tool -f .mfiles-tool
%doc README.txt tool/{LICENSE.txt,CHANGES.txt}
%{_bindir}/antlr3
%{_javadir}/ant/ant-antlr3.jar
%config(noreplace) %{_sysconfdir}/ant.d/ant-antlr3

%files C
%doc tool/LICENSE.txt
%exclude %{_libdir}/libantlr3c.{a,la}
%{_libdir}/libantlr3c.so

%files C-devel
%{_includedir}/*.h

%files C-help
%{_mandir}/man3/*
%doc runtime/C/api

%files C++-devel
%doc tool/LICENSE.txt
%{_includedir}/*.{hpp,inl}

%files java -f .mfiles-java
%doc tool/LICENSE.txt

%files javascript
%doc tool/LICENSE.txt
%{_datadir}/antlr/

%files java-help -f .mfiles-javadoc


%changelog
* Sat Dec 21 2019 sunguoshuai<sunguoshuai@huawei.com> - 1:3.5.2-21
- Use version and release macro.

* Sat Dec 21 2019 zoushuangshuang<zoushuangshuang@huawei.com> - 1:3.5.2-20
- Package init
