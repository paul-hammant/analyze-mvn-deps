# analyze-deps: An alternative Maven dependency analyzer.

A Bash script to analyze Maven dependency upgrade opportunities.

It is an alternative to [maven-dependency-plugin](https://maven.apache.org/plugins/maven-dependency-plugin/) and [versions-maven-plugin](http://www.mojohaus.org/versions-maven-plugin/) (and maybe others) that are written in Java.

## Running it

First `cd` to your clone/checkout (where the room pom.xml is) and then:

```
$ bash <(curl -s https://raw.githubusercontent.com/paul-hammant/analyze-deps/master/analyze-deps.sh)
```
That works on Mac and Linux. It probably will not work on the Linux-Subsystem-For-Windows (can someone let me know?). 

Oh and I just wanted to see how far I could get in shell script alone without resorting to Java (like the existing plugins for this). Or Python which might would only have 3x the lines of code, but could get past some semantic versioning / dewey decimal issues (see glitch #4 below).

## The results from running the script

After running the script, peer inside the `.deps/` folder and look at the generated files:

* big-dependency-report.txt
* dependencies-tree.txt		
* flattened-unique-gavs.txt
* immediate-upgrade-opportunities.txt
* mvn-dep-tree-output.txt

They can all be checked in if you want. If you do so, you get to watch a moving target (using Git diff or show) each time you run the analyze-deps script. Meaning, you were in step with other projects releases yesterday, but today you are not.

I think the `immediate-upgrade-opportunities.txt` and `dependencies-tree.txt` files are the most useful ones. At least ones that you'd use to guide you 
towards which dependency to upgrade first (or harass other dev teams).  Other people might take the view that `big-dependency-report.txt` is more useful.

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

### The big-dependency-report.txt file

```


========================================================================
Presently in use: aopalliance:aopalliance  1.0
   - a level 8 dependencies among 1 (possibly transitive) uses
2005-09-20 05:45  1.0 ***

========================================================================
Presently in use: com.apple:AppleJavaExtensions  1.4
   - a level 2 dependencies among 1 (possibly transitive) uses
2010-10-22 13:57  1.4 ***

========================================================================
Presently in use: com.clearspring.analytics:stream  2.7.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-10 19:08  2.9.6
2016-08-01 20:09  2.9.5
2016-07-05 19:30  2.9.4
2016-06-15 17:00  2.9.3
2016-05-03 14:45  2.9.2
2016-02-24 15:44  2.9.1
2015-05-08 18:38  2.9.0
2015-02-10 13:06  2.8.0
2014-05-23 13:41  2.7.0 ***

========================================================================
Presently in use: com.esotericsoftware:kryo-shaded  3.0.3
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-07-23 22:02  4.0.1
2016-07-05 23:27  4.0.0
2015-07-26 21:47  3.0.3 ***

========================================================================
Presently in use: com.esotericsoftware:minlog  1.3.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2013-11-14 21:31  1.3
2013-11-14 20:46  1.3-SNAPHOT
unknown-date unknown:time  minlog
unknown-date unknown:time  1.3.0 ***

========================================================================
Presently in use: com.fasterxml.jackson.core:jackson-annotations  2.8.0
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-24 03:12  2.9.4
2017-12-24 02:10  2.8.11
2017-12-08 23:07  2.9.3
2017-10-14 02:44  2.9.2
2017-09-08 00:47  2.9.1
2017-08-24 04:23  2.8.10
2017-07-30 03:53  2.9.0
2017-06-17 01:15  2.9.0.pr4
2017-06-12 00:37  2.8.9
2017-04-25 05:32  2.9.0.pr3
2017-04-05 03:20  2.8.8
2017-03-22 03:23  2.9.0.pr2
2017-03-02 16:49  2.9.0.pr1
2017-02-21 01:00  2.8.7
2017-02-04 19:17  2.7.9
2017-01-12 04:32  2.8.6
2016-11-14 06:05  2.8.5
2016-10-14 03:46  2.8.4
2016-09-26 14:47  2.7.8
2016-09-18 01:24  2.8.3
2016-08-30 00:36  2.8.2
2016-08-26 21:48  2.7.7
2016-07-23 02:25  2.7.6
2016-07-19 22:54  2.8.1
2016-07-04 05:20  2.8.0 ***

========================================================================
Presently in use: com.fasterxml.jackson.core:jackson-core  2.8.8
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-01-24 03:14  2.9.4
2017-12-24 02:13  2.8.11
2017-12-09 03:00  2.9.3
2017-10-14 03:26  2.9.2
2017-09-08 00:48  2.9.1
2017-08-24 04:24  2.8.10
2017-07-30 04:03  2.9.0
2017-06-17 01:16  2.9.0.pr4
2017-06-12 00:43  2.8.9
2017-04-25 05:37  2.9.0.pr3
2017-04-05 03:23  2.8.8 ***

========================================================================
Presently in use: com.fasterxml.jackson.core:jackson-databind  2.8.8
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-01-24 04:07  2.9.4
2017-12-24 02:21  2.8.11
2017-12-20 03:26  2.7.9.2
2017-12-09 03:05  2.9.3
2017-10-14 03:29  2.9.2
2017-09-08 01:10  2.9.1
2017-08-24 04:28  2.8.10
2017-07-30 04:22  2.9.0
2017-07-11 04:13  2.6.7.1
2017-06-17 01:24  2.9.0.pr4
2017-06-12 00:53  2.8.9
2017-04-25 05:47  2.9.0.pr3
2017-04-19 15:35  2.8.8.1
2017-04-18 05:12  2.7.9.1
2017-04-05 03:29  2.8.8 ***

========================================================================
Presently in use: com.fasterxml.jackson.datatype:jackson-datatype-jdk8  2.8.8
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-01-24 04:39  2.9.4
2017-12-24 02:29  2.8.11
2017-12-09 03:18  2.9.3
2017-10-14 04:11  2.9.2
2017-09-08 01:33  2.9.1
2017-08-24 04:41  2.8.10
2017-07-30 04:50  2.9.0
2017-06-17 01:52  2.9.0.pr4
2017-06-12 05:08  2.8.9
2017-04-25 06:01  2.9.0.pr3
2017-04-05 03:47  2.8.8 ***

========================================================================
Presently in use: com.fasterxml.jackson.module:jackson-module-paranamer  2.8.8
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-24 04:34  2.9.4
2017-12-24 02:27  2.8.11
2017-12-09 03:11  2.9.3
2017-10-14 03:38  2.9.2
2017-09-08 01:30  2.9.1
2017-08-24 04:33  2.8.10
2017-07-30 04:42  2.9.0
2017-06-17 01:48  2.9.0.pr4
2017-06-12 02:59  2.8.9
2017-04-25 05:53  2.9.0.pr3
2017-04-05 03:43  2.8.8 ***

========================================================================
Presently in use: com.fasterxml.jackson.module:jackson-module-scala_2.11  2.8.8
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-28 23:08  2.8.11
2018-01-28 22:57  2.9.4
2017-11-12 21:23  2.9.2
2017-09-11 09:18  2.8.10
2017-09-11 08:56  2.9.1
2017-07-30 17:10  2.9.0
2017-06-12 21:52  2.8.9
2017-04-25 19:46  2.9.0.pr3
2017-04-05 18:50  2.8.8 ***

========================================================================
Presently in use: com.github.sarxos:webcam-capture  0.3.12
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-17 19:22  0.3.12 ***

========================================================================
Presently in use: com.google.code.findbugs:annotations  3.0.0
   - a level 1 dependencies among 1 (possibly transitive) uses
2015-10-09 06:11  3.0.1u2
2015-10-09 06:05  3.0.1u1
2015-10-09 05:46  3.0.1
2014-07-10 11:56  3.0.0 ***

========================================================================
Presently in use: com.google.code.findbugs:jsr305  1.3.9
   - a level 3 dependencies among 2 (possibly transitive) uses
2017-03-31 04:55  3.0.2
2015-10-09 05:06  3.0.1
2014-07-10 11:55  3.0.0
2013-12-31 07:26  2.0.3
2013-10-03 06:33  2.0.2
unknown-date unknown:time  2.0.1
unknown-date unknown:time  2.0.0
unknown-date unknown:time  1.3.9 ***

========================================================================
Presently in use: com.google.guava:guava  14.0.1
   - a level 2 dependencies among 2 (possibly transitive) uses
2018-02-01 20:26  24.0-jre
2018-02-01 20:17  24.0-android
2017-12-21 01:03  23.6-jre
2017-12-21 00:53  23.6-android
2017-11-22 20:33  23.5-jre
2017-11-22 20:22  23.5-android
2017-11-09 17:35  23.4-jre
2017-11-09 17:24  23.4-android
2017-10-26 20:06  23.3-jre
2017-10-26 19:55  23.3-android
2017-10-11 22:54  23.2-jre
2017-10-11 22:43  23.2-android
2017-09-27 20:02  23.1-jre
2017-09-27 19:58  23.1-android
2017-08-04 21:24  23.0
2017-08-04 20:34  23.0-android
2017-07-25 17:12  23.0-rc1-android
2017-05-22 19:02  22.0-android
2017-05-22 18:49  22.0
2017-05-02 21:34  22.0-rc1-android
2017-01-12 19:22  21.0
2016-10-28 20:56  20.0
2015-12-09 20:58  19.0
2014-08-25 18:48  18.0
2014-04-22 20:47  17.0
2014-02-03 22:45  16.0.1
2014-01-17 21:44  16.0
2013-09-06 19:52  15.0
2013-03-14 23:57  14.0.1 ***

========================================================================
Presently in use: com.google.inject:guice  3.0
   - a level 7 dependencies among 1 (possibly transitive) uses
2016-06-17 19:53  4.1.0
2015-04-28 20:33  4.0
2011-03-25 18:19  3.0 ***

========================================================================
Presently in use: com.google.protobuf:protobuf-java  2.5.0
   - a level 2 dependencies among 3 (possibly transitive) uses
2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0
2017-01-19 00:55  3.2.0rc2
2016-09-27 00:07  3.1.0
2016-09-06 23:54  3.0.2
2016-07-28 18:39  3.0.0
2016-07-18 22:54  3.0.0-beta-4
2016-05-18 18:50  3.0.0-beta-3
2016-01-04 23:15  3.0.0-beta-2
2015-08-28 00:08  3.0.0-beta-1
2015-06-30 21:16  3.0.0-alpha-3.1
2015-05-29 22:33  3.0.0-alpha-3
2015-03-04 21:35  3.0.0-alpha-2
2014-10-23 01:10  2.6.1
2014-09-03 23:09  2.6.0
2013-03-08 00:18  2.5.0 ***

========================================================================
Presently in use: com.google.protobuf:protobuf-java  2.6.1
   - a level 5 dependencies among 3 (possibly transitive) uses
2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0
2017-01-19 00:55  3.2.0rc2
2016-09-27 00:07  3.1.0
2016-09-06 23:54  3.0.2
2016-07-28 18:39  3.0.0
2016-07-18 22:54  3.0.0-beta-4
2016-05-18 18:50  3.0.0-beta-3
2016-01-04 23:15  3.0.0-beta-2
2015-08-28 00:08  3.0.0-beta-1
2015-06-30 21:16  3.0.0-alpha-3.1
2015-05-29 22:33  3.0.0-alpha-3
2015-03-04 21:35  3.0.0-alpha-2
2014-10-23 01:10  2.6.1 ***

========================================================================
Presently in use: com.google.protobuf:protobuf-java  3.2.0
   - a level 5 dependencies among 3 (possibly transitive) uses
2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0 ***

========================================================================
Presently in use: com.googlecode.efficient-java-matrix-library:ejml  0.23
   - a level 2 dependencies among 1 (possibly transitive) uses
2014-06-13 04:42  0.25
2013-12-27 02:15  0.24
2013-06-21 16:16  0.23 ***

========================================================================
Presently in use: com.hazelcast.jet.demos:cryptocurrency-realtime-trend  0.1-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:demos  0.1-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:flight-telemetry  0.1-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:jetleopard  1.0.0-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:markov-chain-generator  0.1-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:online-training-traffic-predictor  0.1-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet.demos:realtime-image-recognition  1.0-SNAPSHOT
   - a level 0 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: com.hazelcast.jet:hazelcast-jet-client-protocol  0.6-SNAPSHOT
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-12-06 15:29  0.5.1
2017-11-16 08:36  0.5
2017-06-14 08:29  0.4
2017-03-21 10:24  0.3.1
2017-02-06 14:32  0.3

========================================================================
Presently in use: com.hazelcast.jet:hazelcast-jet-core  0.6-SNAPSHOT
   - a level 1 dependencies among 1 (possibly transitive) uses
2017-12-06 15:29  0.5.1
2017-11-16 08:36  0.5
2017-06-14 08:29  0.4
2017-03-21 10:24  0.3.1
2017-02-06 14:32  0.3

========================================================================
Presently in use: com.hazelcast.jet:hazelcast-jet  0.5
   - a level 1 dependencies among 7 (possibly transitive) uses
2017-12-06 15:29  0.5.1
2017-11-16 08:36  0.5 ***

========================================================================
Presently in use: com.hazelcast.jet:hazelcast-jet  0.6-SNAPSHOT
   - a level 4 dependencies among 7 (possibly transitive) uses
2017-12-06 15:29  0.5.1
2017-11-16 08:36  0.5
2017-06-14 08:29  0.4
2017-03-21 10:24  0.3.1
2017-02-06 14:32  0.3

========================================================================
Presently in use: com.hazelcast:hazelcast-client  3.9
   - a level 2 dependencies among 2 (possibly transitive) uses
2018-01-03 12:15  3.9.2
2018-01-03 10:40  3.8.9
2017-12-04 14:52  3.8.8
2017-11-30 10:35  3.9.1
2017-11-09 09:04  3.8.7
2017-10-23 12:17  3.9 ***

========================================================================
Presently in use: com.hazelcast:hazelcast-spark  0.2
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-03-09 09:26  0.2 ***

========================================================================
Presently in use: com.hazelcast:hazelcast  3.9
   - a level 2 dependencies among 4 (possibly transitive) uses
2018-01-03 12:15  3.9.2
2018-01-03 10:40  3.8.9
2017-12-04 14:52  3.8.8
2017-11-30 10:35  3.9.1
2017-11-09 09:04  3.8.7
2017-10-23 12:17  3.9 ***

========================================================================
Presently in use: com.io7m.xom:xom  1.2.10
   - a level 2 dependencies among 1 (possibly transitive) uses
2013-10-25 16:16  1.2.10 ***

========================================================================
Presently in use: com.nativelibs4java:bridj  0.7.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2015-03-08 16:48  0.7.0 ***

========================================================================
Presently in use: com.ning:compress-lzf  1.0.3
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-03-14 02:49  1.0.4
2014-08-16 04:32  1.0.3 ***

========================================================================
Presently in use: com.squareup.okhttp3:okhttp  3.9.1
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-11-18 19:39  3.9.1 ***

========================================================================
Presently in use: com.squareup.okio:okio  1.13.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-05-12 16:24  1.13.0 ***

========================================================================
Presently in use: com.thoughtworks.paranamer:paranamer  2.8
   - a level 4 dependencies among 1 (possibly transitive) uses
2015-08-26 11:29  2.8 ***

========================================================================
Presently in use: com.twitter:chill-java  0.8.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-02-23 22:57  0.7.7
2017-02-23 19:53  0.8.4
2017-02-23 19:16  0.9.2
2017-01-14 01:13  0.8.3
2017-01-14 00:59  0.7.6
2017-01-09 18:25  0.9.1
2017-01-03 19:42  0.9.0
2016-10-11 01:16  0.8.1
2016-02-11 19:29  0.8.0 ***

========================================================================
Presently in use: com.twitter:chill_2.11  0.8.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-02-23 22:56  0.7.7
2017-02-23 19:53  0.8.4
2017-02-23 19:15  0.9.2
2017-01-14 01:11  0.8.3
2017-01-14 00:58  0.7.6
2017-01-09 19:38  0.8.2
2017-01-09 18:42  0.7.5
2017-01-09 18:23  0.9.1
2017-01-03 19:40  0.9.0
2016-10-11 01:17  0.8.1
2016-02-11 19:30  0.8.0 ***

========================================================================
Presently in use: com.twitter:hbc-core  2.2.0
   - a level 2 dependencies among 1 (possibly transitive) uses
2014-07-02 17:25  2.2.0 ***

========================================================================
Presently in use: com.twitter:hbc-twitter4j  2.2.0
   - a level 1 dependencies among 1 (possibly transitive) uses
2014-07-02 17:29  2.2.0 ***

========================================================================
Presently in use: com.twitter:joauth  6.0.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2014-01-30 23:17  6.0.2 ***

========================================================================
Presently in use: com:betleopard  1.1.0
   - a level 1 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: commons-beanutils:commons-beanutils-core  1.8.0
   - a level 6 dependencies among 1 (possibly transitive) uses
2010-03-24 17:33  1.8.3
2009-11-09 14:15  1.8.2
2009-10-19 22:46  1.8.1
2008-08-31 18:13  1.8.0 ***

========================================================================
Presently in use: commons-beanutils:commons-beanutils  1.7.0
   - a level 9 dependencies among 2 (possibly transitive) uses
2016-09-21 16:21  1.9.3
2014-05-26 19:19  1.9.2
2014-01-06 18:19  1.9.1
2013-12-07 15:31  1.9.0
2010-03-24 17:16  1.8.3
2009-11-09 14:05  1.8.2
2009-10-16 21:20  1.8.1
2008-08-28 16:21  1.8.0
2005-09-20 05:46  1.7.0 ***

========================================================================
Presently in use: commons-cli:commons-cli  1.2
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-03-09 13:02  1.4
2015-06-14 10:06  1.3.1
2015-05-03 14:54  1.3
2009-03-19 20:08  1.2 ***

========================================================================
Presently in use: commons-codec:commons-codec  1.3
   - a level 4 dependencies among 2 (possibly transitive) uses
2017-10-17 14:54  1.11
2014-11-06 14:15  1.10
2013-12-21 03:57  1.9
2013-04-23 20:04  1.8
2012-09-11 12:14  1.7
2011-12-03 02:38  1.6
2011-03-25 01:34  1.5
2009-08-09 21:22  1.4
2005-09-20 05:46  1.3 ***

========================================================================
Presently in use: commons-codec:commons-codec  1.6
   - a level 7 dependencies among 2 (possibly transitive) uses
2017-10-17 14:54  1.11
2014-11-06 14:15  1.10
2013-12-21 03:57  1.9
2013-04-23 20:04  1.8
2012-09-11 12:14  1.7
2011-12-03 02:38  1.6 ***

========================================================================
Presently in use: commons-collections:commons-collections  3.2.1
   - a level 6 dependencies among 1 (possibly transitive) uses
2015-11-12 23:11  3.2.2
2008-04-15 01:09  3.2.1 ***

========================================================================
Presently in use: commons-configuration:commons-configuration  1.6
   - a level 5 dependencies among 1 (possibly transitive) uses
2013-10-24 08:22  1.10
2012-08-16 19:29  1.9
2012-01-27 20:42  1.8
2011-09-04 19:17  1.7
2009-02-04 19:44  1.6 ***

========================================================================
Presently in use: commons-digester:commons-digester  1.8
   - a level 6 dependencies among 1 (possibly transitive) uses
2010-09-24 11:02  2.1
2009-01-03 16:51  2.0
2009-01-03 16:48  1.8.1
2006-12-03 18:33  1.8 ***

========================================================================
Presently in use: commons-httpclient:commons-httpclient  3.1
   - a level 4 dependencies among 1 (possibly transitive) uses
2007-08-21 13:44  3.1 ***

========================================================================
Presently in use: commons-io:commons-io  2.1
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-10-15 10:00  2.6
2016-04-22 14:52  2.5
2012-06-12 22:22  2.4
2012-04-10 15:12  2.3
2012-03-26 15:14  2.2
2011-10-03 21:32  2.1 ***

========================================================================
Presently in use: commons-lang:commons-lang  2.5
   - a level 5 dependencies among 1 (possibly transitive) uses
2011-01-16 22:21  2.6
2010-02-25 01:23  2.5 ***

========================================================================
Presently in use: commons-logging:commons-logging  1.1.1
   - a level 4 dependencies among 1 (possibly transitive) uses
2014-07-05 18:12  1.2
2013-05-16 20:05  1.1.3
2013-03-16 12:54  1.1.2
2007-11-26 20:24  1.1.1 ***

========================================================================
Presently in use: commons-net:commons-net  2.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-02-11 15:18  3.6
2016-05-01 22:37  3.5
2015-11-19 12:33  3.4
2013-06-07 22:52  3.3
2012-11-26 17:26  3.2
2012-02-14 18:42  3.1
2011-06-02 18:35  3.0.1
2011-05-10 13:41  3.0
2010-11-17 00:55  2.2 ***

========================================================================
Presently in use: de.jollyday:jollyday  0.4.9
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-12-13 21:24  0.5.3
2017-01-10 22:40  0.5.2
2015-05-06 21:15  0.4.9 ***

========================================================================
Presently in use: edu.stanford.nlp:stanford-corenlp  3.8.0
   - a level 1 dependencies among 3 (possibly transitive) uses
2017-06-15 05:20  3.8.0 ***

========================================================================
Presently in use: edu.stanford.nlp:stanford-corenlp  models
   - a level 1 dependencies among 3 (possibly transitive) uses
2017-06-15 05:20  3.8.0
2017-01-07 12:27  3.7.0
2016-01-21 09:16  3.6.0
2015-05-04 20:27  3.5.2
2015-02-09 20:02  3.5.1
2014-10-31 20:56  3.5.0
2014-09-04 23:40  3.4.1
2014-07-10 23:26  3.4
2014-01-14 09:19  3.3.1
2013-11-16 00:34  3.3.0
2013-07-09 02:17  3.2.0
2013-04-17 19:09  1.3.5
2012-12-17 20:07  1.3.4
2012-07-20 23:04  1.3.3
2012-06-10 02:31  1.3.2
2012-05-09 21:58  1.3.1
2012-01-11 09:47  1.3.0
2011-09-26 13:10  1.2.0

========================================================================
Presently in use: edu.stanford.nlp:stanford-corenlp  models-english
   - a level 4 dependencies among 3 (possibly transitive) uses
2017-06-15 05:20  3.8.0
2017-01-07 12:27  3.7.0
2016-01-21 09:16  3.6.0
2015-05-04 20:27  3.5.2
2015-02-09 20:02  3.5.1
2014-10-31 20:56  3.5.0
2014-09-04 23:40  3.4.1
2014-07-10 23:26  3.4
2014-01-14 09:19  3.3.1
2013-11-16 00:34  3.3.0
2013-07-09 02:17  3.2.0
2013-04-17 19:09  1.3.5
2012-12-17 20:07  1.3.4
2012-07-20 23:04  1.3.3
2012-06-10 02:31  1.3.2
2012-05-09 21:58  1.3.1
2012-01-11 09:47  1.3.0
2011-09-26 13:10  1.2.0

========================================================================
Presently in use: io.dropwizard.metrics:metrics-core  3.1.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-05 18:52  4.0.2
2018-01-03 17:28  4.0.1
2017-12-24 20:53  3.2.6
2017-12-24 20:37  4.0.0
2017-09-15 08:36  3.2.5
2017-08-03 18:01  3.2.4
2017-06-28 07:54  3.2.3
2017-06-02 17:59  3.1.5
2017-03-20 14:18  3.2.2
2017-03-10 15:41  3.2.1
2017-03-10 13:25  3.1.4
2017-02-24 14:20  3.2.0
2017-02-24 13:57  3.1.3
2015-04-26 03:59  3.1.2 ***

========================================================================
Presently in use: io.dropwizard.metrics:metrics-graphite  3.1.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-05 18:54  4.0.2
2018-01-03 17:30  4.0.1
2017-12-24 20:55  3.2.6
2017-12-24 20:39  4.0.0
2017-09-15 08:38  3.2.5
2017-08-03 18:04  3.2.4
2017-06-28 07:58  3.2.3
2017-06-02 18:01  3.1.5
2017-03-20 14:20  3.2.2
2017-03-10 15:43  3.2.1
2017-03-10 13:27  3.1.4
2017-02-24 14:21  3.2.0
2017-02-24 13:59  3.1.3
2015-04-26 04:00  3.1.2 ***

========================================================================
Presently in use: io.dropwizard.metrics:metrics-json  3.1.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-05 18:56  4.0.2
2018-01-03 17:33  4.0.1
2017-12-24 20:58  3.2.6
2017-12-24 20:41  4.0.0
2017-09-15 08:45  3.2.5
2017-08-03 18:09  3.2.4
2017-06-28 08:05  3.2.3
2017-06-02 18:06  3.1.5
2017-03-20 14:24  3.2.2
2017-03-10 15:47  3.2.1
2017-03-10 13:30  3.1.4
2017-02-24 14:24  3.2.0
2017-02-24 14:01  3.1.3
2015-04-26 04:01  3.1.2 ***

========================================================================
Presently in use: io.dropwizard.metrics:metrics-jvm  3.1.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-05 18:52  4.0.2
2018-01-03 17:29  4.0.1
2017-12-24 20:54  3.2.6
2017-12-24 20:38  4.0.0
2017-09-15 08:36  3.2.5
2017-08-03 18:02  3.2.4
2017-06-28 07:55  3.2.3
2017-06-02 18:00  3.1.5
2017-03-20 14:18  3.2.2
2017-03-10 15:42  3.2.1
2017-03-10 13:26  3.1.4
2017-02-24 14:20  3.2.0
2017-02-24 13:58  3.1.3
2015-04-26 03:59  3.1.2 ***

========================================================================
Presently in use: io.netty:netty-all  4.0.42.Final
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-21 18:38  4.0.55.Final
2018-01-21 15:09  4.1.20.Final
2017-12-15 14:51  4.1.19.Final
2017-12-08 15:42  4.0.54.Final
2017-12-08 12:12  4.1.18.Final
2017-11-09 00:33  4.0.53.Final
2017-11-08 23:30  4.1.17.Final
2017-09-25 07:23  4.1.16.Final
2017-09-21 20:26  4.0.52.Final
2017-08-24 17:09  4.1.15.Final
2017-08-24 13:26  4.0.51.Final
2017-08-02 19:06  4.0.50.Final
2017-08-02 14:44  4.1.14.Final
2017-07-06 12:25  4.1.13.Final
2017-07-06 06:11  4.0.49.Final
2017-06-09 09:55  4.0.48.Final
2017-06-09 06:27  4.1.12.Final
2017-05-11 18:17  4.0.47.Final
2017-05-11 17:47  4.1.11.Final
2017-04-29 13:45  4.0.46.Final
2017-04-29 12:37  4.1.10.Final
2017-03-10 09:27  4.0.45.Final
2017-03-10 07:23  4.1.9.Final
2017-01-30 17:12  4.0.44.Final
2017-01-30 14:55  4.1.8.Final
2017-01-12 13:02  4.0.43.Final
2017-01-12 11:20  4.1.7.Final
2016-10-14 13:05  4.0.42.Final ***

========================================================================
Presently in use: io.netty:netty  3.8.0.Final
   - a level 3 dependencies among 2 (possibly transitive) uses
2016-06-29 12:45  3.10.6.Final
2015-10-13 10:12  3.10.5.Final
2015-07-21 08:02  3.9.9.Final
2015-06-30 13:28  3.10.4.Final
2015-05-08 15:31  3.10.3.Final
2015-05-08 15:11  3.9.8.Final
2015-05-08 08:43  3.10.2.Final
2015-05-08 08:26  3.9.7.Final
2015-03-23 18:54  3.10.1.Final
2014-12-17 05:02  3.10.0.Final
2014-12-17 04:14  3.9.6.Final
2014-10-30 11:34  3.9.5.Final
2014-10-17 05:25  3.8.3.Final
2014-09-12 11:20  3.6.10.Final
2014-08-26 08:19  3.9.4.Final
2014-08-06 18:59  3.9.3.Final
2014-07-30 23:52  3.9.1.1.Final
2014-06-11 09:22  3.9.2.Final
2014-04-30 13:52  3.9.1.Final
2014-04-30 13:33  3.8.2.Final
2014-04-30 13:18  3.7.1.Final
2014-04-30 13:01  3.6.9.Final
2014-03-13 05:27  3.8.1.Final
2014-03-12 09:16  3.6.8.Final
2013-12-22 10:55  3.9.0.Final
2013-12-03 05:48  3.6.7.Final
2013-11-07 09:23  3.8.0.Final ***

========================================================================
Presently in use: javax.annotation:javax.annotation-api  1.2
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-09-13 12:24  1.3.1
2016-09-22 18:50  1.3
2013-04-26 17:38  1.2 ***

========================================================================
Presently in use: javax.cache:cache-api  1.0.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-12-16 17:15  1.1.0
2014-03-28 03:34  1.0.0 ***

========================================================================
Presently in use: javax.inject:javax.inject  1
   - a level 8 dependencies among 1 (possibly transitive) uses
2009-10-13 23:35  1 ***

========================================================================
Presently in use: javax.servlet:javax.servlet-api  3.0.1
   - a level 2 dependencies among 2 (possibly transitive) uses
2017-08-15 17:59  4.0.0
2017-06-02 18:19  4.0.0-b07
2017-05-24 16:02  4.0.0-b06
2017-03-29 23:01  4.0.0-b05
2017-03-16 21:26  4.0.0-b04
2017-03-02 02:40  4.0.0-b03
2017-02-03 23:22  4.0.0-b02
2015-10-09 00:21  4.0.0-b01
2013-04-25 23:52  3.1.0
2013-04-24 05:23  3.1-b09
2013-04-05 18:01  3.1-b08
2013-03-08 06:57  3.1-b07
2013-02-11 21:38  3.1-b06
2013-01-10 18:56  3.1-b05
2012-12-17 23:37  3.1-b04
2012-12-11 16:50  3.1-b03
2012-09-07 21:50  3.1-b02
2012-07-05 20:59  3.1-b01
2011-07-12 19:40  3.0.1 ***

========================================================================
Presently in use: javax.servlet:javax.servlet-api  3.1.0
   - a level 5 dependencies among 2 (possibly transitive) uses
2017-08-15 17:59  4.0.0
2017-06-02 18:19  4.0.0-b07
2017-05-24 16:02  4.0.0-b06
2017-03-29 23:01  4.0.0-b05
2017-03-16 21:26  4.0.0-b04
2017-03-02 02:40  4.0.0-b03
2017-02-03 23:22  4.0.0-b02
2015-10-09 00:21  4.0.0-b01
2013-04-25 23:52  3.1.0 ***

========================================================================
Presently in use: javax.validation:validation-api  1.1.0.Final
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-19 16:23  2.0.1.Final
2017-08-03 14:44  2.0.0.Final
2017-07-11 13:41  2.0.0.CR3
2017-07-05 13:30  2.0.0.CR2
2017-06-21 17:28  2.0.0.CR1
2017-05-17 14:50  2.0.0.Beta2
2017-04-24 12:02  2.0.0.Beta1
2017-03-28 10:46  2.0.0.Alpha2
2017-02-03 09:02  2.0.0.Alpha1
2013-04-10 13:03  1.1.0.Final ***

========================================================================
Presently in use: javax.ws.rs:javax.ws.rs-api  2.0.1
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-08-04 15:16  2.1
2017-06-14 22:20  2.1-m09
2017-06-05 19:32  2.1-m08
2017-04-18 18:45  2.1-m07
2017-04-11 21:17  2.1-m06
2017-02-24 15:32  2.1-m05
2017-02-10 18:22  2.1-m04
2017-01-23 12:53  2.1-m03
2017-01-13 13:55  2.1-m02
2016-09-14 15:03  2.1-m01
2014-08-07 12:08  2.0.1 ***

========================================================================
Presently in use: javax.xml.bind:jaxb-api  2.2.7
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-07-31 11:27  2.3.0
2017-02-01 11:04  2.3.0-b170201.1204
2014-10-20 12:34  2.2.12
2014-10-01 13:48  2.2.12-b141001.1542
2014-01-09 09:54  2.2.12-b140109.1041
2013-09-06 10:11  2.2.11
2013-07-23 16:54  2.2.10
2013-03-21 17:15  2.2.9
2013-03-21 16:27  2.2.8
2012-05-24 09:37  2.2.7 ***

========================================================================
Presently in use: joda-time:joda-time  2.9.4
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-03-23 13:33  2.9.9
2017-03-22 22:15  2.9.8
2016-12-19 22:55  2.9.7
2016-11-10 21:09  2.9.6
2016-11-03 16:36  2.9.5
2016-05-27 09:25  2.9.4 ***

========================================================================
Presently in use: junit:junit  4.12
   - a level 1 dependencies among 1 (possibly transitive) uses
2014-12-04 16:17  4.12 ***

========================================================================
Presently in use: log4j:log4j  1.2.12
   - a level 1 dependencies among 4 (possibly transitive) uses
2012-05-26 09:43  1.2.17
2010-03-31 04:25  1.2.16
2007-08-30 17:41  1.2.15
2006-12-01 06:27  1.2.14
2006-01-03 17:34  1.2.13
2005-09-23 20:01  1.2.12 ***

========================================================================
Presently in use: log4j:log4j  1.2.17
   - a level 4 dependencies among 4 (possibly transitive) uses
2012-05-26 09:43  1.2.17 ***

========================================================================
Presently in use: net.dean.jraw:JRAW  1.0.0
   - a level 1 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: net.dean.jraw:moshi-deeply-nested  1.0.0
   - a level 2 dependencies among 1 (possibly transitive) uses

========================================================================
Presently in use: net.java.dev.jets3t:jets3t  0.7.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2015-08-23 13:44  0.9.4
2015-01-31 21:43  0.9.3
2014-07-22 10:22  0.9.2
2014-06-07 14:29  0.9.1
unknown-date unknown:time  0.9.0
unknown-date unknown:time  0.8.1
unknown-date unknown:time  0.8.0
unknown-date unknown:time  0.7.4
unknown-date unknown:time  0.7.3
unknown-date unknown:time  0.7.2
unknown-date unknown:time  0.7.1 ***

========================================================================
Presently in use: net.jpountz.lz4:lz4  1.3.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2014-11-26 19:24  1.3
2013-08-08 15:34  1.2.0
2013-05-01 16:47  1.1.2
2013-02-12 20:55  1.1.1
2013-02-09 21:53  1.1.0
2013-01-08 00:24  1.0.0
unknown-date unknown:time  1.3.0 ***

========================================================================
Presently in use: net.lingala.zip4j:zip4j  1.3.2
   - a level 5 dependencies among 1 (possibly transitive) uses
2013-12-27 19:23  1.3.2 ***

========================================================================
Presently in use: net.razorvine:pyrolite  4.13
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-07-05 20:04  4.20
2017-03-19 14:18  4.19
2017-02-19 14:56  4.18
2017-02-02 20:33  4.17
2017-01-12 19:57  4.16
2016-12-27 23:31  4.15
2016-10-13 21:26  4.14
2016-09-08 22:46  4.13 ***

========================================================================
Presently in use: net.sf.py4j:py4j  0.10.4
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-07-05 09:05  0.10.6
2017-05-28 11:35  0.10.5
2016-10-16 10:39  0.10.4 ***

========================================================================
Presently in use: org.apache.avro:avro-ipc  1.7.7
   - a level 4 dependencies among 2 (possibly transitive) uses
2017-05-07 18:53  1.8.2
2016-05-17 16:05  1.8.1
2016-01-22 16:19  1.8.0
2014-07-18 20:09  1.7.7 ***

========================================================================
Presently in use: org.apache.avro:avro-ipc  tests
   - a level 7 dependencies among 2 (possibly transitive) uses
2017-05-07 18:53  1.8.2
2016-05-17 16:05  1.8.1
2016-01-22 16:19  1.8.0
2014-07-18 20:09  1.7.7
2014-01-10 21:42  1.7.6
2013-08-08 16:17  1.7.5
2013-02-22 17:59  1.7.4
2012-12-03 18:24  1.7.3
2012-09-18 00:39  1.7.2
2012-07-12 19:31  1.7.1
2012-06-07 22:14  1.7.0
2012-03-02 22:32  1.6.3
2012-02-09 23:44  1.6.2
2011-11-04 21:57  1.6.1
2011-10-28 22:35  1.6.0
2011-09-07 21:53  1.5.4
2011-08-25 22:21  1.5.3
2011-07-28 20:06  1.5.2
2011-04-29 22:52  1.5.1
2011-03-08 18:42  1.5.0

========================================================================
Presently in use: org.apache.avro:avro-mapred  hadoop2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-05-07 18:53  1.8.2
2016-05-17 16:05  1.8.1
2016-01-22 16:21  1.8.0
2014-07-18 20:09  1.7.7
2014-01-10 21:42  1.7.6
2013-08-08 16:18  1.7.5
2013-02-22 18:00  1.7.4
2012-12-03 18:24  1.7.3
2012-09-18 00:39  1.7.2
2012-07-12 19:31  1.7.1
2012-06-07 22:14  1.7.0
2012-03-02 22:32  1.6.3
2012-02-09 23:45  1.6.2
2011-11-04 21:57  1.6.1
2011-10-28 22:35  1.6.0
2011-09-07 21:54  1.5.4
2011-08-25 22:21  1.5.3
2011-07-28 20:06  1.5.2
2011-04-29 22:52  1.5.1
2011-03-08 18:42  1.5.0

========================================================================
Presently in use: org.apache.avro:avro  1.7.7
   - a level 6 dependencies among 4 (possibly transitive) uses
2017-05-07 18:52  1.8.2
2016-05-17 16:03  1.8.1
2016-01-22 16:16  1.8.0
2014-07-18 20:08  1.7.7 ***

========================================================================
Presently in use: org.apache.commons:commons-compress  1.4.1
   - a level 5 dependencies among 2 (possibly transitive) uses
2017-10-14 13:28  1.15
2017-05-11 19:16  1.14
2016-12-25 12:26  1.13
2016-06-18 15:42  1.12
2016-04-02 19:14  1.11
2015-08-15 15:53  1.10
2014-10-06 05:02  1.9
2014-05-09 19:17  1.8.1
2014-03-09 06:52  1.8
2014-01-16 19:35  1.7
2013-10-23 04:16  1.6
2013-03-11 06:17  1.5
2012-05-22 04:57  1.4.1 ***

========================================================================
Presently in use: org.apache.commons:commons-compress  1.7
   - a level 8 dependencies among 2 (possibly transitive) uses
2017-10-14 13:28  1.15
2017-05-11 19:16  1.14
2016-12-25 12:26  1.13
2016-06-18 15:42  1.12
2016-04-02 19:14  1.11
2015-08-15 15:53  1.10
2014-10-06 05:02  1.9
2014-05-09 19:17  1.8.1
2014-03-09 06:52  1.8
2014-01-16 19:35  1.7 ***

========================================================================
Presently in use: org.apache.commons:commons-crypto  1.0.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2016-07-26 01:20  1.0.0 ***

========================================================================
Presently in use: org.apache.commons:commons-lang3  3.3.1
   - a level 2 dependencies among 2 (possibly transitive) uses
2017-11-04 18:16  3.7
2017-06-09 09:41  3.6
2016-10-13 19:53  3.5
2015-04-03 12:31  3.4
2014-04-06 12:21  3.3.2
2014-03-15 13:04  3.3.1 ***

========================================================================
Presently in use: org.apache.commons:commons-lang3  3.5
   - a level 5 dependencies among 2 (possibly transitive) uses
2017-11-04 18:16  3.7
2017-06-09 09:41  3.6
2016-10-13 19:53  3.5 ***

========================================================================
Presently in use: org.apache.commons:commons-math3  3.4.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2016-03-17 17:35  3.6.1
2016-01-02 19:37  3.6
2015-04-14 12:39  3.5
2015-01-08 17:28  3.4.1 ***

========================================================================
Presently in use: org.apache.commons:commons-math  2.1
   - a level 6 dependencies among 2 (possibly transitive) uses
2011-02-26 18:24  2.2
2010-03-28 02:48  2.1 ***

========================================================================
Presently in use: org.apache.curator:curator-client  2.4.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-07-26 14:09  4.0.0
2017-03-01 04:28  3.3.0
2017-03-01 03:17  2.12.0
2016-11-11 14:33  3.2.1
2016-11-11 13:43  2.11.1
2016-06-15 02:16  3.2.0
2016-06-15 01:15  2.11.0
2016-02-10 20:17  2.10.0
2016-02-10 20:05  3.1.0
2015-10-26 02:01  2.9.1
2015-10-12 05:29  3.0.0
2015-09-02 17:59  2.9.0
2015-05-08 19:00  2.8.0
2015-01-13 13:31  2.7.1
2014-10-31 04:33  2.7.0
2014-07-08 03:00  2.6.0
2014-05-24 16:28  2.5.0
2014-04-21 22:05  2.4.2
2014-03-06 12:35  2.4.1
2014-02-05 23:08  2.4.0 ***

========================================================================
Presently in use: org.apache.curator:curator-framework  2.4.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-07-26 14:09  4.0.0
2017-03-01 04:29  3.3.0
2017-03-01 03:17  2.12.0
2016-11-11 14:33  3.2.1
2016-11-11 13:43  2.11.1
2016-06-15 02:16  3.2.0
2016-06-15 01:16  2.11.0
2016-02-10 20:18  2.10.0
2016-02-10 20:06  3.1.0
2015-10-26 02:01  2.9.1
2015-10-12 05:29  3.0.0
2015-09-02 18:00  2.9.0
2015-05-08 19:00  2.8.0
2015-01-13 13:32  2.7.1
2014-10-31 04:33  2.7.0
2014-07-08 03:01  2.6.0
2014-05-24 16:29  2.5.0
2014-04-21 22:06  2.4.2
2014-03-06 12:36  2.4.1
2014-02-05 23:08  2.4.0 ***

========================================================================
Presently in use: org.apache.curator:curator-recipes  2.4.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-07-26 14:10  4.0.0
2017-03-01 04:29  3.3.0
2017-03-01 03:17  2.12.0
2016-11-11 14:33  3.2.1
2016-11-11 13:44  2.11.1
2016-06-15 02:17  3.2.0
2016-06-15 01:16  2.11.0
2016-02-10 20:18  2.10.0
2016-02-10 20:06  3.1.0
2015-10-26 02:02  2.9.1
2015-10-12 05:30  3.0.0
2015-09-02 18:00  2.9.0
2015-05-08 19:01  2.8.0
2015-01-13 13:32  2.7.1
2014-10-31 04:34  2.7.0
2014-07-08 03:01  2.6.0
2014-05-24 16:29  2.5.0
2014-04-21 22:07  2.4.2
2014-03-06 12:36  2.4.1
2014-02-05 23:09  2.4.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-annotations  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:37  2.7.5
2017-12-08 20:14  3.0.0
2017-12-05 09:20  2.8.3
2017-11-13 23:53  2.9.0
2017-10-19 23:23  2.8.2
2017-07-28 20:48  2.7.4
2017-06-07 21:21  2.8.1
2017-03-17 08:39  2.8.0
2016-10-02 23:05  2.6.5
2016-08-18 00:59  2.7.3
2016-02-03 04:44  2.6.4
2016-01-14 21:31  2.7.2
2015-12-11 22:35  2.6.3
2015-10-22 20:16  2.6.2
2015-09-16 19:23  2.6.1
2015-06-29 01:14  2.7.1
2015-04-10 22:41  2.7.0
2014-11-14 23:53  2.5.2
2014-11-13 22:34  2.6.0
2014-09-05 23:04  2.5.1
2014-08-06 20:02  2.5.0
2014-06-21 06:08  2.4.1
2014-06-19 14:15  0.23.11
2014-03-31 08:31  2.4.0
2014-02-11 13:55  2.3.0
2013-12-03 05:44  0.23.10
2013-10-07 06:28  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-auth  2.2.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-12-16 01:37  2.7.5
2017-12-08 20:15  3.0.0
2017-12-05 09:21  2.8.3
2017-11-13 23:53  2.9.0
2017-10-19 23:23  2.8.2
2017-07-28 20:49  2.7.4
2017-06-07 21:22  2.8.1
2017-03-17 08:40  2.8.0
2016-10-02 23:07  2.6.5
2016-08-18 01:01  2.7.3
2016-02-03 04:47  2.6.4
2016-01-14 21:32  2.7.2
2015-12-11 22:38  2.6.3
2015-10-22 20:16  2.6.2
2015-09-16 19:24  2.6.1
2015-06-29 01:15  2.7.1
2015-04-10 22:42  2.7.0
2014-11-14 23:54  2.5.2
2014-11-13 22:35  2.6.0
2014-09-05 23:05  2.5.1
2014-08-06 20:02  2.5.0
2014-06-21 06:08  2.4.1
2014-06-19 14:15  0.23.11
2014-03-31 08:31  2.4.0
2014-02-11 13:55  2.3.0
2013-12-03 05:45  0.23.10
2013-10-07 06:28  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-client  2.2.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-12-16 01:42  2.7.5
2017-12-08 20:21  3.0.0
2017-12-05 09:29  2.8.3
2017-11-14 00:00  2.9.0
2017-10-19 23:32  2.8.2
2017-07-28 21:06  2.7.4
2017-06-07 21:37  2.8.1
2017-03-17 08:48  2.8.0
2016-10-02 23:29  2.6.5
2016-08-18 01:26  2.7.3
2016-02-03 05:50  2.6.4
2016-01-14 23:49  2.7.2
2015-12-11 23:46  2.6.3
2015-10-22 20:41  2.6.2
2015-09-16 19:41  2.6.1
2015-06-29 03:35  2.7.1
2015-04-10 22:55  2.7.0
2014-11-15 00:07  2.5.2
2014-11-13 22:53  2.6.0
2014-09-05 23:24  2.5.1
2014-08-06 20:21  2.5.0
2014-06-21 06:22  2.4.1
2014-06-19 14:28  0.23.11
2014-03-31 08:44  2.4.0
2014-02-11 14:07  2.3.0
2013-12-03 06:00  0.23.10
2013-10-07 06:39  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-common  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:37  2.7.5
2017-12-08 20:15  3.0.0
2017-12-05 09:21  2.8.3
2017-11-13 23:53  2.9.0
2017-10-19 23:24  2.8.2
2017-07-28 20:50  2.7.4
2017-06-07 21:23  2.8.1
2017-03-17 08:40  2.8.0
2016-10-02 23:08  2.6.5
2016-08-18 01:03  2.7.3
2016-02-03 04:51  2.6.4
2016-01-14 21:34  2.7.2
2015-12-11 22:41  2.6.3
2015-10-22 20:17  2.6.2
2015-09-16 19:25  2.6.1
2015-06-29 01:17  2.7.1
2015-04-10 22:43  2.7.0
2014-11-14 23:55  2.5.2
2014-11-13 22:37  2.6.0
2014-09-05 23:06  2.5.1
2014-08-06 20:03  2.5.0
2014-06-21 06:10  2.4.1
2014-06-19 14:17  0.23.11
2014-03-31 08:33  2.4.0
2014-02-11 13:57  2.3.0
2013-12-03 05:46  0.23.10
2013-10-07 06:30  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-hdfs  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:38  2.7.5
2017-12-08 20:16  3.0.0
2017-12-05 09:22  2.8.3
2017-11-13 23:55  2.9.0
2017-10-19 23:25  2.8.2
2017-07-28 20:54  2.7.4
2017-06-07 21:26  2.8.1
2017-03-17 08:42  2.8.0
2016-10-02 23:13  2.6.5
2016-08-18 01:45  2.7.3
2016-02-03 05:07  2.6.4
2016-01-14 22:10  2.7.2
2015-12-11 22:57  2.6.3
2015-10-22 20:23  2.6.2
2015-09-16 19:29  2.6.1
2015-06-29 01:54  2.7.1
2015-04-10 22:46  2.7.0
2014-11-14 23:58  2.5.2
2014-11-13 22:41  2.6.0
2014-09-05 23:10  2.5.1
2014-08-06 20:07  2.5.0
2014-06-21 06:13  2.4.1
2014-06-19 14:18  0.23.11
2014-03-31 08:36  2.4.0
2014-02-11 14:00  2.3.0
2013-12-03 05:47  0.23.10
2013-10-07 06:32  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-mapreduce-client-app  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:40  2.7.5
2017-12-08 20:19  3.0.0
2017-12-05 09:26  2.8.3
2017-11-13 23:58  2.9.0
2017-10-19 23:30  2.8.2
2017-07-28 21:02  2.7.4
2017-06-07 21:34  2.8.1
2017-03-17 08:46  2.8.0
2016-10-02 23:24  2.6.5
2016-08-18 01:22  2.7.3
2016-02-03 05:34  2.6.4
2016-01-14 23:30  2.7.2
2015-12-11 23:32  2.6.3
2015-10-22 20:37  2.6.2
2015-09-16 19:38  2.6.1
2015-06-29 03:15  2.7.1
2015-04-10 22:52  2.7.0
2014-11-15 00:05  2.5.2
2014-11-13 22:49  2.6.0
2014-09-05 23:21  2.5.1
2014-08-06 20:18  2.5.0
2014-06-21 06:20  2.4.1
2014-06-19 14:24  0.23.11
2014-03-31 08:42  2.4.0
2014-02-11 14:05  2.3.0
2013-12-03 05:56  0.23.10
2013-10-07 06:37  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-mapreduce-client-common  2.2.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-12-16 01:40  2.7.5
2017-12-08 20:19  3.0.0
2017-12-05 09:26  2.8.3
2017-11-13 23:58  2.9.0
2017-10-19 23:29  2.8.2
2017-07-28 21:02  2.7.4
2017-06-07 21:33  2.8.1
2017-03-17 08:46  2.8.0
2016-10-02 23:24  2.6.5
2016-08-18 01:21  2.7.3
2016-02-03 05:33  2.6.4
2016-01-14 23:29  2.7.2
2015-12-11 23:30  2.6.3
2015-10-22 20:37  2.6.2
2015-09-16 19:37  2.6.1
2015-06-29 03:14  2.7.1
2015-04-10 22:52  2.7.0
2014-11-15 00:05  2.5.2
2014-11-13 22:49  2.6.0
2014-09-05 23:20  2.5.1
2014-08-06 20:17  2.5.0
2014-06-21 06:20  2.4.1
2014-06-19 14:24  0.23.11
2014-03-31 08:42  2.4.0
2014-02-11 14:05  2.3.0
2013-12-03 05:56  0.23.10
2013-10-07 06:36  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-mapreduce-client-core  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:40  2.7.5
2017-12-08 20:19  3.0.0
2017-12-05 09:26  2.8.3
2017-11-13 23:58  2.9.0
2017-10-19 23:29  2.8.2
2017-07-28 21:01  2.7.4
2017-06-07 21:33  2.8.1
2017-03-17 08:46  2.8.0
2016-10-02 23:23  2.6.5
2016-08-18 01:21  2.7.3
2016-02-03 05:32  2.6.4
2016-01-14 23:26  2.7.2
2015-12-11 23:29  2.6.3
2015-10-22 20:36  2.6.2
2015-09-16 19:37  2.6.1
2015-06-29 03:11  2.7.1
2015-04-10 22:51  2.7.0
2014-11-15 00:04  2.5.2
2014-11-13 22:48  2.6.0
2014-09-05 23:20  2.5.1
2014-08-06 20:17  2.5.0
2014-06-21 06:19  2.4.1
2014-06-19 14:23  0.23.11
2014-03-31 08:42  2.4.0
2014-02-11 14:05  2.3.0
2013-12-03 05:54  0.23.10
2013-10-07 06:36  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-mapreduce-client-jobclient  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:41  2.7.5
2017-12-08 20:19  3.0.0
2017-12-05 09:27  2.8.3
2017-11-13 23:59  2.9.0
2017-10-19 23:30  2.8.2
2017-07-28 21:03  2.7.4
2017-06-07 21:34  2.8.1
2017-03-17 08:46  2.8.0
2016-10-02 23:25  2.6.5
2016-08-18 01:22  2.7.3
2016-02-03 05:36  2.6.4
2016-01-14 23:32  2.7.2
2015-12-11 23:34  2.6.3
2015-10-22 20:38  2.6.2
2015-09-16 19:38  2.6.1
2015-06-29 03:17  2.7.1
2015-04-10 22:52  2.7.0
2014-11-15 00:05  2.5.2
2014-11-13 22:50  2.6.0
2014-09-05 23:21  2.5.1
2014-08-06 20:18  2.5.0
2014-06-21 06:20  2.4.1
2014-06-19 14:25  0.23.11
2014-03-31 08:42  2.4.0
2014-02-11 14:06  2.3.0
2013-12-03 05:57  0.23.10
2013-10-07 06:37  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-mapreduce-client-shuffle  2.2.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-12-16 01:40  2.7.5
2017-12-08 20:19  3.0.0
2017-12-05 09:26  2.8.3
2017-11-13 23:58  2.9.0
2017-10-19 23:30  2.8.2
2017-07-28 21:02  2.7.4
2017-06-07 21:33  2.8.1
2017-03-17 08:46  2.8.0
2016-10-02 23:24  2.6.5
2016-08-18 01:21  2.7.3
2016-02-03 05:33  2.6.4
2016-01-14 23:30  2.7.2
2015-12-11 23:31  2.6.3
2015-10-22 20:37  2.6.2
2015-09-16 19:37  2.6.1
2015-06-29 03:15  2.7.1
2015-04-10 22:52  2.7.0
2014-11-15 00:05  2.5.2
2014-11-13 22:49  2.6.0
2014-09-05 23:21  2.5.1
2014-08-06 20:17  2.5.0
2014-06-21 06:20  2.4.1
2014-06-19 14:24  0.23.11
2014-03-31 08:42  2.4.0
2014-02-11 14:05  2.3.0
2013-12-03 05:56  0.23.10
2013-10-07 06:37  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-yarn-api  2.2.0
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-12-16 01:39  2.7.5
2017-12-08 20:16  3.0.0
2017-12-05 09:24  2.8.3
2017-11-13 23:56  2.9.0
2017-10-19 23:27  2.8.2
2017-07-28 20:57  2.7.4
2017-06-07 21:28  2.8.1
2017-03-17 08:43  2.8.0
2016-10-02 23:19  2.6.5
2016-08-18 01:16  2.7.3
2016-02-03 05:20  2.6.4
2016-01-14 23:12  2.7.2
2015-12-11 23:15  2.6.3
2015-10-22 20:31  2.6.2
2015-09-16 19:33  2.6.1
2015-06-29 02:57  2.7.1
2015-04-10 22:48  2.7.0
2014-11-15 00:02  2.5.2
2014-11-13 22:45  2.6.0
2014-09-05 23:17  2.5.1
2014-08-06 20:14  2.5.0
2014-06-21 06:17  2.4.1
2014-06-19 14:20  0.23.11
2014-03-31 08:40  2.4.0
2014-02-11 14:03  2.3.0
2013-12-03 05:50  0.23.10
2013-10-07 06:34  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-yarn-client  2.2.0
   - a level 6 dependencies among 1 (possibly transitive) uses
2017-12-16 01:40  2.7.5
2017-12-08 20:18  3.0.0
2017-12-05 09:25  2.8.3
2017-11-13 23:57  2.9.0
2017-10-19 23:28  2.8.2
2017-07-28 21:00  2.7.4
2017-06-07 21:31  2.8.1
2017-03-17 08:44  2.8.0
2016-10-02 23:22  2.6.5
2016-08-18 01:19  2.7.3
2016-02-03 05:28  2.6.4
2016-01-14 23:23  2.7.2
2015-12-11 23:25  2.6.3
2015-10-22 20:35  2.6.2
2015-09-16 19:36  2.6.1
2015-06-29 03:09  2.7.1
2015-04-10 22:50  2.7.0
2014-11-15 00:04  2.5.2
2014-11-13 22:47  2.6.0
2014-09-05 23:19  2.5.1
2014-08-06 20:16  2.5.0
2014-06-21 06:19  2.4.1
2014-06-19 14:22  0.23.11
2014-03-31 08:41  2.4.0
2014-02-11 14:04  2.3.0
2013-12-03 05:54  0.23.10
2013-10-07 06:36  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-yarn-common  2.2.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-12-16 01:39  2.7.5
2017-12-08 20:16  3.0.0
2017-12-05 09:24  2.8.3
2017-11-13 23:56  2.9.0
2017-10-19 23:27  2.8.2
2017-07-28 20:58  2.7.4
2017-06-07 21:29  2.8.1
2017-03-17 08:43  2.8.0
2016-10-02 23:19  2.6.5
2016-08-18 01:17  2.7.3
2016-02-03 05:21  2.6.4
2016-01-14 23:15  2.7.2
2015-12-11 23:17  2.6.3
2015-10-22 20:32  2.6.2
2015-09-16 19:33  2.6.1
2015-06-29 03:00  2.7.1
2015-04-10 22:49  2.7.0
2014-11-15 00:03  2.5.2
2014-11-13 22:45  2.6.0
2014-09-05 23:18  2.5.1
2014-08-06 20:15  2.5.0
2014-06-21 06:17  2.4.1
2014-06-19 14:20  0.23.11
2014-03-31 08:40  2.4.0
2014-02-11 14:03  2.3.0
2013-12-03 05:52  0.23.10
2013-10-07 06:35  2.2.0 ***

========================================================================
Presently in use: org.apache.hadoop:hadoop-yarn-server-common  2.2.0
   - a level 6 dependencies among 1 (possibly transitive) uses
2017-12-16 01:39  2.7.5
2017-12-08 20:17  3.0.0
2017-12-05 09:24  2.8.3
2017-11-13 23:56  2.9.0
2017-10-19 23:27  2.8.2
2017-07-28 20:58  2.7.4
2017-06-07 21:29  2.8.1
2017-03-17 08:44  2.8.0
2016-10-02 23:20  2.6.5
2016-08-18 01:17  2.7.3
2016-02-03 05:23  2.6.4
2016-01-14 23:17  2.7.2
2015-12-11 23:18  2.6.3
2015-10-22 20:33  2.6.2
2015-09-16 19:34  2.6.1
2015-06-29 03:03  2.7.1
2015-04-10 22:49  2.7.0
2014-11-15 00:03  2.5.2
2014-11-13 22:46  2.6.0
2014-09-05 23:18  2.5.1
2014-08-06 20:15  2.5.0
2014-06-21 06:18  2.4.1
2014-06-19 14:21  0.23.11
2014-03-31 08:40  2.4.0
2014-02-11 14:03  2.3.0
2013-12-03 05:52  0.23.10
2013-10-07 06:35  2.2.0 ***

========================================================================
Presently in use: org.apache.httpcomponents:httpclient  4.2.5
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-18 11:54  4.5.5
2017-11-27 09:42  4.5.4
2017-01-21 16:00  4.5.3
2016-02-21 16:05  4.5.2
2015-09-11 12:56  4.5.1
2015-05-31 11:11  4.5
2015-03-24 15:43  4.4.1
2015-01-27 20:57  4.4
2014-11-02 13:46  4.3.6
2014-07-30 18:24  4.3.5
2014-05-31 15:19  4.3.4
2014-02-22 14:05  4.3.3
2014-01-15 18:43  4.3.2
2013-10-03 19:43  4.3.1
2013-09-04 18:22  4.3
2013-09-04 18:16  4.2.6
2013-04-19 16:29  4.2.5 ***

========================================================================
Presently in use: org.apache.httpcomponents:httpcore  4.2.4
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-12 03:42  4.4.9
2017-09-29 14:23  4.4.8
2017-09-10 10:22  4.4.7
2017-01-07 13:50  4.4.6
2016-06-08 16:39  4.4.5
2015-10-26 17:18  4.4.4
2015-09-04 18:40  4.4.3
2015-08-30 18:36  4.4.2
2015-03-14 16:29  4.4.1
2014-12-14 12:30  4.4
2014-10-18 11:51  4.3.3
2014-02-12 20:44  4.3.2
2013-12-18 14:06  4.3.1
2013-07-29 15:14  4.2.5
2013-07-29 15:06  4.3
2013-03-20 16:12  4.2.4 ***

========================================================================
Presently in use: org.apache.ivy:ivy  2.4.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2014-12-22 16:40  2.4.0 ***

========================================================================
Presently in use: org.apache.lucene:lucene-analyzers-common  4.10.3
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-14 09:36  7.2.1
2017-12-19 09:03  7.2.0
2017-10-23 15:58  5.5.5
2017-10-17 19:02  6.6.2
2017-10-16 17:55  7.1.0
2017-10-05 21:26  7.0.1
2017-09-19 04:58  7.0.0
2017-09-05 14:26  6.6.1
2017-06-05 17:11  6.6.0
2017-04-26 18:08  6.5.1
2017-03-25 08:24  6.5.0
2017-03-06 18:34  6.4.2
2017-02-14 08:36  5.5.4
2017-02-04 18:35  6.4.1
2017-01-20 18:24  6.4.0
2016-11-08 05:21  6.3.0
2016-09-19 15:38  6.2.1
2016-09-08 16:13  5.5.3
2016-08-24 18:42  6.2.0
2016-06-24 18:22  5.5.2
2016-06-16 12:04  6.1.0
2016-05-27 12:54  6.0.1
2016-05-05 07:38  5.5.1
2016-04-07 15:14  6.0.0
2016-02-20 10:16  5.5.0
2016-01-22 19:20  5.3.2
2016-01-21 15:31  5.4.1
2015-12-11 14:37  5.4.0
2015-09-28 16:45  5.3.1
2015-08-20 12:32  5.3.0
2015-06-14 22:15  5.2.1
2015-06-06 18:17  5.2.0
2015-04-13 15:28  5.1.0
2015-03-03 08:23  4.10.4
2015-02-19 09:07  5.0.0
2014-12-20 17:31  4.10.3 ***

========================================================================
Presently in use: org.apache.lucene:lucene-core  4.10.3
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-14 09:33  7.2.1
2017-12-19 09:09  7.2.0
2017-10-23 15:59  5.5.5
2017-10-17 19:03  6.6.2
2017-10-16 17:55  7.1.0
2017-10-05 21:27  7.0.1
2017-09-19 04:54  7.0.0
2017-09-05 14:22  6.6.1
2017-06-05 17:17  6.6.0
2017-04-26 18:04  6.5.1
2017-03-25 08:19  6.5.0
2017-03-06 18:35  6.4.2
2017-02-14 08:41  5.5.4
2017-02-04 18:41  6.4.1
2017-01-20 18:25  6.4.0
2016-11-08 05:16  6.3.0
2016-09-19 15:33  6.2.1
2016-09-08 16:09  5.5.3
2016-08-24 18:40  6.2.0
2016-06-24 18:25  5.5.2
2016-06-16 12:15  6.1.0
2016-05-27 12:56  6.0.1
2016-05-05 07:35  5.5.1
2016-04-07 15:10  6.0.0
2016-02-20 10:17  5.5.0
2016-01-22 19:18  5.3.2
2016-01-21 15:46  5.4.1
2015-12-11 14:28  5.4.0
2015-09-28 16:29  5.3.1
2015-08-20 12:20  5.3.0
2015-06-14 22:09  5.2.1
2015-06-06 18:15  5.2.0
2015-04-13 15:24  5.1.0
2015-03-03 08:21  4.10.4
2015-02-19 09:04  5.0.0
2014-12-20 17:31  4.10.3 ***

========================================================================
Presently in use: org.apache.lucene:lucene-queries  4.10.3
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-14 09:32  7.2.1
2017-12-19 09:25  7.2.0
2017-10-23 16:00  5.5.5
2017-10-17 18:48  6.6.2
2017-10-16 17:56  7.1.0
2017-10-05 21:29  7.0.1
2017-09-19 04:51  7.0.0
2017-09-05 14:19  6.6.1
2017-06-05 17:22  6.6.0
2017-04-26 18:01  6.5.1
2017-03-25 08:16  6.5.0
2017-03-06 18:22  6.4.2
2017-02-14 08:33  5.5.4
2017-02-04 18:30  6.4.1
2017-01-20 18:23  6.4.0
2016-11-08 05:27  6.3.0
2016-09-19 15:44  6.2.1
2016-09-08 16:06  5.5.3
2016-08-24 18:42  6.2.0
2016-06-24 18:27  5.5.2
2016-06-16 11:59  6.1.0
2016-05-27 12:58  6.0.1
2016-05-05 07:29  5.5.1
2016-04-07 15:11  6.0.0
2016-02-20 10:07  5.5.0
2016-01-22 19:16  5.3.2
2016-01-21 15:22  5.4.1
2015-12-11 14:23  5.4.0
2015-09-28 16:21  5.3.1
2015-08-20 12:12  5.3.0
2015-06-14 22:22  5.2.1
2015-06-06 18:14  5.2.0
2015-04-13 15:23  5.1.0
2015-03-03 08:19  4.10.4
2015-02-19 09:02  5.0.0
2014-12-20 17:31  4.10.3 ***

========================================================================
Presently in use: org.apache.lucene:lucene-queryparser  4.10.3
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-14 09:32  7.2.1
2017-12-19 09:22  7.2.0
2017-10-23 16:00  5.5.5
2017-10-17 18:51  6.6.2
2017-10-16 17:56  7.1.0
2017-10-05 21:29  7.0.1
2017-09-19 04:51  7.0.0
2017-09-05 14:19  6.6.1
2017-06-05 17:05  6.6.0
2017-04-26 18:00  6.5.1
2017-03-25 08:15  6.5.0
2017-03-06 18:24  6.4.2
2017-02-14 08:33  5.5.4
2017-02-04 18:29  6.4.1
2017-01-20 18:23  6.4.0
2016-11-08 05:19  6.3.0
2016-09-19 15:35  6.2.1
2016-09-08 16:06  5.5.3
2016-08-24 18:39  6.2.0
2016-06-24 18:27  5.5.2
2016-06-16 11:59  6.1.0
2016-05-27 12:58  6.0.1
2016-05-05 07:28  5.5.1
2016-04-07 15:14  6.0.0
2016-02-20 10:06  5.5.0
2016-01-22 19:16  5.3.2
2016-01-21 15:21  5.4.1
2015-12-11 14:22  5.4.0
2015-09-28 16:20  5.3.1
2015-08-20 12:11  5.3.0
2015-06-14 22:12  5.2.1
2015-06-06 18:14  5.2.0
2015-04-13 15:23  5.1.0
2015-03-03 08:19  4.10.4
2015-02-19 09:02  5.0.0
2014-12-20 17:30  4.10.3 ***

========================================================================
Presently in use: org.apache.lucene:lucene-sandbox  4.10.3
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-14 09:31  7.2.1
2017-12-19 09:17  7.2.0
2017-10-23 15:58  5.5.5
2017-10-17 18:55  6.6.2
2017-10-16 17:55  7.1.0
2017-10-05 21:26  7.0.1
2017-09-19 04:50  7.0.0
2017-09-05 14:18  6.6.1
2017-06-05 17:16  6.6.0
2017-04-26 18:00  6.5.1
2017-03-25 08:15  6.5.0
2017-03-06 18:28  6.4.2
2017-02-14 08:39  5.5.4
2017-02-04 18:38  6.4.1
2017-01-20 18:23  6.4.0
2016-11-08 05:32  6.3.0
2016-09-19 15:48  6.2.1
2016-09-08 16:05  5.5.3
2016-08-24 18:41  6.2.0
2016-06-24 18:22  5.5.2
2016-06-16 12:09  6.1.0
2016-05-27 12:53  6.0.1
2016-05-05 07:28  5.5.1
2016-04-07 15:09  6.0.0
2016-02-20 10:06  5.5.0
2016-01-22 19:16  5.3.2
2016-01-21 15:38  5.4.1
2015-12-11 14:20  5.4.0
2015-09-28 16:18  5.3.1
2015-08-20 12:09  5.3.0
2015-06-14 22:26  5.2.1
2015-06-06 18:14  5.2.0
2015-04-13 15:22  5.1.0
2015-03-03 08:18  4.10.4
2015-02-19 09:02  5.0.0
2014-12-20 17:29  4.10.3 ***

========================================================================
Presently in use: org.apache.spark:spark-core_2.11  2.1.1
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-11-25 05:29  2.2.1
2017-10-03 03:05  2.1.2
2017-07-01 00:34  2.2.0
2017-04-26 00:44  2.1.1 ***

========================================================================
Presently in use: org.apache.spark:spark-launcher_2.11  2.1.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-25 05:13  2.2.1
2017-10-03 02:38  2.1.2
2017-07-01 00:38  2.2.0
2017-04-26 00:48  2.1.1 ***

========================================================================
Presently in use: org.apache.spark:spark-network-common_2.11  2.1.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-25 05:09  2.2.1
2017-10-03 02:44  2.1.2
2017-07-01 00:34  2.2.0
2017-04-26 00:43  2.1.1 ***

========================================================================
Presently in use: org.apache.spark:spark-network-shuffle_2.11  2.1.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-25 05:12  2.2.1
2017-10-03 03:11  2.1.2
2017-07-01 00:40  2.2.0
2017-04-26 00:50  2.1.1 ***

========================================================================
Presently in use: org.apache.spark:spark-tags_2.11  2.1.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-25 05:22  2.2.1
2017-10-03 03:02  2.1.2
2017-07-01 00:35  2.2.0
2017-04-26 00:44  2.1.1 ***

========================================================================
Presently in use: org.apache.spark:spark-unsafe_2.11  2.1.1
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-25 05:10  2.2.1
2017-10-03 02:40  2.1.2
2017-07-01 00:33  2.2.0
2017-04-26 00:43  2.1.1 ***

========================================================================
Presently in use: org.apache.xbean:xbean-asm5-shaded  4.4
   - a level 3 dependencies among 1 (possibly transitive) uses
2015-11-23 10:46  4.5
2015-09-10 04:48  4.4 ***

========================================================================
Presently in use: org.apache.zookeeper:zookeeper  3.4.5
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-11-01 19:08  3.4.11
2017-03-23 12:08  3.4.10
2016-08-23 08:55  3.4.9
2016-02-06 03:56  3.4.8
2015-11-11 07:10  3.4.7
2014-02-23 17:18  3.4.6
2012-11-19 00:57  3.4.5 ***

========================================================================
Presently in use: org.boofcv:boofcv-WebcamCapture  0.28
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-01-20 16:09  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-calibration  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:11  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-core  0.28
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-01-20 16:11  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-feature  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:11  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-geo  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:12  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-io  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:12  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-ip  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:12  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-learning  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:12  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-recognition  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:13  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-sfm  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:13  0.28 ***

========================================================================
Presently in use: org.boofcv:boofcv-swing  0.28
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-20 16:11  0.28 ***

========================================================================
Presently in use: org.codehaus.jackson:jackson-core-asl  1.9.13
   - a level 4 dependencies among 1 (possibly transitive) uses
2012-11-06 16:27  1.9.11
2012-10-02 01:38  1.8.11
2012-09-24 02:55  1.9.10
2012-07-28 17:37  1.9.9
2012-07-15 18:41  1.8.10
2012-06-29 00:02  1.9.8
2012-05-02 17:49  1.9.7
2012-03-27 03:16  1.9.6
2012-03-27 03:11  1.8.9
2012-02-25 06:09  1.9.5
2012-01-21 01:24  1.8.8
2012-01-21 01:19  1.9.4
2011-12-17 06:38  1.9.3
2011-12-17 05:17  1.8.7
2011-11-05 02:40  1.9.2
2011-10-24 01:22  1.9.1
2011-10-05 01:08  1.8.6
2011-10-05 00:57  1.9.0
2011-08-13 04:12  1.7.9
2011-08-05 00:45  1.8.5
2011-08-05 00:15  1.6.9
2011-07-26 01:46  1.8.4
2011-07-09 05:22  1.8.3
2011-07-09 05:17  1.7.8
2011-06-16 04:32  1.8.2
2011-05-18 04:33  1.8.1
2011-05-18 04:26  1.7.7
2011-04-21 05:29  1.8.0
2011-04-13 05:04  1.7.6
2011-04-02 03:26  1.7.5
2011-04-02 03:25  1.6.7
2011-03-05 03:12  1.7.4
2011-02-15 02:36  1.7.3
2011-02-15 02:29  1.6.6
2011-02-03 03:41  1.7.2
2011-02-02 01:15  1.6.5
2011-01-13 04:42  1.7.1
2011-01-07 04:59  1.7.0
2010-12-21 22:58  1.5.8
2010-12-21 22:54  1.6.4
2010-12-05 00:15  1.6.3
2010-11-02 23:47  1.6.2
2010-10-07 04:35  1.6.1
2010-10-04 02:32  1.5.7
2010-09-07 05:24  1.6.0
2010-08-18 05:45  1.5.6
2010-07-24 22:52  1.5.5
2010-06-26 04:17  1.5.4
2010-06-26 03:41  1.4.5
2010-05-31 22:05  1.5.3
2010-04-26 02:41  1.4.4
2010-04-25 22:07  1.5.2
2010-04-10 03:12  1.5.1
2010-03-14 06:35  1.5.0
2010-02-19 07:14  1.4.3
2010-02-19 07:01  1.3.5
2010-02-01 03:18  1.3.4
2010-02-01 03:17  1.4.2
2010-01-11 04:12  1.4.1
2009-12-22 08:03  1.3.3
2009-12-20 01:22  1.4.0
2009-12-03 03:40  1.3.2
2009-11-24 03:17  1.3.1
2009-10-31 02:14  1.3.0
2009-10-04 02:02  1.2.1
2009-08-03 02:08  1.2.0
2009-08-01 06:05  1.1.2
2009-07-19 02:45  1.1.1
2009-06-23 03:25  1.1.0
2009-06-05 01:55  1.0.1
2009-05-10 01:38  1.0.0
2009-04-28 06:09  0.9.9-6
2009-04-21 06:07  0.9.9-5
2009-04-15 05:28  0.9.9-4
2009-04-03 17:35  0.9.9-3
2009-03-20 03:29  0.9.9-2
2009-03-03 06:38  0.9.9
2009-02-17 06:45  0.9.8
2009-02-04 21:48  0.9.7
unknown-date unknown:time  1.9.13 ***

========================================================================
Presently in use: org.codehaus.jackson:jackson-mapper-asl  1.9.13
   - a level 4 dependencies among 1 (possibly transitive) uses
2012-11-06 16:27  1.9.11
2012-10-02 01:39  1.8.11
2012-09-24 02:56  1.9.10
2012-07-28 17:38  1.9.9
2012-07-15 18:41  1.8.10
2012-06-29 00:02  1.9.8
2012-05-02 17:49  1.9.7
2012-03-27 03:17  1.9.6
2012-03-27 03:12  1.8.9
2012-02-25 06:10  1.9.5
2012-01-21 01:25  1.8.8
2012-01-21 01:20  1.9.4
2011-12-17 06:39  1.9.3
2011-12-17 05:17  1.8.7
2011-11-05 02:40  1.9.2
2011-10-24 01:23  1.9.1
2011-10-05 01:08  1.8.6
2011-10-05 00:58  1.9.0
2011-08-13 04:12  1.7.9
2011-08-05 00:46  1.8.5
2011-08-05 00:15  1.6.9
2011-07-26 01:46  1.8.4
2011-07-09 05:23  1.8.3
2011-07-09 05:17  1.7.8
2011-06-16 04:33  1.8.2
2011-05-18 04:34  1.8.1
2011-05-18 04:27  1.7.7
2011-04-21 05:30  1.8.0
2011-04-13 05:05  1.7.6
2011-04-02 03:26  1.7.5
2011-04-02 03:25  1.6.7
2011-03-05 03:12  1.7.4
2011-02-15 02:36  1.7.3
2011-02-15 02:30  1.6.6
2011-02-03 03:41  1.7.2
2011-02-02 01:16  1.6.5
2011-01-13 04:42  1.7.1
2011-01-07 05:00  1.7.0
2010-12-21 22:58  1.5.8
2010-12-21 22:54  1.6.4
2010-12-05 00:15  1.6.3
2010-11-02 23:47  1.6.2
2010-10-07 04:35  1.6.1
2010-10-04 02:33  1.5.7
2010-09-07 05:25  1.6.0
2010-08-18 05:45  1.5.6
2010-07-24 22:52  1.5.5
2010-06-26 04:17  1.5.4
2010-06-26 03:41  1.4.5
2010-05-31 22:05  1.5.3
2010-04-26 02:42  1.4.4
2010-04-25 22:08  1.5.2
2010-04-10 03:12  1.5.1
2010-03-14 06:35  1.5.0
2010-02-19 07:15  1.4.3
2010-02-19 07:02  1.3.5
2010-02-01 03:19  1.3.4
2010-02-01 03:17  1.4.2
2010-01-11 04:13  1.4.1
2009-12-22 08:04  1.3.3
2009-12-20 01:22  1.4.0
2009-12-03 03:40  1.3.2
2009-11-24 03:17  1.3.1
2009-10-31 02:15  1.3.0
2009-10-04 02:03  1.2.1
2009-08-03 02:08  1.2.0
2009-08-01 06:05  1.1.2
2009-07-19 02:45  1.1.1
2009-06-23 03:25  1.1.0
2009-06-05 01:55  1.0.1
2009-05-10 01:38  1.0.0
2009-04-28 06:09  0.9.9-6
2009-04-21 06:08  0.9.9-5
2009-04-15 05:29  0.9.9-4
2009-04-03 17:35  0.9.9-3
2009-03-20 03:30  0.9.9-2
2009-03-03 06:39  0.9.9
2009-02-17 06:46  0.9.8
2009-02-04 21:49  0.9.7
unknown-date unknown:time  1.9.13 ***

========================================================================
Presently in use: org.ddogleg:ddogleg  0.13
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-17 21:48  0.13 ***

========================================================================
Presently in use: org.deepboof:io  0.4
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-08-14 06:29  0.4 ***

========================================================================
Presently in use: org.deepboof:learning  0.4
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-08-14 06:30  0.4 ***

========================================================================
Presently in use: org.deepboof:main  0.4
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-08-14 06:30  0.4 ***

========================================================================
Presently in use: org.deepboof:models  0.4
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-08-14 06:30  0.4 ***

========================================================================
Presently in use: org.ejml:ejml-cdense  0.33
   - a level 5 dependencies among 1 (possibly transitive) uses
2018-01-17 16:37  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-core  0.33
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-17 16:38  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-ddense  0.33
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-17 16:38  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-dsparse  0.33
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-17 16:38  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-fdense  0.33
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-17 16:38  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-simple  0.33
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-17 16:38  0.33 ***

========================================================================
Presently in use: org.ejml:ejml-zdense  0.33
   - a level 5 dependencies among 1 (possibly transitive) uses
2018-01-17 16:39  0.33 ***

========================================================================
Presently in use: org.fusesource.leveldbjni:leveldbjni-all  1.8
   - a level 4 dependencies among 1 (possibly transitive) uses
2013-10-17 13:18  1.8 ***

========================================================================
Presently in use: org.georegression:georegression  0.15
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-18 03:43  0.15 ***

========================================================================
Presently in use: org.glassfish.hk2.external:aopalliance-repackaged  2.4.0-b34
   - a level 5 dependencies among 1 (possibly transitive) uses
2018-01-05 22:42  2.5.0-b61
2017-11-09 20:42  2.5.0-b60
2017-10-20 14:49  2.5.0-b59
2017-10-17 14:09  2.5.0-b58
2017-10-07 13:48  2.5.0-b57
2017-10-06 13:56  2.5.0-b56
2017-09-27 18:29  2.5.0-b55
2017-09-14 10:55  2.5.0-b54
2017-09-13 19:20  2.5.0-b53
2017-09-11 16:09  2.5.0-b52
2017-09-11 15:21  2.5.0-b51
2017-09-10 12:10  2.5.0-b50
2017-09-09 23:40  2.5.0-b49
2017-09-08 17:28  2.5.0-b48
2017-09-07 02:02  2.5.0-b47
2017-09-05 18:11  2.5.0-b46
2017-08-28 10:40  2.5.0-b45
2017-07-21 02:39  2.5.0-b44
2017-07-18 23:53  2.5.0-b43
2017-07-11 00:59  2.5.0-b42
2017-07-06 22:12  2.5.0-b41
2017-07-06 21:47  2.5.0-b40
2017-06-14 16:10  2.5.0-b38
2017-06-06 00:55  2.5.0-b37
2017-03-08 22:57  2.5.0-b36
2017-02-28 02:22  2.5.0-b35
2017-02-17 18:32  2.5.0-b34
2017-02-17 00:26  2.5.0-b33
2017-01-18 18:01  2.5.0-b32
2016-12-23 14:18  2.5.0-b31
2016-12-02 17:53  2.5.0-b30
2016-11-29 20:12  2.5.0-b29
2016-11-08 20:11  2.5.0-b28
2016-10-21 14:11  2.5.0-b27
2016-10-20 16:12  2.5.0-b26
2016-10-18 12:57  2.5.0-b25
2016-10-11 14:26  2.5.0-b24
2016-10-07 12:32  2.5.0-b23
2016-10-06 12:20  2.5.0-b22
2016-10-02 01:17  2.5.0-b21
2016-09-30 18:02  2.5.0-b19
2016-09-26 15:56  2.5.0-b18
2016-09-26 14:13  2.5.0-b17
2016-09-16 16:07  2.5.0-b16
2016-09-13 18:10  2.5.0-b15
2016-09-12 13:19  2.5.0-b14
2016-09-09 15:17  2.5.0-b13
2016-09-07 02:38  2.5.0-b12
2016-09-04 14:44  2.5.0-b11
2016-08-31 15:49  2.5.0-b10
2016-08-29 18:46  2.5.0-b09
2016-08-24 21:32  2.5.0-b08
2016-08-12 16:40  2.5.0-b07
2016-06-29 18:40  2.5.0-b06
2016-05-27 19:07  2.5.0-b05
2016-04-18 15:41  2.5.0-b04
2016-01-21 16:32  2.5.0-b03
2016-01-20 22:59  2.5.0-b02
2016-01-06 13:06  2.5.0-b01
2016-01-05 20:06  2.4.0
2015-11-19 11:55  2.4.0-b34 ***

========================================================================
Presently in use: org.glassfish.hk2.external:javax.inject  2.4.0-b34
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-05 22:40  2.5.0-b61
2017-11-09 20:41  2.5.0-b60
2017-10-20 14:48  2.5.0-b59
2017-10-17 14:08  2.5.0-b58
2017-10-07 13:47  2.5.0-b57
2017-10-06 13:55  2.5.0-b56
2017-09-27 18:29  2.5.0-b55
2017-09-14 10:54  2.5.0-b54
2017-09-13 19:19  2.5.0-b53
2017-09-11 16:08  2.5.0-b52
2017-09-11 15:20  2.5.0-b51
2017-09-10 12:09  2.5.0-b50
2017-09-09 23:39  2.5.0-b49
2017-09-08 17:27  2.5.0-b48
2017-09-07 02:01  2.5.0-b47
2017-09-05 18:10  2.5.0-b46
2017-08-28 10:40  2.5.0-b45
2017-07-21 02:38  2.5.0-b44
2017-07-18 23:52  2.5.0-b43
2017-07-11 00:59  2.5.0-b42
2017-07-06 22:12  2.5.0-b41
2017-07-06 21:46  2.5.0-b40
2017-06-14 16:10  2.5.0-b38
2017-06-06 00:54  2.5.0-b37
2017-03-08 22:56  2.5.0-b36
2017-02-28 02:22  2.5.0-b35
2017-02-17 18:32  2.5.0-b34
2017-02-17 00:25  2.5.0-b33
2017-01-18 18:01  2.5.0-b32
2016-12-23 14:18  2.5.0-b31
2016-12-02 17:53  2.5.0-b30
2016-11-29 20:12  2.5.0-b29
2016-11-08 20:10  2.5.0-b28
2016-10-21 14:10  2.5.0-b27
2016-10-20 16:12  2.5.0-b26
2016-10-18 12:57  2.5.0-b25
2016-10-11 14:26  2.5.0-b24
2016-10-07 12:32  2.5.0-b23
2016-10-06 12:20  2.5.0-b22
2016-10-02 01:17  2.5.0-b21
2016-09-30 18:02  2.5.0-b19
2016-09-26 15:56  2.5.0-b18
2016-09-26 14:13  2.5.0-b17
2016-09-16 16:07  2.5.0-b16
2016-09-13 18:10  2.5.0-b15
2016-09-12 13:19  2.5.0-b14
2016-09-09 15:17  2.5.0-b13
2016-09-07 02:38  2.5.0-b12
2016-09-04 14:44  2.5.0-b11
2016-08-31 15:49  2.5.0-b10
2016-08-29 18:46  2.5.0-b09
2016-08-24 21:32  2.5.0-b08
2016-08-12 16:40  2.5.0-b07
2016-06-29 18:40  2.5.0-b06
2016-05-27 19:07  2.5.0-b05
2016-04-18 15:41  2.5.0-b04
2016-01-21 16:32  2.5.0-b03
2016-01-20 22:59  2.5.0-b02
2016-01-06 13:06  2.5.0-b01
2016-01-05 20:06  2.4.0
2015-11-19 11:55  2.4.0-b34 ***

========================================================================
Presently in use: org.glassfish.hk2:hk2-api  2.4.0-b34
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-05 22:42  2.5.0-b61
2017-11-09 20:43  2.5.0-b60
2017-10-20 14:49  2.5.0-b59
2017-10-17 14:10  2.5.0-b58
2017-10-07 13:48  2.5.0-b57
2017-10-06 13:57  2.5.0-b56
2017-09-27 18:30  2.5.0-b55
2017-09-14 10:56  2.5.0-b54
2017-09-13 19:20  2.5.0-b53
2017-09-11 16:09  2.5.0-b52
2017-09-11 15:22  2.5.0-b51
2017-09-10 12:11  2.5.0-b50
2017-09-09 23:40  2.5.0-b49
2017-09-08 17:28  2.5.0-b48
2017-09-07 02:02  2.5.0-b47
2017-09-05 18:11  2.5.0-b46
2017-08-28 10:41  2.5.0-b45
2017-07-21 02:39  2.5.0-b44
2017-07-18 23:53  2.5.0-b43
2017-07-11 01:01  2.5.0-b42
2017-07-06 22:13  2.5.0-b41
2017-07-06 21:48  2.5.0-b40
2017-06-14 16:11  2.5.0-b38
2017-06-06 00:56  2.5.0-b37
2017-03-08 22:57  2.5.0-b36
2017-02-28 02:23  2.5.0-b35
2017-02-17 18:33  2.5.0-b34
2017-02-17 00:27  2.5.0-b33
2017-01-18 18:02  2.5.0-b32
2016-12-23 14:19  2.5.0-b31
2016-12-02 17:54  2.5.0-b30
2016-11-29 20:13  2.5.0-b29
2016-11-08 20:12  2.5.0-b28
2016-10-21 14:11  2.5.0-b27
2016-10-20 16:13  2.5.0-b26
2016-10-18 12:58  2.5.0-b25
2016-10-11 14:28  2.5.0-b24
2016-10-07 12:33  2.5.0-b23
2016-10-06 12:21  2.5.0-b22
2016-10-02 01:18  2.5.0-b21
2016-09-30 18:04  2.5.0-b19
2016-09-26 15:57  2.5.0-b18
2016-09-26 14:14  2.5.0-b17
2016-09-16 16:08  2.5.0-b16
2016-09-13 18:11  2.5.0-b15
2016-09-12 13:20  2.5.0-b14
2016-09-09 15:17  2.5.0-b13
2016-09-07 02:39  2.5.0-b12
2016-09-04 14:45  2.5.0-b11
2016-08-31 15:51  2.5.0-b10
2016-08-29 18:47  2.5.0-b09
2016-08-24 21:33  2.5.0-b08
2016-08-12 16:40  2.5.0-b07
2016-06-29 18:41  2.5.0-b06
2016-05-27 19:08  2.5.0-b05
2016-04-18 15:41  2.5.0-b04
2016-01-21 16:33  2.5.0-b03
2016-01-20 23:00  2.5.0-b02
2016-01-06 13:07  2.5.0-b01
2016-01-05 20:07  2.4.0
2015-11-19 11:56  2.4.0-b34 ***

========================================================================
Presently in use: org.glassfish.hk2:hk2-locator  2.4.0-b34
   - a level 4 dependencies among 1 (possibly transitive) uses
2018-01-05 22:43  2.5.0-b61
2017-11-09 20:43  2.5.0-b60
2017-10-20 14:50  2.5.0-b59
2017-10-17 14:11  2.5.0-b58
2017-10-07 13:49  2.5.0-b57
2017-10-06 13:58  2.5.0-b56
2017-09-27 18:31  2.5.0-b55
2017-09-14 10:57  2.5.0-b54
2017-09-13 19:21  2.5.0-b53
2017-09-11 16:11  2.5.0-b52
2017-09-10 12:12  2.5.0-b50
2017-09-09 23:41  2.5.0-b49
2017-09-08 17:29  2.5.0-b48
2017-09-07 02:04  2.5.0-b47
2017-09-05 18:13  2.5.0-b46
2017-08-28 10:42  2.5.0-b45
2017-07-21 02:40  2.5.0-b44
2017-07-18 23:55  2.5.0-b43
2017-07-11 01:02  2.5.0-b42
2017-07-06 22:14  2.5.0-b41
2017-07-06 21:48  2.5.0-b40
2017-06-14 16:12  2.5.0-b38
2017-06-06 00:56  2.5.0-b37
2017-03-08 22:58  2.5.0-b36
2017-02-28 02:24  2.5.0-b35
2017-02-17 18:33  2.5.0-b34
2017-02-17 00:28  2.5.0-b33
2017-01-18 18:02  2.5.0-b32
2016-12-23 14:19  2.5.0-b31
2016-12-02 17:55  2.5.0-b30
2016-11-29 20:14  2.5.0-b29
2016-11-08 20:13  2.5.0-b28
2016-10-21 14:12  2.5.0-b27
2016-10-20 16:13  2.5.0-b26
2016-10-18 12:58  2.5.0-b25
2016-10-11 14:29  2.5.0-b24
2016-10-07 12:34  2.5.0-b23
2016-10-06 12:21  2.5.0-b22
2016-10-02 01:19  2.5.0-b21
2016-09-30 18:05  2.5.0-b19
2016-09-26 15:58  2.5.0-b18
2016-09-26 14:15  2.5.0-b17
2016-09-16 16:09  2.5.0-b16
2016-09-13 18:12  2.5.0-b15
2016-09-12 13:20  2.5.0-b14
2016-09-09 15:18  2.5.0-b13
2016-09-07 02:40  2.5.0-b12
2016-09-04 14:45  2.5.0-b11
2016-08-31 15:52  2.5.0-b10
2016-08-29 18:48  2.5.0-b09
2016-08-24 21:34  2.5.0-b08
2016-08-12 16:41  2.5.0-b07
2016-06-29 18:42  2.5.0-b06
2016-05-27 19:08  2.5.0-b05
2016-04-18 15:42  2.5.0-b04
2016-01-21 16:33  2.5.0-b03
2016-01-20 23:01  2.5.0-b02
2016-01-06 13:07  2.5.0-b01
2016-01-05 20:08  2.4.0
2015-11-19 11:56  2.4.0-b34 ***

========================================================================
Presently in use: org.glassfish.hk2:hk2-utils  2.4.0-b34
   - a level 5 dependencies among 1 (possibly transitive) uses
2018-01-05 22:41  2.5.0-b61
2017-11-09 20:42  2.5.0-b60
2017-10-20 14:48  2.5.0-b59
2017-10-17 14:09  2.5.0-b58
2017-10-07 13:48  2.5.0-b57
2017-10-06 13:56  2.5.0-b56
2017-09-27 18:29  2.5.0-b55
2017-09-14 10:55  2.5.0-b54
2017-09-13 19:19  2.5.0-b53
2017-09-11 16:09  2.5.0-b52
2017-09-11 15:21  2.5.0-b51
2017-09-10 12:10  2.5.0-b50
2017-09-09 23:40  2.5.0-b49
2017-09-08 17:27  2.5.0-b48
2017-09-07 02:02  2.5.0-b47
2017-09-05 18:11  2.5.0-b46
2017-08-28 10:40  2.5.0-b45
2017-07-21 02:39  2.5.0-b44
2017-07-18 23:53  2.5.0-b43
2017-07-11 01:00  2.5.0-b42
2017-07-06 22:13  2.5.0-b41
2017-07-06 21:47  2.5.0-b40
2017-06-14 16:11  2.5.0-b38
2017-06-06 00:55  2.5.0-b37
2017-03-08 22:57  2.5.0-b36
2017-02-28 02:23  2.5.0-b35
2017-02-17 18:33  2.5.0-b34
2017-02-17 00:27  2.5.0-b33
2017-01-18 18:01  2.5.0-b32
2016-12-23 14:19  2.5.0-b31
2016-12-02 17:54  2.5.0-b30
2016-11-29 20:13  2.5.0-b29
2016-11-08 20:11  2.5.0-b28
2016-10-21 14:11  2.5.0-b27
2016-10-20 16:13  2.5.0-b26
2016-10-18 12:57  2.5.0-b25
2016-10-11 14:27  2.5.0-b24
2016-10-07 12:33  2.5.0-b23
2016-10-06 12:21  2.5.0-b22
2016-10-02 01:18  2.5.0-b21
2016-09-30 18:03  2.5.0-b19
2016-09-26 15:57  2.5.0-b18
2016-09-26 14:14  2.5.0-b17
2016-09-16 16:08  2.5.0-b16
2016-09-13 18:11  2.5.0-b15
2016-09-12 13:19  2.5.0-b14
2016-09-09 15:17  2.5.0-b13
2016-09-07 02:39  2.5.0-b12
2016-09-04 14:45  2.5.0-b11
2016-08-31 15:50  2.5.0-b10
2016-08-29 18:47  2.5.0-b09
2016-08-24 21:33  2.5.0-b08
2016-08-12 16:40  2.5.0-b07
2016-06-29 18:41  2.5.0-b06
2016-05-27 19:07  2.5.0-b05
2016-04-18 15:41  2.5.0-b04
2016-01-21 16:33  2.5.0-b03
2016-01-20 23:00  2.5.0-b02
2016-01-06 13:06  2.5.0-b01
2016-01-05 20:07  2.4.0
2015-11-19 11:55  2.4.0-b34 ***

========================================================================
Presently in use: org.glassfish.hk2:osgi-resource-locator  1.0.1
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-07-11 01:04  2.5.0-b42
2017-07-06 22:16  2.5.0-b41
2017-07-06 21:50  2.5.0-b40
2017-06-14 16:14  2.5.0-b38
2017-06-06 00:58  2.5.0-b37
2017-03-08 22:59  2.5.0-b36
2017-02-28 02:25  2.5.0-b35
2017-02-17 18:35  2.5.0-b34
2017-02-17 00:30  2.5.0-b33
2017-01-18 18:03  2.5.0-b32
2016-12-23 14:21  2.5.0-b31
2016-12-02 17:56  2.5.0-b30
2016-11-29 20:15  2.5.0-b29
2016-11-08 20:15  2.5.0-b28
2016-10-21 14:13  2.5.0-b27
2016-10-20 16:15  2.5.0-b26
2016-10-18 12:59  2.5.0-b25
2016-10-11 14:31  2.5.0-b24
2016-10-07 12:36  2.5.0-b23
2016-10-06 12:24  2.5.0-b22
2016-10-02 01:21  2.5.0-b21
2016-09-30 18:07  2.5.0-b19
2016-09-26 15:59  2.5.0-b18
2016-09-26 14:16  2.5.0-b17
2016-09-16 16:10  2.5.0-b16
2016-09-13 18:14  2.5.0-b15
2016-09-12 13:21  2.5.0-b14
2016-09-09 15:19  2.5.0-b13
2016-09-07 02:42  2.5.0-b12
2016-09-04 14:47  2.5.0-b11
2016-08-31 15:54  2.5.0-b10
2016-08-29 18:49  2.5.0-b09
2016-08-24 21:35  2.5.0-b08
2016-08-12 16:42  2.5.0-b07
2016-06-29 18:43  2.5.0-b06
2016-05-27 19:10  2.5.0-b05
2016-04-18 15:43  2.5.0-b04
2016-01-21 16:35  2.5.0-b03
2016-01-20 23:02  2.5.0-b02
2016-01-06 13:08  2.5.0-b01
2016-01-05 20:09  2.4.0
unknown-date unknown:time  1.0.1 ***

========================================================================
Presently in use: org.glassfish.jersey.bundles.repackaged:jersey-guava  2.22.2
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-03-13 12:58  2.26-b03
2017-02-01 00:00  2.26-b02
2017-01-19 17:24  2.25.1
2017-01-13 20:32  2.26-b01
2016-12-08 14:11  2.25
2016-11-30 12:32  2.22.4
2016-11-21 17:48  2.24.1
2016-10-27 15:31  2.24
2016-10-26 07:41  2.22.3
2016-08-08 18:22  2.23.2
2016-06-09 19:52  2.23.1
2016-05-18 08:43  2.23
2016-02-16 12:27  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.containers:jersey-container-servlet-core  2.22.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-09-05 10:10  2.26
2017-07-27 06:31  2.26-b09
2017-07-12 09:02  2.26-b08
2017-06-30 14:01  2.26-b07
2017-06-15 13:28  2.26-b06
2017-06-09 21:39  2.26-b05
2017-05-19 08:17  2.26-b04
2017-03-13 12:43  2.26-b03
2017-01-31 23:58  2.26-b02
2017-01-19 17:16  2.25.1
2017-01-13 20:25  2.26-b01
2016-12-08 13:50  2.25
2016-11-30 12:34  2.22.4
2016-11-21 17:43  2.24.1
2016-10-27 15:37  2.24
2016-10-26 07:43  2.22.3
2016-08-08 18:01  2.23.2
2016-06-09 19:51  2.23.1
2016-05-18 08:49  2.23
2016-02-16 12:29  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.containers:jersey-container-servlet  2.22.2
   - a level 3 dependencies among 2 (possibly transitive) uses
2017-09-05 10:20  2.26
2017-07-27 06:37  2.26-b09
2017-07-12 09:25  2.26-b08
2017-06-30 14:11  2.26-b07
2017-06-15 13:40  2.26-b06
2017-06-09 21:38  2.26-b05
2017-05-19 08:12  2.26-b04
2017-03-13 12:50  2.26-b03
2017-02-01 00:14  2.26-b02
2017-01-19 17:09  2.25.1
2017-01-13 20:19  2.26-b01
2016-12-08 14:00  2.25
2016-11-30 12:35  2.22.4
2016-11-21 17:46  2.24.1
2016-10-27 15:52  2.24
2016-10-26 07:44  2.22.3
2016-08-08 18:22  2.23.2
2016-06-09 19:17  2.23.1
2016-05-18 08:50  2.23
2016-02-16 12:30  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.core:jersey-client  2.22.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-09-05 10:19  2.26
2017-07-27 06:31  2.26-b09
2017-07-12 09:18  2.26-b08
2017-06-30 14:10  2.26-b07
2017-06-15 13:16  2.26-b06
2017-06-09 21:44  2.26-b05
2017-05-19 08:18  2.26-b04
2017-03-13 12:35  2.26-b03
2017-01-31 23:43  2.26-b02
2017-01-19 17:21  2.25.1
2017-01-13 20:35  2.26-b01
2016-12-08 13:53  2.25
2016-11-30 12:33  2.22.4
2016-11-21 17:41  2.24.1
2016-10-27 15:55  2.24
2016-10-26 07:42  2.22.3
2016-08-08 18:24  2.23.2
2016-06-09 19:38  2.23.1
2016-05-18 08:46  2.23
2016-02-16 12:28  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.core:jersey-common  2.22.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-09-05 10:15  2.26
2017-07-27 06:39  2.26-b09
2017-07-12 09:24  2.26-b08
2017-06-30 14:19  2.26-b07
2017-06-15 13:25  2.26-b06
2017-06-09 21:45  2.26-b05
2017-05-19 08:26  2.26-b04
2017-03-13 12:42  2.26-b03
2017-02-01 00:13  2.26-b02
2017-01-19 17:30  2.25.1
2017-01-13 20:31  2.26-b01
2016-12-08 13:36  2.25
2016-11-30 12:32  2.22.4
2016-11-21 17:51  2.24.1
2016-10-27 15:44  2.24
2016-10-26 07:41  2.22.3
2016-08-08 18:25  2.23.2
2016-06-09 19:38  2.23.1
2016-05-18 08:45  2.23
2016-02-16 12:28  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.core:jersey-server  2.22.2
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-09-05 10:14  2.26
2017-07-27 06:37  2.26-b09
2017-07-12 09:06  2.26-b08
2017-06-30 14:09  2.26-b07
2017-06-15 13:11  2.26-b06
2017-06-09 21:43  2.26-b05
2017-05-19 08:14  2.26-b04
2017-03-13 12:33  2.26-b03
2017-02-01 00:04  2.26-b02
2017-01-19 17:17  2.25.1
2017-01-13 20:24  2.26-b01
2016-12-08 13:32  2.25
2016-11-30 12:34  2.22.4
2016-11-21 17:38  2.24.1
2016-10-27 15:42  2.24
2016-10-26 07:43  2.22.3
2016-08-08 18:02  2.23.2
2016-06-09 19:10  2.23.1
2016-05-18 08:48  2.23
2016-02-16 12:29  2.22.2 ***

========================================================================
Presently in use: org.glassfish.jersey.media:jersey-media-jaxb  2.22.2
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-09-05 10:14  2.26
2017-07-27 06:33  2.26-b09
2017-07-12 09:14  2.26-b08
2017-06-30 14:28  2.26-b07
2017-06-15 13:20  2.26-b06
2017-06-09 21:41  2.26-b05
2017-05-19 08:28  2.26-b04
2017-03-13 13:03  2.26-b03
2017-01-31 23:50  2.26-b02
2017-01-19 17:20  2.25.1
2017-01-13 20:29  2.26-b01
2016-12-08 13:40  2.25
2016-11-30 12:33  2.22.4
2016-11-21 17:26  2.24.1
2016-10-27 15:28  2.24
2016-10-26 07:42  2.22.3
2016-08-08 18:20  2.23.2
2016-06-09 19:30  2.23.1
2016-05-18 08:47  2.23
2016-02-16 12:28  2.22.2 ***

========================================================================
Presently in use: org.glassfish:javax.json  1.0.4
   - a level 2 dependencies among 1 (possibly transitive) uses
2017-11-02 18:57  1.1.2
2017-05-18 22:43  1.1
2017-03-10 16:05  1.1.0-M2
2017-01-27 18:17  1.1.0-M1
2013-11-18 19:53  1.0.4 ***

========================================================================
Presently in use: org.hamcrest:hamcrest-core  1.3
   - a level 2 dependencies among 1 (possibly transitive) uses
2012-07-09 21:08  1.3 ***

========================================================================
Presently in use: org.javassist:javassist  3.18.1-GA
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-10-10 18:05  3.22.0-GA
2017-06-06 13:02  3.22.0-CR2
2016-10-04 16:29  3.22.0-CR1
2016-10-03 16:45  3.21.0-GA
2015-06-25 12:09  3.20.0-GA
2015-01-07 03:05  3.19.0-GA
2014-05-27 16:55  3.18.2-GA
2013-08-30 16:59  3.18.1-GA ***

========================================================================
Presently in use: org.jetbrains.kotlin:kotlin-stdlib  1.2.10
   - a level 2 dependencies among 1 (possibly transitive) uses
2018-01-23 12:59  1.2.21
2018-01-16 18:21  1.2.20
2017-12-13 14:55  1.2.10 ***

========================================================================
Presently in use: org.jetbrains:annotations  13.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2015-10-15 08:56  15.0
2013-12-17 12:10  13.0 ***

========================================================================
Presently in use: org.json4s:json4s-ast_2.11  3.2.11
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-11-30 13:34  3.6.0-M2
2017-10-13 15:12  3.6.0-M1
2017-07-29 00:08  3.5.3
2017-05-04 20:28  3.5.2
2017-03-18 04:17  3.5.1
2016-11-04 14:25  3.5.0
2016-11-02 16:18  3.5.0.RC1
2016-10-18 16:37  3.4.2
2016-09-22 13:52  3.4.1
2016-06-18 16:06  3.4.0
2015-11-22 02:43  4.0.0-M1
2015-10-03 13:06  3.3.0
2015-09-20 05:42  3.3.0.RC6
2015-09-14 11:59  3.3.0.RC5
2015-09-05 01:24  3.3.0.RC4
2015-07-14 12:56  3.3.0.RC3
2015-05-16 02:05  3.3.0.RC2
2015-04-13 14:49  3.3.0.RC1
2014-10-24 01:10  3.2.11 ***

========================================================================
Presently in use: org.json4s:json4s-core_2.11  3.2.11
   - a level 4 dependencies among 1 (possibly transitive) uses
2017-11-30 13:36  3.6.0-M2
2017-10-13 15:13  3.6.0-M1
2017-07-29 00:08  3.5.3
2017-05-04 20:28  3.5.2
2017-03-18 04:17  3.5.1
2016-11-04 14:26  3.5.0
2016-11-02 16:20  3.5.0.RC1
2016-10-18 16:38  3.4.2
2016-09-22 13:54  3.4.1
2016-06-18 16:06  3.4.0
2015-10-03 13:07  3.3.0
2015-09-20 05:44  3.3.0.RC6
2015-09-14 12:04  3.3.0.RC5
2015-09-05 01:25  3.3.0.RC4
2015-07-14 12:57  3.3.0.RC3
2015-05-16 02:06  3.3.0.RC2
2015-04-13 14:50  3.3.0.RC1
2014-10-24 01:10  3.2.11 ***

========================================================================
Presently in use: org.json4s:json4s-jackson_2.11  3.2.11
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-11-30 13:38  3.6.0-M2
2017-10-13 15:12  3.6.0-M1
2017-07-29 00:07  3.5.3
2017-05-04 20:27  3.5.2
2017-03-18 04:17  3.5.1
2016-11-04 14:25  3.5.0
2016-11-02 16:19  3.5.0.RC1
2016-10-18 16:38  3.4.2
2016-09-22 13:53  3.4.1
2016-06-18 16:06  3.4.0
2015-10-03 13:07  3.3.0
2015-09-20 05:43  3.3.0.RC6
2015-09-14 12:01  3.3.0.RC5
2015-09-05 01:24  3.3.0.RC4
2015-07-14 12:57  3.3.0.RC3
2015-05-16 02:06  3.3.0.RC2
2015-04-13 14:50  3.3.0.RC1
2014-10-24 01:11  3.2.11 ***

========================================================================
Presently in use: org.json:json  20171018
   - a level 1 dependencies among 1 (possibly transitive) uses
2018-02-03 21:40  20180130
2017-10-19 19:31  20171018 ***

========================================================================
Presently in use: org.mortbay.jetty:jetty-util  6.1.26
   - a level 5 dependencies among 1 (possibly transitive) uses
2010-11-10 21:38  6.1.26 ***

========================================================================
Presently in use: org.objenesis:objenesis  2.1
   - a level 5 dependencies among 1 (possibly transitive) uses
2017-06-20 15:28  2.6
2017-01-18 02:01  2.5.1
2017-01-13 04:40  2.5
2016-05-23 05:26  2.4
2016-05-10 04:21  2.3
2015-08-12 14:35  2.2
2013-10-10 21:25  2.1 ***

========================================================================
Presently in use: org.python:jython  2.7.0
   - a level 1 dependencies among 1 (possibly transitive) uses
2016-02-03 04:18  2.7.1b3
2015-10-12 03:59  2.7.1b2
2015-09-11 01:58  2.7.1b1
2015-04-29 03:12  2.7.0 ***

========================================================================
Presently in use: org.rauschig:jarchivelib  0.5.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2015-04-15 13:17  0.7.1
2014-12-02 18:25  0.7.0
2014-11-14 21:04  0.6.2
2014-10-20 19:40  0.6.1
2014-04-09 14:48  0.6.0
2014-03-03 14:51  0.5.0 ***

========================================================================
Presently in use: org.roaringbitmap:RoaringBitmap  0.5.11
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-02-01 19:00  0.7.0
2017-12-23 18:07  0.6.66
2017-12-23 03:05  0.6.65
2017-12-23 02:38  0.6.63
2017-12-19 02:09  0.6.59
2017-12-19 01:44  0.6.58
2017-12-13 00:23  0.6.53
2017-08-29 17:41  0.6.51
2017-08-21 22:20  0.6.50
2017-08-19 12:12  0.6.49
2017-08-14 23:05  0.6.48
2017-08-08 20:12  0.6.47
2017-07-07 18:58  0.6.46
2017-07-03 15:36  0.6.45
2017-05-08 14:03  0.6.44
2017-04-14 14:51  0.6.43
2017-04-08 00:53  0.6.42
2017-03-23 19:45  0.6.41
2017-03-20 20:58  0.6.40
2017-03-07 16:34  0.6.39
2017-03-07 14:02  0.6.38
2017-02-20 16:25  0.6.37
2017-02-17 16:25  0.6.36
2017-01-30 23:21  0.6.35
2017-01-18 23:14  0.6.34
2017-01-05 16:08  0.6.32
2017-01-03 19:51  0.6.31
2016-12-19 14:22  0.6.29
2016-12-07 03:15  0.6.28
2016-09-26 17:02  0.6.27
2016-09-09 14:33  0.6.26
2016-08-30 19:32  0.6.25
2016-08-22 17:26  0.6.24
2016-08-11 19:34  0.6.23
2016-08-10 21:39  0.6.22
2016-07-29 19:59  0.6.21
2016-07-21 23:07  0.6.20
2016-07-21 22:16  0.6.19
2016-05-16 13:32  0.6.18
2016-05-06 03:17  0.6.17
2016-05-03 19:28  0.6.16
2016-04-24 21:20  0.6.15
2016-04-04 22:16  0.6.14
2016-04-04 21:39  0.6.13
2016-04-03 18:57  0.6.12
2016-03-26 23:16  0.6.11
2016-03-24 19:03  0.6.10
2016-03-21 22:03  0.6.9
2016-03-21 20:11  0.6.8
2016-03-19 23:29  0.6.7
2016-03-03 19:32  0.6.5
2016-03-02 22:29  0.6.4
2016-02-17 01:26  0.5.21
2016-02-17 01:16  0.6.3
2016-02-13 18:07  0.6.2
2016-02-07 23:20  0.6.1
2016-02-05 15:09  0.6.0
2016-01-29 17:09  0.5.20
2016-01-28 14:03  0.5.19
2016-01-21 18:08  0.5.18
2016-01-18 16:21  0.5.17
2016-01-05 03:10  0.5.16
2015-12-25 18:51  0.5.15
2015-12-24 19:27  0.5.14
2015-11-26 16:26  0.5.13
2015-11-25 15:09  0.5.12
2015-11-17 00:35  0.5.11 ***

========================================================================
Presently in use: org.scala-lang.modules:scala-parser-combinators_2.11  1.0.1
   - a level 7 dependencies among 1 (possibly transitive) uses
2018-02-01 21:09  1.1.0
2018-01-31 16:51  1.0.7
2017-05-02 13:27  1.0.6
2016-12-16 19:59  1.0.5
2014-12-15 00:21  1.0.3
2014-07-23 06:45  1.0.2
2014-04-16 09:22  1.0.1 ***

========================================================================
Presently in use: org.scala-lang.modules:scala-xml_2.11  1.0.1
   - a level 7 dependencies among 1 (possibly transitive) uses
2016-09-20 09:26  1.0.6
2015-07-24 19:12  1.0.5
2014-12-04 20:18  1.0.3
2014-05-20 08:10  1.0.2
2014-04-16 09:21  1.0.1 ***

========================================================================
Presently in use: org.scala-lang:scala-compiler  2.11.0
   - a level 6 dependencies among 1 (possibly transitive) uses
2018-01-31 04:20  2.13.0-M3
2017-11-03 20:07  2.10.7
2017-11-03 01:37  2.11.12
2017-10-11 07:40  2.12.4
2017-07-25 10:45  2.12.3
2017-07-21 12:50  2.13.0-M2
2017-04-14 06:18  2.13.0-M1
2017-04-13 19:50  2.11.11
2017-04-13 08:20  2.12.2
2017-04-05 17:22  2.11.10
2017-03-28 07:15  2.11.9
2017-01-05 21:03  2.11.8-18269ea
2016-12-05 11:10  2.12.1
2016-10-28 23:09  2.12.0
2016-10-13 05:47  2.12.0-RC1-1e81a09
2016-09-27 07:51  2.12.0-RC1-ceaf419
2016-09-16 08:30  2.12.0-RC1-be43eb5
2016-06-29 10:47  2.12.0-M5
2016-06-28 19:47  2.12.0-M4-9901daf
2016-04-01 21:46  2.12.0-M4
2016-03-18 05:23  2.12.0-M3-dc9effe
2016-03-04 15:26  2.11.8
2015-10-05 14:26  2.12.0-M3
2015-09-18 09:35  2.10.6
2015-07-14 14:32  2.12.0-M2
2015-06-22 20:18  2.11.7
2015-05-01 16:28  2.12.0-M1
2015-02-27 01:54  2.10.5
2015-02-26 01:01  2.11.6
2015-01-07 00:32  2.11.5
2014-10-23 15:35  2.11.4
2014-10-10 17:34  2.11.3
2014-07-23 06:39  2.11.2
2014-05-20 08:03  2.11.1
2014-04-16 09:14  2.11.0 ***

========================================================================
Presently in use: org.scala-lang:scala-library  2.11.8
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-31 04:19  2.13.0-M3
2017-11-03 20:06  2.10.7
2017-11-03 01:37  2.11.12
2017-10-11 07:04  2.12.4
2017-07-25 10:47  2.12.3
2017-07-21 12:49  2.13.0-M2
2017-04-14 06:18  2.13.0-M1
2017-04-13 19:50  2.11.11
2017-04-13 08:19  2.12.2
2017-04-05 17:21  2.11.10
2017-03-28 07:15  2.11.9
2017-01-05 21:02  2.11.8-18269ea
2016-12-05 11:09  2.12.1
2016-10-28 23:07  2.12.0
2016-10-13 05:46  2.12.0-RC1-1e81a09
2016-09-27 07:49  2.12.0-RC1-ceaf419
2016-09-16 08:28  2.12.0-RC1-be43eb5
2016-06-29 10:46  2.12.0-M5
2016-06-28 19:47  2.12.0-M4-9901daf
2016-04-01 21:46  2.12.0-M4
2016-03-18 05:23  2.12.0-M3-dc9effe
2016-03-04 15:26  2.11.8 ***

========================================================================
Presently in use: org.scala-lang:scala-reflect  2.11.8
   - a level 3 dependencies among 1 (possibly transitive) uses
2018-01-31 04:17  2.13.0-M3
2017-11-03 20:07  2.10.7
2017-11-03 01:37  2.11.12
2017-10-11 07:22  2.12.4
2017-07-25 10:44  2.12.3
2017-07-21 12:47  2.13.0-M2
2017-04-14 06:14  2.13.0-M1
2017-04-13 19:50  2.11.11
2017-04-13 08:18  2.12.2
2017-04-05 17:22  2.11.10
2017-03-28 07:15  2.11.9
2017-01-05 21:03  2.11.8-18269ea
2016-12-05 11:06  2.12.1
2016-10-28 23:04  2.12.0
2016-10-13 05:43  2.12.0-RC1-1e81a09
2016-09-27 07:47  2.12.0-RC1-ceaf419
2016-09-16 08:26  2.12.0-RC1-be43eb5
2016-06-29 10:47  2.12.0-M5
2016-06-28 19:47  2.12.0-M4-9901daf
2016-04-01 21:46  2.12.0-M4
2016-03-18 05:23  2.12.0-M3-dc9effe
2016-03-04 15:26  2.11.8 ***

========================================================================
Presently in use: org.scala-lang:scalap  2.11.0
   - a level 5 dependencies among 1 (possibly transitive) uses
2018-01-31 04:19  2.13.0-M3
2017-11-03 20:07  2.10.7
2017-11-03 01:37  2.11.12
2017-10-11 07:30  2.12.4
2017-07-25 10:47  2.12.3
2017-07-21 12:50  2.13.0-M2
2017-04-14 06:18  2.13.0-M1
2017-04-13 19:51  2.11.11
2017-04-13 08:19  2.12.2
2017-04-05 17:22  2.11.10
2017-03-28 07:15  2.11.9
2017-01-05 21:03  2.11.8-18269ea
2016-12-05 11:09  2.12.1
2016-10-28 23:07  2.12.0
2016-10-13 05:46  2.12.0-RC1-1e81a09
2016-09-27 07:49  2.12.0-RC1-ceaf419
2016-09-16 08:29  2.12.0-RC1-be43eb5
2016-06-29 10:47  2.12.0-M5
2016-06-28 19:47  2.12.0-M4-9901daf
2016-04-01 21:47  2.12.0-M4
2016-03-18 05:23  2.12.0-M3-dc9effe
2016-03-04 15:26  2.11.8
2015-10-05 14:26  2.12.0-M3
2015-09-18 09:36  2.10.6
2015-07-14 14:32  2.12.0-M2
2015-06-22 20:18  2.11.7
2015-05-01 16:28  2.12.0-M1
2015-02-27 01:55  2.10.5
2015-02-26 01:01  2.11.6
2015-01-07 00:32  2.11.5
2014-10-23 15:35  2.11.4
2014-10-10 17:34  2.11.3
2014-07-23 06:39  2.11.2
2014-05-20 08:03  2.11.1
2014-04-16 09:14  2.11.0 ***

========================================================================
Presently in use: org.slf4j:jcl-over-slf4j  1.7.16
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-03-16 16:37  1.7.25
2017-02-24 11:06  1.7.24
2017-02-14 22:32  1.7.23
2016-12-13 17:06  1.7.22
2016-04-04 18:38  1.7.21
2016-03-29 15:13  1.7.20
2016-03-14 21:35  1.7.19
2016-02-26 18:52  1.7.18
2016-02-11 20:27  1.7.16 ***

========================================================================
Presently in use: org.slf4j:jul-to-slf4j  1.7.16
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-03-16 16:37  1.7.25
2017-02-24 11:06  1.7.24
2017-02-14 22:32  1.7.23
2016-12-13 17:06  1.7.22
2016-04-04 18:39  1.7.21
2016-03-29 15:13  1.7.20
2016-03-14 21:35  1.7.19
2016-02-26 18:53  1.7.18
2016-02-11 20:27  1.7.16 ***

========================================================================
Presently in use: org.slf4j:slf4j-api  1.7.12
   - a level 2 dependencies among 3 (possibly transitive) uses
2017-03-16 16:36  1.7.25
2017-02-24 11:05  1.7.24
2017-02-14 22:31  1.7.23
2016-12-13 17:05  1.7.22
2016-04-04 18:36  1.7.21
2016-03-29 15:12  1.7.20
2016-03-14 21:34  1.7.19
2016-02-26 18:51  1.7.18
2016-02-11 20:26  1.7.16
2016-02-09 16:29  1.7.15
2016-01-24 20:47  1.7.14
2015-11-10 20:14  1.7.13
2015-03-26 20:50  1.7.12 ***

========================================================================
Presently in use: org.slf4j:slf4j-api  1.7.16
   - a level 5 dependencies among 3 (possibly transitive) uses
2017-03-16 16:36  1.7.25
2017-02-24 11:05  1.7.24
2017-02-14 22:31  1.7.23
2016-12-13 17:05  1.7.22
2016-04-04 18:36  1.7.21
2016-03-29 15:12  1.7.20
2016-03-14 21:34  1.7.19
2016-02-26 18:51  1.7.18
2016-02-11 20:26  1.7.16 ***

========================================================================
Presently in use: org.slf4j:slf4j-api  1.7.21
   - a level 5 dependencies among 3 (possibly transitive) uses
2017-03-16 16:36  1.7.25
2017-02-24 11:05  1.7.24
2017-02-14 22:31  1.7.23
2016-12-13 17:05  1.7.22
2016-04-04 18:36  1.7.21 ***

========================================================================
Presently in use: org.slf4j:slf4j-log4j12  1.7.16
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-03-16 16:37  1.7.25
2017-02-24 11:05  1.7.24
2017-02-14 22:32  1.7.23
2016-12-13 17:05  1.7.22
2016-04-04 18:37  1.7.21
2016-03-29 15:12  1.7.20
2016-03-14 21:34  1.7.19
2016-02-26 18:52  1.7.18
2016-02-11 20:26  1.7.16 ***

========================================================================
Presently in use: org.slf4j:slf4j-simple  1.7.21
   - a level 1 dependencies among 1 (possibly transitive) uses
2017-03-16 16:36  1.7.25
2017-02-24 11:05  1.7.24
2017-02-14 22:31  1.7.23
2016-12-13 17:05  1.7.22
2016-04-04 18:36  1.7.21 ***

========================================================================
Presently in use: org.spark-project.spark:unused  1.0.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2014-10-22 07:00  1.0.0 ***

========================================================================
Presently in use: org.tukaani:xz  1.0
   - a level 6 dependencies among 2 (possibly transitive) uses
2018-01-04 16:09  1.8
2017-12-29 16:36  1.7
2016-11-27 11:38  1.6
2014-03-08 11:39  1.5
2013-09-22 10:14  1.4
2013-05-12 18:06  1.3
2013-01-29 14:27  1.2
2012-07-05 06:07  1.1
2011-10-22 09:44  1.0 ***

========================================================================
Presently in use: org.tukaani:xz  1.4
   - a level 9 dependencies among 2 (possibly transitive) uses
2018-01-04 16:09  1.8
2017-12-29 16:36  1.7
2016-11-27 11:38  1.6
2014-03-08 11:39  1.5
2013-09-22 10:14  1.4 ***

========================================================================
Presently in use: org.twitter4j:twitter4j-core  4.0.1
   - a level 2 dependencies among 1 (possibly transitive) uses
2016-12-25 12:57  4.0.6
2016-09-13 17:10  4.0.5
2015-03-28 15:40  4.0.3
2014-06-24 14:41  4.0.2
2014-03-18 17:04  4.0.1 ***

========================================================================
Presently in use: org.twitter4j:twitter4j-stream  4.0.1
   - a level 2 dependencies among 1 (possibly transitive) uses
2016-12-25 12:58  4.0.6
2016-09-13 17:11  4.0.5
2015-03-28 15:42  4.0.3
2014-06-24 14:43  4.0.2
2014-03-18 17:07  4.0.1 ***

========================================================================
Presently in use: org.xerial.snappy:snappy-java  1.1.2.6
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-12-07 19:51  1.1.7.1
2017-12-01 01:00  1.1.7
2017-05-22 16:05  1.1.4
2017-02-16 18:19  1.1.4-M3
2017-02-13 19:46  1.1.4-M2
2017-02-11 01:07  1.1.4-M1
2017-01-26 06:47  1.1.3-M2
2017-01-20 15:28  1.1.3-M1
2016-06-02 17:49  1.1.2.6 ***

========================================================================
Presently in use: org.yaml:snakeyaml  1.17
   - a level 3 dependencies among 1 (possibly transitive) uses
2017-10-14 11:45  1.19
2017-02-22 13:18  1.18
2016-02-19 13:13  1.17 ***

========================================================================
Presently in use: oro:oro  2.0.8
   - a level 3 dependencies among 1 (possibly transitive) uses
2005-09-20 05:50  2.0.8 ***

========================================================================
Presently in use: xalan:xalan  2.7.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2014-07-24 18:48  2.7.2
2005-09-20 05:52  2.7.0 ***

========================================================================
Presently in use: xerces:xercesImpl  2.8.0
   - a level 3 dependencies among 1 (possibly transitive) uses
2013-02-20 20:20  2.11.0
2011-08-15 22:32  2.10.0
2010-05-20 08:54  2.6.2-jaxb-1.0.6
2008-10-01 22:19  2.9.1
2008-10-01 22:19  2.9.0
2006-10-07 12:02  2.8.1
2006-04-10 20:32  2.8.0 ***

========================================================================
Presently in use: xml-apis:xml-apis  1.3.03
   - a level 3 dependencies among 1 (possibly transitive) uses
2011-08-20 00:11  1.4.01
2010-02-03 21:05  1.2.01
2006-12-22 13:37  1.3.04
2006-04-10 20:32  1.3.03 ***

========================================================================
Presently in use: xmlenc:xmlenc  0.52
   - a level 5 dependencies among 1 (possibly transitive) uses
2005-09-20 05:53  0.33
2005-09-20 05:53  0.20
unknown-date unknown:time  0.52 ***

```
