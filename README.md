# analyze-deps: An alternative Maven dependency analyzer.

A Python3 script to analyze Maven dependency upgrade opportunities.

It is an alternative to [maven-dependency-plugin](https://maven.apache.org/plugins/maven-dependency-plugin/) and 
[versions-maven-plugin](http://www.mojohaus.org/versions-maven-plugin/) (and maybe others) that are written in Java.

## Script dependencies
The script uses [natsort](https://pypi.org/project/natsort/)([docs](https://natsort.readthedocs.io/en/master/)) and 
[requests](https://pypi.org/project/requests/)([docs](http://docs.python-requests.org/en/master/))

## Running it

First `cd` to your clone/checkout (where the room pom.xml is) and then:

```
$ mvn install -DskipTests
$ python3 <(curl -s https://raw.githubusercontent.com/paul-hammant/analyze-deps/master/analyze-deps.py)
```
That works on Mac and Linux. It probably will not work on the Linux-Subsystem-For-Windows (can someone let me know?). 

History: I just wanted to see how far I could get in shell script alone without resorting to Java (like the existing plugins for this). 
Or Python which might would only have 3x the lines of code, but could get past some semantic versioning / dewey decimal issues (see 
glitch #4 below). Turns out only so far, and this has now been ported to Python3 by Ilia Mikhnevich.

## The results from running the script

After running the script, peer inside the `.deps/` folder and look at the generated files:

* dependencies-tree.txt		
* flattened-unique-gavs.txt
* immediate-upgrade-opportunities.txt
* mvn-dep-tree-output.txt

They can all be checked in if you want (except `mvn-dep-tree-output.txt`). If you do so, you get to watch a moving target (using Git diff or show) each 
time you run the analyze-deps script. Meaning, you were in step with other projects releases yesterday, but today 
you are not.

I think the `immediate-upgrade-opportunities.txt` and `dependencies-tree.txt` files are the most useful ones. At least 
ones that you'd use to guide you 
towards which dependency to upgrade first (or harass other dev teams).

With `dependencies-tree.txt` you get to see transitive dependencies too. You would not upgrade those yourself but that 
level of detail does give you clues that that
an 'upstream' team should attend to their upgrades (assuming you are on the latest of their releases).

## Glitches

1. If the dependency tree has two versions of the same group:artifact and there is some independence in the complete DAG 
between those two branches, then the item can be listed twice and/or marked for upgrade when none is necessary. You can 
see that with `log4j` (jar) which is marked as `1.2.12` in one branch and `1.2.17` in another. Anyway, the confusion means 
that right at the top, version `1.2.17` is marked as  eligible to upgrade to version `1.2.17` - doh!. Your eyeballs will 
scan past that quickly as a red herring.

2. Related a group:artifact may be in the larger graph twice. Once as 'jar' and once as something else, causing an 
erroneous marking for upgrade.

3. Qualifiers are not well catered for. See `org.apache.avro:avro-mapred:jar:hadoop2:1.7.7:compile` above (hadoop2 
being the qualifier).

4. Where a team releases (say) `4.1.3` and then back-ports the fix of a bug to (say) `3.9.5` the latter might have a 
more recent timestamp and be deemed more recent than the former - causing an erroneous upgrade suggestion.

5. The script is only checking the 'maven central' repository. So Gradle's at https://repo.gradle.org/gradle/libs-releases-local/ 
is not checked

## Examples of output for the excellent Hazelcast [github.com/hazelcast/hazelcast-jet-demos](https://github.com/hazelcast/hazelcast-jet-demos) 

Notes: 

1. This is with the repo as of March 30th, 2018, and the report made on July 27th, 2018
2. Lines that end in `> N.n.n` are a suggested version upgrade (notwithstanding the glitches mentioned above)
3. The Hazelcast dev team [speedily consumed upgrade suggestions](https://github.com/hazelcast/hazelcast-jet-demos/commit/289f64a606c00f55dbd26366edf5a7a07648f950) that were made to them while 
this tool was being developed.

### The dependency-tree.txt file

```
com.hazelcast.samples:code-samples:pom:0.1-SNAPSHOT
book.hazelcast.client:clients:pom:0.1-SNAPSHOT
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
book.hazelcast.client.basic:basic:jar:0.1-SNAPSHOT
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
com.hazelcast.samples:helper:jar:0.1-SNAPSHOT
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
com.hazelcast.samples.distributed-map:distributed-map:pom:0.1-SNAPSHOT
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
com.hazelcast.samples.distributed-map:nearcache:jar:0.1-SNAPSHOT
 com.hazelcast.samples:helper:jar:0.1-SNAPSHOT:compile
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
book.hazelcast.client:client-near-cache:jar:0.1-SNAPSHOT
 com.hazelcast.samples.distributed-map:nearcache:jar:0.1-SNAPSHOT:compile
  com.hazelcast.samples:helper:jar:0.1-SNAPSHOT:compile
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
book.hazelcast.client.basic:clients-rest:jar:0.1-SNAPSHOT
 org.glassfish.jersey.core:jersey-client:jar:2.8:compile  > 2.27, 2.22.4
  org.glassfish.jersey.core:jersey-common:jar:2.8:compile  > 2.27, 2.22.4
   javax.annotation:javax.annotation-api:jar:1.2:compile  > 1.3.2
   org.glassfish.jersey.bundles.repackaged:jersey-guava:jar:2.8:compile  > 2.26-b03, 2.22.4
   org.glassfish.hk2:osgi-resource-locator:jar:1.0.1:compile  > 2.5.0-b42, 1.0.2
  javax.ws.rs:javax.ws.rs-api:jar:2.0:compile  > 2.1, 2.0.1
  org.glassfish.hk2:hk2-api:jar:2.2.0:compile  > 2.5.0-b61
   org.glassfish.hk2:hk2-utils:jar:2.2.0:compile  > 2.5.0-b61
   org.glassfish.hk2.external:aopalliance-repackaged:jar:2.2.0:compile  > 2.5.0-b61
  org.glassfish.hk2.external:javax.inject:jar:2.2.0:compile  > 2.5.0-b61
  org.glassfish.hk2:hk2-locator:jar:2.2.0:compile  > 2.5.0-b61
   org.javassist:javassist:jar:3.18.1-GA:compile  > 3.23.1-GA
 com.hazelcast.samples:helper:jar:0.1-SNAPSHOT:compile
 com.hazelcast:hazelcast-all:jar:3.
 [and many more lines]

```

### The immediate-upgrade-opportunities.txt file

Dependencies uses in one or more modules that could be directly upgraded by the Hazelcast team

```
 ch.qos.logback:logback-classic:jar:1.1.11:compile  > 1.3.0-alpha4
 com.amazonaws:aws-java-sdk-ec2:jar:1.10.77:compile  > 1.11.375
 com.atomikos:transactions-jdbc:jar:3.9.3:compile  > 4.0.6
 com.esotericsoftware.kryo:kryo:jar:2.22:compile  > 2.24.0
 com.esotericsoftware:kryo:jar:4.0.0:compile  > kryo, 4.0.2
 com.fasterxml.jackson.core:jackson-annotations:jar:2.6.6:compile  > 2.9.6, 2.6.7
 com.fasterxml.jackson.core:jackson-databind:jar:2.6.6:compile  > 2.9.6, 2.6.7.1
 com.google.protobuf:protobuf-java:jar:2.6.1:compile  > 3.6.0, 2.6.1
 com.hazelcast.jet:hazelcast-jet-core:jar:0.5:compile  > 0.6.1, 0.5.1
 com.hazelcast:hazelcast-all:jar:3.10-SNAPSHOT:compile  > 3.10.3
 com.hazelcast:hazelcast-all:jar:3.9.1:compile  > 3.10.3
 com.hazelcast:hazelcast-all:jar:3.9:compile  > 3.10.3
 com.hazelcast:hazelcast-client:jar:3.10-SNAPSHOT:compile  > 3.10.3
 com.hazelcast:hazelcast-client:jar:3.7.7:compile  > 3.10.3
 com.hazelcast:hazelcast-client:jar:3.9.3:compile  > 3.10.3
 com.hazelcast:hazelcast-hibernate3:jar:3.6.4:compile  > 3.8.2, 3.6.8
 com.hazelcast:hazelcast-hibernate4:jar:3.6.4:compile  > 3.8.2, 3.6.8
 com.hazelcast:hazelcast-jca-rar:rar:3.6.4:compile  > 3.7.1, 3.6.8
 com.hazelcast:hazelcast-jca:jar:3.6.4:provided  > 3.7.1, 3.6.8
 com.hazelcast:hazelcast-jclouds:jar:3.7:compile  > 3.7.2
 com.hazelcast:hazelcast-kubernetes:jar:1.0.0:compile  > 1.1.0
 com.hazelcast:hazelcast-spark:jar:0.3-SNAPSHOT:compile  > 0.2
 com.hazelcast:hazelcast-spring:jar:3.9.3:compile  > 3.9.4, 3.10.3
 com.hazelcast:hazelcast:jar:3.10-SNAPSHOT:compile  > 3.10.3
 com.hazelcast:hazelcast:jar:3.10-SNAPSHOT:provided  > 3.10.3
 com.hazelcast:hazelcast:jar:3.7.5:compile  > 3.10.3
 com.hazelcast:hazelcast:jar:3.7.7:compile  > 3.10.3
 com.hazelcast:hazelcast:jar:3.9.1:compile  > 3.10.3
 com.hazelcast:hazelcast:jar:3.9.3:compile  > 3.10.3
 com.hazelcast:hazelcast:jar:3.9:compile  > 3.10.3
 com.hazelcast:spring-data-hazelcast:jar:1.0:compile  > 2.0, 1.2.1
 com.ibm.websphere.appserver.api:com.ibm.websphere.appserver.api.basics:jar:1.2.9:provided  > 1.3.21, 1.2.20
 com.solacesystems:sol-common:jar:10.0.0:compile  > 10.4.0, 10.0.2
 com.solacesystems:sol-jcsmp:jar:10.0.0:compile  > 10.4.0, 10.0.2
 commons-lang:commons-lang:jar:2.6:compile  > 2.6
 commons-logging:commons-logging:jar:1.1.3:compile  > 1.2
 javax.cache:cache-api:jar:1.0.0:compile  > 1.1.0
 javax.cache:cache-api:jar:1.1.0:compile  > 1.1.0
 javax.servlet.jsp:jsp-api:jar:2.1:provided  > 2.2.1-b03, 2.1.3-b06
 javax.servlet:javax.servlet-api:jar:3.0.1:provided  > 4.0.1, 3.1.0
 javax.servlet:servlet-api:jar:2.5:provided  > 3.0-alpha-1
 junit:junit:jar:3.8.1:test  > 4.12, 3.8.2
 junit:junit:jar:4.11:test  > 4.12, 3.8.2
 junit:junit:jar:4.12:compile  > 4.12, 3.8.2
 junit:junit:jar:4.7:test  > 4.12, 3.8.2
 log4j:log4j:jar:1.2.12:compile  > 1.2.17
 log4j:log4j:jar:1.2.15:runtime  > 1.2.17
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 net.sf.supercsv:super-csv:jar:2.2.0:compile  > 2.4.0, 2.2.1
 org.apache.commons:commons-lang3:jar:3.0:compile  > 3.7, 3.0.1
 org.apache.derby:derby:jar:10.10.2.0:compile  > 10.14.2.0
 org.apache.felix:org.apache.felix.framework:jar:5.4.0:compile  > 6.0.0, 5.6.10
 org.apache.jclouds.labs:google-compute-engine:jar:1.9.1:compile  > 1.9.3
 org.apache.jclouds:jclouds-allcompute:jar:1.9.1:compile  > 2.1.0, 1.9.3
 org.apache.logging.log4j:log4j-core:jar:2.7:compile  > 2.11.0
 org.apache.logging.log4j:log4j-slf4j-impl:jar:2.7:compile  > 2.11.0
 org.apache.spark:spark-core_2.10:jar:2.1.0:compile  > 2.2.2, 2.1.3
 org.aspectj:aspectjrt:jar:1.6.10:compile  > 1.9.1, 1.6.12
 org.glassfish.jersey.core:jersey-client:jar:2.8:compile  > 2.27, 2.22.4
 org.hdrhistogram:HdrHistogram:jar:1.2.1:compile  > 2.1.10
 org.hibernate.javax.persistence:hibernate-jpa-2.0-api:jar:1.0.0.Final:compile  > 1.0.1.Final
 org.hibernate:hibernate-core:jar:3.5.4-Final:compile  > 5.3.3.Final, 3.6.10.Final, 3.5.6-Final
 org.hibernate:hibernate-core:jar:4.3.7.Final:compile  > 5.3.3.Final, 3.6.10.Final, 3.5.6-Final
 org.hibernate:hibernate-core:jar:4.3.8.Final:compile  > 5.3.3.Final, 3.6.10.Final, 3.5.6-Final
 org.hibernate:hibernate-entitymanager:jar:3.6.9.Final:compile  > 5.3.3.Final, 3.6.10.Final
 org.hsqldb:hsqldb:jar:2.2.9:compile  > 2.4.1
 org.hsqldb:hsqldb:jar:2.3.3:compile  > 2.4.1
 org.hsqldb:hsqldb:jar:2.3.3:test  > 2.4.1
 org.jsr107.ri:cache-ri-impl:jar:1.0.0:compile  > 1.1.0
 org.mongodb:mongo-java-driver:jar:2.7.3:provided  > 3.8.0, 2.14.3
 org.mongodb:mongo-java-driver:jar:3.0.4:compile  > 3.8.0, 2.14.3
 org.ops4j.pax.tinybundles:tinybundles:jar:2.1.1:compile  > 3.0.0
 org.osgi:org.osgi.core:jar:6.0.0:compile  > 6.0.0, 4.3.1
 org.projectlombok:lombok:jar:1.16.10:compile  > 1.18.2, 1.16.22
 org.projectlombok:lombok:jar:1.16.14:compile  > 1.18.2, 1.16.22
 org.projectlombok:lombok:jar:1.16.18:compile  > 1.18.2, 1.16.22
 org.slf4j:jcl-over-slf4j:jar:1.6.6:runtime  > 1.8.0-beta2
 org.slf4j:slf4j-api:jar:1.6.1:compile  > 1.8.0-beta2, 1.5.11
 org.slf4j:slf4j-api:jar:1.6.6:compile  > 1.8.0-beta2, 1.5.11
 org.slf4j:slf4j-api:jar:1.7.25:compile  > 1.8.0-beta2, 1.5.11
 org.slf4j:slf4j-log4j12:jar:1.6.6:compile  > 1.8.0-beta2
 org.slf4j:slf4j-log4j12:jar:1.6.6:runtime  > 1.8.0-beta2
 org.slf4j:slf4j-log4j12:jar:1.7.21:compile  > 1.8.0-beta2
 org.slf4j:slf4j-log4j12:jar:1.7.5:compile  > 1.8.0-beta2
 org.slf4j:slf4j-log4j12:jar:1.7.7:compile  > 1.8.0-beta2
 org.springframework.boot:spring-boot-devtools:jar:1.5.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE
 org.springframework.boot:spring-boot-starter-actuator:jar:1.3.1.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-actuator:jar:1.5.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-cache:jar:1.3.1.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-cache:jar:1.5.9.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-data-jpa:jar:1.4.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-logging:jar:1.4.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-test:jar:1.4.2.RELEASE:test  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-test:jar:1.5.2.RELEASE:test  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-test:jar:1.5.9.RELEASE:test  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-thymeleaf:jar:1.4.0.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-thymeleaf:jar:1.5.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.4.7.RELEASE
 org.springframework.boot:spring-boot-starter-web:jar:1.3.1.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-web:jar:1.4.0.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-web:jar:1.4.3.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter-web:jar:1.5.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.4.0.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.4.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.5.2.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.5.7.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.5.8.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.boot:spring-boot-starter:jar:1.5.9.RELEASE:compile  > 2.0.3.RELEASE, 1.5.14.RELEASE, 1.3.8.RELEASE
 org.springframework.cloud:spring-cloud-netflix-eureka-server:jar:1.2.5.RELEASE:compile  > 2.0.0.RELEASE, 1.4.5.RELEASE, 1.2.7.RELEASE
 org.springframework.cloud:spring-cloud-starter-eureka:jar:1.2.5.RELEASE:compile  > 1.4.5.RELEASE, 1.2.7.RELEASE
 org.springframework.cloud:spring-cloud-starter:jar:1.1.7.RELEASE:compile  > 2.0.0.RELEASE, 1.3.4.RELEASE, 1.1.9.RELEASE
 org.springframework.data:spring-data-mongodb:jar:1.0.1.RELEASE:provided  > 2.0.8.RELEASE, 1.10.13.RELEASE, 1.0.4.RELEASE
 org.springframework.security:spring-security-config:jar:3.2.3.RELEASE:compile  > 5.0.7.RELEASE, 3.2.10.RELEASE
 org.springframework.security:spring-security-web:jar:3.2.3.RELEASE:compile  > 5.0.7.RELEASE, 3.2.10.RELEASE
 org.springframework:spring-context-support:jar:4.2.3.RELEASE:compile  > 5.0.8.RELEASE, 4.3.18.RELEASE, 4.2.9.RELEASE
 org.springframework:spring-context:jar:3.2.8.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-context:jar:4.0.6.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-context:jar:4.1.5.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-context:jar:4.2.3.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-context:jar:4.2.6.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-context:jar:4.3.1.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-core:jar:3.2.8.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-core:jar:4.0.6.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-core:jar:4.2.3.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-core:jar:4.2.6.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-core:jar:4.3.1.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-orm:jar:4.0.6.RELEASE:compile  > 5.0.8.RELEASE, 4.3.18.RELEASE, 4.0.9.RELEASE
 org.springframework:spring-tx:jar:4.0.6.RELEASE:compile  > 5.0.8.RELEASE, 4.3.18.RELEASE, 4.0.9.RELEASE
 org.springframework:spring-tx:jar:4.3.1.RELEASE:compile  > 5.0.8.RELEASE, 4.3.18.RELEASE, 4.0.9.RELEASE
 org.springframework:spring-web:jar:3.2.8.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-webmvc:jar:3.2.8.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-webmvc:jar:4.2.6.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
 org.springframework:spring-webmvc:jar:4.3.7.RELEASE:compile  > 5.0.8.RELEASE, 3.2.18.RELEASE
```

