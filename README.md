# analyze-deps: An alternative Maven dependency analyzer.

A Python3 script to analyze Maven dependency upgrade opportunities.

It is an alternative to [maven-dependency-plugin](https://maven.apache.org/plugins/maven-dependency-plugin/) and [versions-maven-plugin](http://www.mojohaus.org/versions-maven-plugin/) (and maybe others) that are written in Java.

## Running it

First `cd` to your clone/checkout (where the room pom.xml is) and then:
### Script dependencies
The script uses [natsort](https://pypi.org/project/natsort/)([docs](https://natsort.readthedocs.io/en/master/)) and [requests](https://pypi.org/project/requests/)([docs](http://docs.python-requests.org/en/master/))

```
$ python3 <(curl -s https://raw.githubusercontent.com/paul-hammant/analyze-deps/master/analyze-deps.py)
```
That works on Mac and Linux. It probably will not work on the Linux-Subsystem-For-Windows (can someone let me know?). 

History: I just wanted to see how far I could get in shell script alone without resorting to Java (like the existing plugins for this). Or Python which might would only have 3x the lines of code, but could get past some semantic versioning / dewey decimal issues (see glitch #4 below). Turns out only so far, and this has now been ported to Python3 by Ilia Mikhnevich.

## The results from running the script

After running the script, peer inside the `.deps/` folder and look at the generated files:

* dependencies-tree.txt		
* flattened-unique-gavs.txt
* immediate-upgrade-opportunities.txt
* mvn-dep-tree-output.txt

They can all be checked in if you want. If you do so, you get to watch a moving target (using Git diff or show) each time you run the analyze-deps script. Meaning, you were in step with other projects releases yesterday, but today you are not.

I think the `immediate-upgrade-opportunities.txt` and `dependencies-tree.txt` files are the most useful ones. At least ones that you'd use to guide you 
towards which dependency to upgrade first (or harass other dev teams).

With `dependencies-tree.txt` you get to see transitive dependencies too. You would not upgrade those yourself but that level of detail does give you clues that that
an 'upstream' team should attend to their upgrades (assuming you are on the latest of their releases).

## Glitches

1. If the dependency tree has two versions of the same group:artifact and there is some independence in the complete DAG between those two branches, then the item can be listed twice and/or marked for upgrade when none is necessary. You can see that with `log4j` (jar) which is marked as `1.2.12` in one branch and `1.2.17` in another. Anyway, the confusion means that right at the top, version `1.2.17` is marked as  eligible to upgrade to version `1.2.17` - doh!. Your eyeballs will scan past that quickly as a red herring.

2. Related a group:artifact may be in the larger graph twice. Once as 'jar' and once as something else, causing an erroneous marking for upgrade.

3. Qualifiers are not well catered for. See `org.apache.avro:avro-mapred:jar:hadoop2:1.7.7:compile` above (hadoop2 being the qualifier).

4. Where a team releases (say) `4.1.3` and then back-ports the fix of a bug to (say) `3.9.5` the latter might have a more recent timestamp and be deemed more recent than the former - causing an erroneous upgrade suggestion.

5. The script is only checking the 'maven central' repository. So Gradle's at https://repo.gradle.org/gradle/libs-releases-local/ is not checked

## Examples of output for the excellent Hazelcast [github.com/hazelcast/hazelcast-jet-demos](https://github.com/hazelcast/hazelcast-jet-demos)

Lines that end in `> N.n.n` are a suggested version upgrade (notwithstanding the glitches mentioned above)

Note: the Hazelcast dev team [speedily consumed upgrade suggestions](https://github.com/hazelcast/hazelcast-jet-demos/commit/289f64a606c00f55dbd26366edf5a7a07648f950) :)

### The dependency-tree.txt file

```
--- demos ---
com.hazelcast.jet.demos:demos:pom:0.1-SNAPSHOT
--- cryptocurrency-realtime-trend ---
com.hazelcast.jet.demos:cryptocurrency-realtime-trend:jar:0.1-SNAPSHOT
 com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT:compile  > 0.5.1
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 edu.stanford.nlp:stanford-corenlp:jar:3.8.0:compile  > 3.8.0
  com.apple:AppleJavaExtensions:jar:1.4:compile
  de.jollyday:jollyday:jar:0.4.9:compile  > 0.5.3
   javax.xml.bind:jaxb-api:jar:2.2.7:compile  > 2.3.0
  org.apache.commons:commons-lang3:jar:3.3.1:compile  > 3.7
  org.apache.lucene:lucene-queryparser:jar:4.10.3:compile  > 7.2.1
   org.apache.lucene:lucene-sandbox:jar:4.10.3:compile  > 7.2.1
  org.apache.lucene:lucene-analyzers-common:jar:4.10.3:compile  > 7.2.1
  org.apache.lucene:lucene-queries:jar:4.10.3:compile  > 7.2.1
  org.apache.lucene:lucene-core:jar:4.10.3:compile  > 7.2.1
  javax.servlet:javax.servlet-api:jar:3.0.1:compile  > 4.0.0
  com.io7m.xom:xom:jar:1.2.10:compile
   xml-apis:xml-apis:jar:1.3.03:compile  > 1.4.01
   xerces:xercesImpl:jar:2.8.0:compile  > 2.11.0
   xalan:xalan:jar:2.7.0:compile  > 2.7.2
  joda-time:joda-time:jar:2.9.4:compile  > 2.9.9
  com.googlecode.efficient-java-matrix-library:ejml:jar:0.23:compile  > 0.25
  org.glassfish:javax.json:jar:1.0.4:compile  > 1.1.2
  org.slf4j:slf4j-api:jar:1.7.12:compile  > 1.7.25
  com.google.protobuf:protobuf-java:jar:3.2.0:compile  > 3.5.1
 edu.stanford.nlp:stanford-corenlp:jar:models:3.8.0:compile  > 3.8.0
 edu.stanford.nlp:stanford-corenlp:jar:models-english:3.8.0:compile  > 3.8.0
 net.dean.jraw:JRAW:jar:1.0.0:compile  > 
  org.jetbrains.kotlin:kotlin-stdlib:jar:1.2.10:compile  > 1.2.21
   org.jetbrains:annotations:jar:13.0:compile  > 15.0
  com.squareup.okhttp3:okhttp:jar:3.9.1:compile
   com.squareup.okio:okio:jar:1.13.0:compile
  net.dean.jraw:moshi-deeply-nested:jar:1.0.0:compile  > 
 com.twitter:hbc-twitter4j:jar:2.2.0:compile
  com.twitter:hbc-core:jar:2.2.0:compile
   org.apache.httpcomponents:httpclient:jar:4.2.5:compile  > 4.5.5
    org.apache.httpcomponents:httpcore:jar:4.2.4:compile  > 4.4.9
    commons-logging:commons-logging:jar:1.1.1:compile  > 1.2
    commons-codec:commons-codec:jar:1.6:compile  > 1.11
   com.twitter:joauth:jar:6.0.2:compile
   com.google.code.findbugs:jsr305:jar:1.3.9:compile  > 3.0.2
  com.google.guava:guava:jar:14.0.1:compile  > 24.0-jre
  org.twitter4j:twitter4j-core:jar:4.0.1:compile  > 4.0.6
  org.twitter4j:twitter4j-stream:jar:4.0.1:compile  > 4.0.6
 org.json:json:jar:20171018:compile  > 20180130
--- flight-telemetry ---
com.hazelcast.jet.demos:flight-telemetry:jar:0.1-SNAPSHOT
 com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT:compile  > 0.5.1
 org.python:jython:jar:2.7.0:compile  > 2.7.1b3
 log4j:log4j:jar:1.2.12:compile  > 1.2.17
--- realtime-image-recognition ---
com.hazelcast.jet.demos:realtime-image-recognition:jar:1.0-SNAPSHOT
 org.slf4j:slf4j-simple:jar:1.7.21:compile  > 1.7.25
  org.slf4j:slf4j-api:jar:1.7.21:compile  > 1.7.25
 org.boofcv:boofcv-core:jar:0.28:compile
  org.georegression:georegression:jar:0.15:compile
   org.ddogleg:ddogleg:jar:0.13:compile
    org.ejml:ejml-core:jar:0.33:compile
    org.ejml:ejml-fdense:jar:0.33:compile
    org.ejml:ejml-ddense:jar:0.33:compile
    org.ejml:ejml-simple:jar:0.33:compile
     org.ejml:ejml-cdense:jar:0.33:compile
     org.ejml:ejml-zdense:jar:0.33:compile
    org.ejml:ejml-dsparse:jar:0.33:compile
  org.boofcv:boofcv-calibration:jar:0.28:compile
  org.boofcv:boofcv-feature:jar:0.28:compile
  org.boofcv:boofcv-geo:jar:0.28:compile
  org.boofcv:boofcv-io:jar:0.28:compile
   org.yaml:snakeyaml:jar:1.17:compile  > 1.19
  org.boofcv:boofcv-ip:jar:0.28:compile
  org.boofcv:boofcv-learning:jar:0.28:compile
  org.boofcv:boofcv-recognition:jar:0.28:compile
   org.deepboof:main:jar:0.4:compile
   org.deepboof:models:jar:0.4:compile
    org.deepboof:learning:jar:0.4:compile
    org.deepboof:io:jar:0.4:compile
     com.google.protobuf:protobuf-java:jar:2.6.1:compile  > 3.5.1
     org.rauschig:jarchivelib:jar:0.5.0:compile  > 0.7.1
      org.apache.commons:commons-compress:jar:1.7:compile  > 1.15
       org.tukaani:xz:jar:1.4:compile  > 1.8
     net.lingala.zip4j:zip4j:jar:1.3.2:compile
  org.boofcv:boofcv-sfm:jar:0.28:compile
 org.boofcv:boofcv-WebcamCapture:jar:0.28:compile
  org.boofcv:boofcv-swing:jar:0.28:compile
  com.github.sarxos:webcam-capture:jar:0.3.12:compile
   com.nativelibs4java:bridj:jar:0.7.0:compile
 com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT:compile  > 0.5.1
--- jetleopard ---
com.hazelcast.jet.demos:jetleopard:jar:1.0.0-SNAPSHOT
 junit:junit:jar:4.12:test
  org.hamcrest:hamcrest-core:jar:1.3:test
 com:betleopard:jar:1.1.0:compile  > 
  org.apache.spark:spark-core_2.11:jar:2.1.1:compile  > 2.2.1
   org.apache.avro:avro-mapred:jar:hadoop2:1.7.7:compile  > 1.8.2
    org.apache.avro:avro-ipc:jar:1.7.7:compile  > 1.8.2
     org.apache.avro:avro:jar:1.7.7:compile  > 1.8.2
    org.apache.avro:avro-ipc:jar:tests:1.7.7:compile  > 1.8.2
    org.codehaus.jackson:jackson-core-asl:jar:1.9.13:compile  > 1.9.11
    org.codehaus.jackson:jackson-mapper-asl:jar:1.9.13:compile  > 1.9.11
   com.twitter:chill_2.11:jar:0.8.0:compile  > 0.7.7
    com.esotericsoftware:kryo-shaded:jar:3.0.3:compile  > 4.0.1
     com.esotericsoftware:minlog:jar:1.3.0:compile  > 1.3
     org.objenesis:objenesis:jar:2.1:compile  > 2.6
   com.twitter:chill-java:jar:0.8.0:compile  > 0.7.7
   org.apache.xbean:xbean-asm5-shaded:jar:4.4:compile  > 4.5
   org.apache.hadoop:hadoop-client:jar:2.2.0:compile  > 2.7.5
    org.apache.hadoop:hadoop-common:jar:2.2.0:compile  > 2.7.5
     commons-cli:commons-cli:jar:1.2:compile  > 1.4
     org.apache.commons:commons-math:jar:2.1:compile  > 2.2
     xmlenc:xmlenc:jar:0.52:compile  > 0.33
     commons-io:commons-io:jar:2.1:compile  > 2.6
     commons-lang:commons-lang:jar:2.5:compile  > 2.6
     commons-configuration:commons-configuration:jar:1.6:compile  > 1.10
      commons-collections:commons-collections:jar:3.2.1:compile  > 3.2.2
      commons-digester:commons-digester:jar:1.8:compile  > 2.1
       commons-beanutils:commons-beanutils:jar:1.7.0:compile  > 1.9.3
      commons-beanutils:commons-beanutils-core:jar:1.8.0:compile  > 1.8.3
     com.google.protobuf:protobuf-java:jar:2.5.0:compile  > 3.5.1
     org.apache.hadoop:hadoop-auth:jar:2.2.0:compile  > 2.7.5
     org.apache.commons:commons-compress:jar:1.4.1:compile  > 1.15
      org.tukaani:xz:jar:1.0:compile  > 1.8
    org.apache.hadoop:hadoop-hdfs:jar:2.2.0:compile  > 2.7.5
     org.mortbay.jetty:jetty-util:jar:6.1.26:compile
    org.apache.hadoop:hadoop-mapreduce-client-app:jar:2.2.0:compile  > 2.7.5
     org.apache.hadoop:hadoop-mapreduce-client-common:jar:2.2.0:compile  > 2.7.5
      org.apache.hadoop:hadoop-yarn-client:jar:2.2.0:compile  > 2.7.5
       com.google.inject:guice:jar:3.0:compile  > 4.1.0
        javax.inject:javax.inject:jar:1:compile
        aopalliance:aopalliance:jar:1.0:compile
      org.apache.hadoop:hadoop-yarn-server-common:jar:2.2.0:compile  > 2.7.5
     org.apache.hadoop:hadoop-mapreduce-client-shuffle:jar:2.2.0:compile  > 2.7.5
    org.apache.hadoop:hadoop-yarn-api:jar:2.2.0:compile  > 2.7.5
    org.apache.hadoop:hadoop-mapreduce-client-core:jar:2.2.0:compile  > 2.7.5
     org.apache.hadoop:hadoop-yarn-common:jar:2.2.0:compile  > 2.7.5
    org.apache.hadoop:hadoop-mapreduce-client-jobclient:jar:2.2.0:compile  > 2.7.5
    org.apache.hadoop:hadoop-annotations:jar:2.2.0:compile  > 2.7.5
   org.apache.spark:spark-launcher_2.11:jar:2.1.1:compile  > 2.2.1
   org.apache.spark:spark-network-common_2.11:jar:2.1.1:compile  > 2.2.1
    org.fusesource.leveldbjni:leveldbjni-all:jar:1.8:compile
   org.apache.spark:spark-network-shuffle_2.11:jar:2.1.1:compile  > 2.2.1
   org.apache.spark:spark-unsafe_2.11:jar:2.1.1:compile  > 2.2.1
   net.java.dev.jets3t:jets3t:jar:0.7.1:compile  > 0.9.4
    commons-codec:commons-codec:jar:1.3:compile  > 1.11
    commons-httpclient:commons-httpclient:jar:3.1:compile
   org.apache.curator:curator-recipes:jar:2.4.0:compile  > 4.0.0
    org.apache.curator:curator-framework:jar:2.4.0:compile  > 4.0.0
     org.apache.curator:curator-client:jar:2.4.0:compile  > 4.0.0
    org.apache.zookeeper:zookeeper:jar:3.4.5:compile  > 3.4.11
    com.google.guava:guava:jar:14.0.1:compile  > 24.0-jre
   javax.servlet:javax.servlet-api:jar:3.1.0:compile  > 4.0.0
   org.apache.commons:commons-lang3:jar:3.5:compile  > 3.7
   org.apache.commons:commons-math3:jar:3.4.1:compile  > 3.6.1
   com.google.code.findbugs:jsr305:jar:1.3.9:compile  > 3.0.2
   org.slf4j:slf4j-api:jar:1.7.16:compile  > 1.7.25
   org.slf4j:jul-to-slf4j:jar:1.7.16:compile  > 1.7.25
   org.slf4j:jcl-over-slf4j:jar:1.7.16:compile  > 1.7.25
   log4j:log4j:jar:1.2.17:compile  > 1.2.17
   org.slf4j:slf4j-log4j12:jar:1.7.16:compile  > 1.7.25
   com.ning:compress-lzf:jar:1.0.3:compile  > 1.0.4
   org.xerial.snappy:snappy-java:jar:1.1.2.6:compile  > 1.1.7.1
   net.jpountz.lz4:lz4:jar:1.3.0:compile  > 1.3
   org.roaringbitmap:RoaringBitmap:jar:0.5.11:compile  > 0.7.0
   commons-net:commons-net:jar:2.2:compile  > 3.6
   org.json4s:json4s-jackson_2.11:jar:3.2.11:compile  > 3.6.0-M2
    org.json4s:json4s-core_2.11:jar:3.2.11:compile  > 3.6.0-M2
     org.json4s:json4s-ast_2.11:jar:3.2.11:compile  > 3.6.0-M2
     org.scala-lang:scalap:jar:2.11.0:compile  > 2.13.0-M3
      org.scala-lang:scala-compiler:jar:2.11.0:compile  > 2.13.0-M3
       org.scala-lang.modules:scala-xml_2.11:jar:1.0.1:compile  > 1.0.6
       org.scala-lang.modules:scala-parser-combinators_2.11:jar:1.0.1:compile  > 1.1.0
   org.glassfish.jersey.core:jersey-client:jar:2.22.2:compile  > 2.26
    javax.ws.rs:javax.ws.rs-api:jar:2.0.1:compile  > 2.1
    org.glassfish.hk2:hk2-api:jar:2.4.0-b34:compile  > 2.5.0-b61
     org.glassfish.hk2:hk2-utils:jar:2.4.0-b34:compile  > 2.5.0-b61
     org.glassfish.hk2.external:aopalliance-repackaged:jar:2.4.0-b34:compile  > 2.5.0-b61
    org.glassfish.hk2.external:javax.inject:jar:2.4.0-b34:compile  > 2.5.0-b61
    org.glassfish.hk2:hk2-locator:jar:2.4.0-b34:compile  > 2.5.0-b61
     org.javassist:javassist:jar:3.18.1-GA:compile  > 3.22.0-GA
   org.glassfish.jersey.core:jersey-common:jar:2.22.2:compile  > 2.26
    javax.annotation:javax.annotation-api:jar:1.2:compile  > 1.3.1
    org.glassfish.jersey.bundles.repackaged:jersey-guava:jar:2.22.2:compile  > 2.26-b03
    org.glassfish.hk2:osgi-resource-locator:jar:1.0.1:compile  > 2.5.0-b42
   org.glassfish.jersey.core:jersey-server:jar:2.22.2:compile  > 2.26
    org.glassfish.jersey.media:jersey-media-jaxb:jar:2.22.2:compile  > 2.26
    javax.validation:validation-api:jar:1.1.0.Final:compile  > 2.0.1.Final
   org.glassfish.jersey.containers:jersey-container-servlet:jar:2.22.2:compile  > 2.26
   org.glassfish.jersey.containers:jersey-container-servlet-core:jar:2.22.2:compile  > 2.26
   io.netty:netty-all:jar:4.0.42.Final:compile  > 4.0.55.Final
   io.netty:netty:jar:3.8.0.Final:compile  > 3.10.6.Final
   com.clearspring.analytics:stream:jar:2.7.0:compile  > 2.9.6
   io.dropwizard.metrics:metrics-core:jar:3.1.2:compile  > 4.0.2
   io.dropwizard.metrics:metrics-jvm:jar:3.1.2:compile  > 4.0.2
   io.dropwizard.metrics:metrics-json:jar:3.1.2:compile  > 4.0.2
   io.dropwizard.metrics:metrics-graphite:jar:3.1.2:compile  > 4.0.2
   org.apache.ivy:ivy:jar:2.4.0:compile
   oro:oro:jar:2.0.8:compile
   net.razorvine:pyrolite:jar:4.13:compile  > 4.20
   net.sf.py4j:py4j:jar:0.10.4:compile  > 0.10.6
   org.apache.spark:spark-tags_2.11:jar:2.1.1:compile  > 2.2.1
   org.apache.commons:commons-crypto:jar:1.0.0:compile
   org.spark-project.spark:unused:jar:1.0.0:compile
  com.hazelcast:hazelcast-client:jar:3.9:compile  > 3.9.2
  com.hazelcast:hazelcast-spark:jar:0.2:compile
   org.scala-lang:scala-library:jar:2.11.8:compile  > 2.13.0-M3
   javax.cache:cache-api:jar:1.0.0:compile  > 1.1.0
  com.fasterxml.jackson.module:jackson-module-scala_2.11:jar:2.8.8:compile  > 2.8.11
   org.scala-lang:scala-reflect:jar:2.11.8:compile  > 2.13.0-M3
   com.fasterxml.jackson.module:jackson-module-paranamer:jar:2.8.8:compile  > 2.9.4
    com.thoughtworks.paranamer:paranamer:jar:2.8:compile
 com.hazelcast.jet:hazelcast-jet:jar:0.5:compile  > 0.5.1
 com.fasterxml.jackson.core:jackson-core:jar:2.8.8:compile  > 2.9.4
 com.fasterxml.jackson.core:jackson-databind:jar:2.8.8:compile  > 2.9.4
  com.fasterxml.jackson.core:jackson-annotations:jar:2.8.0:compile  > 2.9.4
 com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.8.8:compile  > 2.9.4
--- markov-chain-generator ---
com.hazelcast.jet.demos:markov-chain-generator:jar:0.1-SNAPSHOT
 com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT:compile  > 0.5.1
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 com.google.code.findbugs:annotations:jar:3.0.0:provided  > 3.0.1u2
--- online-training-traffic-predictor ---
com.hazelcast.jet.demos:online-training-traffic-predictor:jar:0.1-SNAPSHOT
 com.hazelcast.jet:hazelcast-jet-core:jar:0.6-SNAPSHOT:compile  > 0.5.1
  com.hazelcast.jet:hazelcast-jet-client-protocol:jar:0.6-SNAPSHOT:compile  > 0.5.1
  com.hazelcast:hazelcast-client:jar:3.9:compile  > 3.9.2
   com.hazelcast:hazelcast:jar:3.9:compile  > 3.9.2

```
### The immediate-upgrade-opportunities.txt file

```
 com.fasterxml.jackson.core:jackson-core:jar:2.8.8:compile  > 2.9.4
 com.fasterxml.jackson.core:jackson-databind:jar:2.8.8:compile  > 2.9.4
 com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.8.8:compile  > 2.9.4
 com.google.code.findbugs:annotations:jar:3.0.0:provided  > 3.0.1u2
 com.hazelcast.jet:hazelcast-jet-core:jar:0.6-SNAPSHOT:compile  > 0.5.1
 com.hazelcast.jet:hazelcast-jet:jar:0.5:compile  > 0.5.1
 com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT:compile  > 0.5.1
 com:betleopard:jar:1.1.0:compile  > 
 edu.stanford.nlp:stanford-corenlp:jar:3.8.0:compile  > 3.8.0
 edu.stanford.nlp:stanford-corenlp:jar:models-english:3.8.0:compile  > 3.8.0
 edu.stanford.nlp:stanford-corenlp:jar:models:3.8.0:compile  > 3.8.0
 log4j:log4j:jar:1.2.12:compile  > 1.2.17
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 net.dean.jraw:JRAW:jar:1.0.0:compile  > 
 org.json:json:jar:20171018:compile  > 20180130
 org.python:jython:jar:2.7.0:compile  > 2.7.1b3
 org.slf4j:slf4j-simple:jar:1.7.21:compile  > 1.7.25
```

These are the pending upgrades that are directly within the control of the HazelCast dev team. All others 
are responsibilities outside this team, and the HazelCast team could raise issues or pull-requests with 
other teams if they felt it was that important.

