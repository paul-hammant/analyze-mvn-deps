# analyze-deps: An alternative Maven dependency analyzer.

A Bash script to analyze Maven dependency upgrade opportunities.

It is an alternative to [maven-dependency-plugin](https://maven.apache.org/plugins/maven-dependency-plugin/) and [versions-maven-plugin](http://www.mojohaus.org/versions-maven-plugin/) (and maybe others) that are written in Java.

## Running it

First `cd` to your clone/checkout (where the room pom.xml is) and

```
$ bash <(curl -s https://raw.githubusercontent.com/paul-hammant/analyze-deps/master/analyze-deps.sh)
```
That works on Mac, and might work on Linux too - lemme know. Oh and I just wanted to see how far I could get in shell script alone wthout resprting to Python and Java (like the existing plugins for this).

## The results from runnng the script

After running the script, peer inside the `.deps/` folder and look at the generated files:

* big-dependency-report.txt
* dependencies-tree.txt		
* flattened-unique-gavs.txt
* immediate-upgrade-opportunities.txt
* mvn-dep-tree-output.txt

They can all be checked in if you want. If you do so, you get to watch a moving target (using Git diff or show) each time you run the analyze-deps script. Meaning, you were in step with other projects releases yesterday, but today you are not.

I think the `immediate-upgrade-opportunities.txt` and `dependencies-tree.txt`	files are the most useful ones. At least ones that you'd use to guide you towards which dependency to upgrade first (or harass other dev teams).  Others might take the view that `big-dependency-report.txt` is more useful.

## Glitches

1. If the dependency tree has two versions of the same group:artifact and there is some independence in the complete DAG between those two branches, then the item can be listed twice and/or marked for upgrade when none is necessary. You can see that with `log4j` (jar) which is marked as `1.2.12` in one branch and `1.2.17` in another. Anyway, the confusion means that right at the top, version `1.2.17` is marked as  eligible to upgrade to version `1.2.17` - doh!. Your eyeballs will scan past that quickly as a red herring.

2. Related a group:artifact may be in the larger graph twice. Once as 'jar' and once as something else, causing an erroneous marking for upgrade.

3. Qualifiers are not well catered for. See `org.apache.avro:avro-mapred:jar:hadoop2:1.7.7:compile` above (hadoop2 being the qualifier).

4. Where a team releases (say) `4.1.3` and then backports the fix of a bug to (say) `3.9.5` the latter might have a more recent timestamp and be deemed more recent than the former - causing an erroneous upgrade suggestion.

5. The script is only checking the 'maven central' repository. So Gradle's at https://repo.gradle.org/gradle/libs-releases-local/ is not checked

## Examples of output for the excellent Hazelcast [github.com/hazelcast/hazelcast-jet-demos](https://github.com/hazelcast/hazelcast-jet-demos)

Lines that end in `> N.n.n` are a suggested version upgrade (notwisthanding the glitches mentioned above)

### The dependency-tree.txt file

```
--- demos ---
--- cryptocurrency-realtime-trend ---
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 edu.stanford.nlp:stanford-corenlp:jar:3.8.0:compile  > 3.8.0
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
   xalan:xalan:jar:2.7.0:compile  > 2.7.2
  joda-time:joda-time:jar:2.9.4:compile  > 2.9.9
  com.googlecode.efficient-java-matrix-library:ejml:jar:0.23:compile  > 0.25
  org.glassfish:javax.json:jar:1.0.4:compile  > 1.1.2
  org.slf4j:slf4j-api:jar:1.7.12:compile  > 1.7.25
  com.google.protobuf:protobuf-java:jar:3.2.0:compile  > 3.5.1
 edu.stanford.nlp:stanford-corenlp:jar:models:3.8.0:compile  > 3.8.0
 edu.stanford.nlp:stanford-corenlp:jar:models-english:3.8.0:compile  > 3.8.0
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
 org.json:json:jar:20171018:compile
--- flight-telemetry ---
 org.python:jython:jar:2.7.0:compile  > 2.7.1b3
 log4j:log4j:jar:1.2.12:compile  > 1.2.17
--- realtime-image-recognition ---
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
  org.boofcv:boofcv-swing:jar:0.28:compile
  com.github.sarxos:webcam-capture:jar:0.3.12:compile
   com.nativelibs4java:bridj:jar:0.7.0:compile
--- jetleopard ---
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
 log4j:log4j:jar:1.2.17:compile  > 1.2.17
 com.google.code.findbugs:annotations:jar:3.0.0:provided  > 3.0.1u2
--- online-training-traffic-predictor ---
  com.hazelcast:hazelcast-client:jar:3.9:compile  > 3.9.2
   com.hazelcast:hazelcast:jar:3.9:compile  > 3.9.2
```

### The immediate-upgrade-opportunities.txt file

```
com.fasterxml.jackson.core:jackson-core:jar:2.8.8:compile  > 2.9.4
com.fasterxml.jackson.core:jackson-databind:jar:2.8.8:compile  > 2.9.4
com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.8.8:compile  > 2.9.4
com.google.code.findbugs:annotations:jar:3.0.0:provided  > 3.0.1u2
```

These are the pending upgrades that are directly within the control of the HazelCast dev team. All others 
are responsibilities outside this team, and the HazelCast team could raise issues or pull-requests with 
other teams if they felt it was that important.

### The big-dependency-report.txt file

```
========================================================================
Presently in use: aopalliance:aopalliance  1.0
 - a level 8 dependency among 1 (possibly transitive) uses

2005-09-20 05:45  1.0 ***

========================================================================
Presently in use: com.apple:AppleJavaExtensions  1.4
 - a level 2 dependency among 1 (possibly transitive) uses

2010-10-22 13:57  1.4 ***

========================================================================
Presently in use: com.clearspring.analytics:stream  2.7.0
 - a level 3 dependency among 1 (possibly transitive) uses

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
 - a level 4 dependency among 1 (possibly transitive) uses

2017-07-23 22:02  4.0.1
2016-07-05 23:27  4.0.0
2015-07-26 21:47  3.0.3 ***

========================================================================
Presently in use: com.esotericsoftware:minlog  1.3.0
 - a level 5 dependency among 1 (possibly transitive) uses

2013-11-14 21:31  1.3
2013-11-14 20:46  1.3-SNAPHOT
unknown-date unknown:time  minlog
unknown-date unknown:time  1.3.0 ***

========================================================================
Presently in use: com.fasterxml.jackson.core:jackson-annotations  2.8.0
 - a level 2 dependency among 1 (possibly transitive) uses

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
 - a level 1 dependency among 1 (possibly transitive) uses

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
 - a level 1 dependency among 1 (possibly transitive) uses

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
 - a level 1 dependency among 1 (possibly transitive) uses

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
 - a level 3 dependency among 1 (possibly transitive) uses

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
 - a level 2 dependency among 1 (possibly transitive) uses

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
 - a level 2 dependency among 1 (possibly transitive) uses

2018-01-17 19:22  0.3.12 ***

========================================================================
Presently in use: com.google.code.findbugs:annotations  3.0.0
 - a level 1 dependency among 1 (possibly transitive) uses

2015-10-09 06:11  3.0.1u2
2015-10-09 06:05  3.0.1u1
2015-10-09 05:46  3.0.1
2014-07-10 11:56  3.0.0 ***

========================================================================
Presently in use: com.google.code.findbugs:jsr305  1.3.9
 - a level 3 dependency among 2 (possibly transitive) uses

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
 - a level 2 dependency among 2 (possibly transitive) uses

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
 - a level 7 dependency among 1 (possibly transitive) uses

2016-06-17 19:53  4.1.0
2015-04-28 20:33  4.0
2011-03-25 18:19  3.0 ***

========================================================================
Presently in use: com.google.protobuf:protobuf-java  2.5.0
 - a level 2 dependency among 3 (possibly transitive) uses

2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0
2017-01-19 00:55  3.2.0rc2
2017-01-13 23:03  3.2.0-rc.1
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
 - a level 5 dependency among 3 (possibly transitive) uses

2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0
2017-01-19 00:55  3.2.0rc2
2017-01-13 23:03  3.2.0-rc.1
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
 - a level 5 dependency among 3 (possibly transitive) uses

2017-12-21 20:09  3.5.1
2017-11-13 22:34  3.5.0
2017-08-15 22:07  3.4.0
2017-05-15 17:46  3.3.1
2017-05-01 22:52  3.3.0
2017-01-28 02:33  3.2.0 ***

========================================================================
Presently in use: com.googlecode.efficient-java-matrix-library:ejml  0.23
 - a level 2 dependency among 1 (possibly transitive) uses

2014-06-13 04:42  0.25
2013-12-27 02:15  0.24
2013-06-21 16:16  0.23 ***

========================================================================
Presently in use: com.hazelcast.jet.demos:cryptocurrency-realtime-trend  0.1-SNAPSHOT
```

### The flattened-unique-gavs.txt file

```
aopalliance:aopalliance:jar:1.0
com.apple:AppleJavaExtensions:jar:1.4
com.clearspring.analytics:stream:jar:2.7.0
com.esotericsoftware:kryo-shaded:jar:3.0.3
com.esotericsoftware:minlog:jar:1.3.0
com.fasterxml.jackson.core:jackson-annotations:jar:2.8.0
com.fasterxml.jackson.core:jackson-core:jar:2.8.8
com.fasterxml.jackson.core:jackson-databind:jar:2.8.8
com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.8.8
com.fasterxml.jackson.module:jackson-module-paranamer:jar:2.8.8
com.fasterxml.jackson.module:jackson-module-scala_2.11:jar:2.8.8
com.github.sarxos:webcam-capture:jar:0.3.12
com.google.code.findbugs:annotations:jar:3.0.0
com.google.code.findbugs:jsr305:jar:1.3.9
com.google.guava:guava:jar:14.0.1
com.google.inject:guice:jar:3.0
com.google.protobuf:protobuf-java:jar:2.5.0
com.google.protobuf:protobuf-java:jar:2.6.1
com.google.protobuf:protobuf-java:jar:3.2.0
com.googlecode.efficient-java-matrix-library:ejml:jar:0.23
com.hazelcast.jet.demos:cryptocurrency-realtime-trend:jar:0.1-SNAPSHOT
com.hazelcast.jet.demos:demos:pom:0.1-SNAPSHOT
com.hazelcast.jet.demos:flight-telemetry:jar:0.1-SNAPSHOT
com.hazelcast.jet.demos:jetleopard:jar:1.0.0-SNAPSHOT
com.hazelcast.jet.demos:markov-chain-generator:jar:0.1-SNAPSHOT
com.hazelcast.jet.demos:online-training-traffic-predictor:jar:0.1-SNAPSHOT
com.hazelcast.jet.demos:realtime-image-recognition:jar:1.0-SNAPSHOT
com.hazelcast.jet:hazelcast-jet-client-protocol:jar:0.6-SNAPSHOT
com.hazelcast.jet:hazelcast-jet-core:jar:0.6-SNAPSHOT
com.hazelcast.jet:hazelcast-jet:jar:0.5
com.hazelcast.jet:hazelcast-jet:jar:0.6-SNAPSHOT
com.hazelcast:hazelcast-client:jar:3.9
com.hazelcast:hazelcast-spark:jar:0.2
com.hazelcast:hazelcast:jar:3.9
com.io7m.xom:xom:jar:1.2.10
com.nativelibs4java:bridj:jar:0.7.0
com.ning:compress-lzf:jar:1.0.3
com.squareup.okhttp3:okhttp:jar:3.9.1
com.squareup.okio:okio:jar:1.13.0
com.thoughtworks.paranamer:paranamer:jar:2.8
com.twitter:chill-java:jar:0.8.0
com.twitter:chill_2.11:jar:0.8.0
com.twitter:hbc-core:jar:2.2.0
com.twitter:hbc-twitter4j:jar:2.2.0
com.twitter:joauth:jar:6.0.2
com:betleopard:jar:1.1.0
commons-beanutils:commons-beanutils-core:jar:1.8.0
commons-beanutils:commons-beanutils:jar:1.7.0
commons-cli:commons-cli:jar:1.2
commons-codec:commons-codec:jar:1.3
commons-codec:commons-codec:jar:1.6
commons-collections:commons-collections:jar:3.2.1
commons-configuration:commons-configuration:jar:1.6
commons-digester:commons-digester:jar:1.8
commons-httpclient:commons-httpclient:jar:3.1
commons-io:commons-io:jar:2.1
commons-lang:commons-lang:jar:2.5
commons-logging:commons-logging:jar:1.1.1
commons-net:commons-net:jar:2.2
de.jollyday:jollyday:jar:0.4.9
edu.stanford.nlp:stanford-corenlp:jar:3.8.0
edu.stanford.nlp:stanford-corenlp:jar:models
edu.stanford.nlp:stanford-corenlp:jar:models-english
io.dropwizard.metrics:metrics-core:jar:3.1.2
io.dropwizard.metrics:metrics-graphite:jar:3.1.2
io.dropwizard.metrics:metrics-json:jar:3.1.2
io.dropwizard.metrics:metrics-jvm:jar:3.1.2
io.netty:netty-all:jar:4.0.42.Final
io.netty:netty:jar:3.8.0.Final
javax.annotation:javax.annotation-api:jar:1.2
javax.cache:cache-api:jar:1.0.0
javax.inject:javax.inject:jar:1
javax.servlet:javax.servlet-api:jar:3.0.1
javax.servlet:javax.servlet-api:jar:3.1.0
javax.validation:validation-api:jar:1.1.0.Final
javax.ws.rs:javax.ws.rs-api:jar:2.0.1
javax.xml.bind:jaxb-api:jar:2.2.7
joda-time:joda-time:jar:2.9.4
junit:junit:jar:4.12
log4j:log4j:jar:1.2.12
log4j:log4j:jar:1.2.17
net.dean.jraw:JRAW:jar:1.0.0
net.dean.jraw:moshi-deeply-nested:jar:1.0.0
net.java.dev.jets3t:jets3t:jar:0.7.1
net.jpountz.lz4:lz4:jar:1.3.0
net.lingala.zip4j:zip4j:jar:1.3.2
net.razorvine:pyrolite:jar:4.13
net.sf.py4j:py4j:jar:0.10.4
org.apache.avro:avro-ipc:jar:1.7.7
org.apache.avro:avro-ipc:jar:tests
org.apache.avro:avro-mapred:jar:hadoop2
org.apache.avro:avro:jar:1.7.7
org.apache.commons:commons-compress:jar:1.4.1
org.apache.commons:commons-compress:jar:1.7
org.apache.commons:commons-crypto:jar:1.0.0
org.apache.commons:commons-lang3:jar:3.3.1
org.apache.commons:commons-lang3:jar:3.5
org.apache.commons:commons-math3:jar:3.4.1
org.apache.commons:commons-math:jar:2.1
org.apache.curator:curator-client:jar:2.4.0
org.apache.curator:curator-framework:jar:2.4.0
org.apache.curator:curator-recipes:jar:2.4.0
org.apache.hadoop:hadoop-annotations:jar:2.2.0
org.apache.hadoop:hadoop-auth:jar:2.2.0
org.apache.hadoop:hadoop-client:jar:2.2.0
org.apache.hadoop:hadoop-common:jar:2.2.0
org.apache.hadoop:hadoop-hdfs:jar:2.2.0
org.apache.hadoop:hadoop-mapreduce-client-app:jar:2.2.0
org.apache.hadoop:hadoop-mapreduce-client-common:jar:2.2.0
org.apache.hadoop:hadoop-mapreduce-client-core:jar:2.2.0
org.apache.hadoop:hadoop-mapreduce-client-jobclient:jar:2.2.0
org.apache.hadoop:hadoop-mapreduce-client-shuffle:jar:2.2.0
org.apache.hadoop:hadoop-yarn-api:jar:2.2.0
org.apache.hadoop:hadoop-yarn-client:jar:2.2.0
org.apache.hadoop:hadoop-yarn-common:jar:2.2.0
org.apache.hadoop:hadoop-yarn-server-common:jar:2.2.0
org.apache.httpcomponents:httpclient:jar:4.2.5
org.apache.httpcomponents:httpcore:jar:4.2.4
org.apache.ivy:ivy:jar:2.4.0
org.apache.lucene:lucene-analyzers-common:jar:4.10.3
org.apache.lucene:lucene-core:jar:4.10.3
org.apache.lucene:lucene-queries:jar:4.10.3
org.apache.lucene:lucene-queryparser:jar:4.10.3
org.apache.lucene:lucene-sandbox:jar:4.10.3
org.apache.spark:spark-core_2.11:jar:2.1.1
org.apache.spark:spark-launcher_2.11:jar:2.1.1
org.apache.spark:spark-network-common_2.11:jar:2.1.1
org.apache.spark:spark-network-shuffle_2.11:jar:2.1.1
org.apache.spark:spark-tags_2.11:jar:2.1.1
org.apache.spark:spark-unsafe_2.11:jar:2.1.1
org.apache.xbean:xbean-asm5-shaded:jar:4.4
org.apache.zookeeper:zookeeper:jar:3.4.5
org.boofcv:boofcv-WebcamCapture:jar:0.28
org.boofcv:boofcv-calibration:jar:0.28
org.boofcv:boofcv-core:jar:0.28
org.boofcv:boofcv-feature:jar:0.28
org.boofcv:boofcv-geo:jar:0.28
org.boofcv:boofcv-io:jar:0.28
org.boofcv:boofcv-ip:jar:0.28
org.boofcv:boofcv-learning:jar:0.28
org.boofcv:boofcv-recognition:jar:0.28
org.boofcv:boofcv-sfm:jar:0.28
org.boofcv:boofcv-swing:jar:0.28
org.codehaus.jackson:jackson-core-asl:jar:1.9.13
org.codehaus.jackson:jackson-mapper-asl:jar:1.9.13
org.ddogleg:ddogleg:jar:0.13
org.deepboof:io:jar:0.4
org.deepboof:learning:jar:0.4
org.deepboof:main:jar:0.4
org.deepboof:models:jar:0.4
org.ejml:ejml-cdense:jar:0.33
org.ejml:ejml-core:jar:0.33
org.ejml:ejml-ddense:jar:0.33
org.ejml:ejml-dsparse:jar:0.33
org.ejml:ejml-fdense:jar:0.33
org.ejml:ejml-simple:jar:0.33
org.ejml:ejml-zdense:jar:0.33
org.fusesource.leveldbjni:leveldbjni-all:jar:1.8
org.georegression:georegression:jar:0.15
org.glassfish.hk2.external:aopalliance-repackaged:jar:2.4.0-b34
org.glassfish.hk2.external:javax.inject:jar:2.4.0-b34
org.glassfish.hk2:hk2-api:jar:2.4.0-b34
org.glassfish.hk2:hk2-locator:jar:2.4.0-b34
org.glassfish.hk2:hk2-utils:jar:2.4.0-b34
org.glassfish.hk2:osgi-resource-locator:jar:1.0.1
org.glassfish.jersey.bundles.repackaged:jersey-guava:jar:2.22.2
org.glassfish.jersey.containers:jersey-container-servlet-core:jar:2.22.2
org.glassfish.jersey.containers:jersey-container-servlet:jar:2.22.2
org.glassfish.jersey.core:jersey-client:jar:2.22.2
org.glassfish.jersey.core:jersey-common:jar:2.22.2
org.glassfish.jersey.core:jersey-server:jar:2.22.2
org.glassfish.jersey.media:jersey-media-jaxb:jar:2.22.2
org.glassfish:javax.json:jar:1.0.4
org.hamcrest:hamcrest-core:jar:1.3
org.javassist:javassist:jar:3.18.1-GA
org.jetbrains.kotlin:kotlin-stdlib:jar:1.2.10
org.jetbrains:annotations:jar:13.0
org.json4s:json4s-ast_2.11:jar:3.2.11
org.json4s:json4s-core_2.11:jar:3.2.11
org.json4s:json4s-jackson_2.11:jar:3.2.11
org.json:json:jar:20171018
org.mortbay.jetty:jetty-util:jar:6.1.26
org.objenesis:objenesis:jar:2.1
org.python:jython:jar:2.7.0
org.rauschig:jarchivelib:jar:0.5.0
org.roaringbitmap:RoaringBitmap:jar:0.5.11
org.scala-lang.modules:scala-parser-combinators_2.11:jar:1.0.1
org.scala-lang.modules:scala-xml_2.11:jar:1.0.1
org.scala-lang:scala-compiler:jar:2.11.0
org.scala-lang:scala-library:jar:2.11.8
org.scala-lang:scala-reflect:jar:2.11.8
org.scala-lang:scalap:jar:2.11.0
org.slf4j:jcl-over-slf4j:jar:1.7.16
org.slf4j:jul-to-slf4j:jar:1.7.16
org.slf4j:slf4j-api:jar:1.7.12
org.slf4j:slf4j-api:jar:1.7.16
org.slf4j:slf4j-api:jar:1.7.21
org.slf4j:slf4j-log4j12:jar:1.7.16
org.slf4j:slf4j-simple:jar:1.7.21
org.spark-project.spark:unused:jar:1.0.0
org.tukaani:xz:jar:1.0
org.tukaani:xz:jar:1.4
org.twitter4j:twitter4j-core:jar:4.0.1
org.twitter4j:twitter4j-stream:jar:4.0.1
org.xerial.snappy:snappy-java:jar:1.1.2.6
org.yaml:snakeyaml:jar:1.17
oro:oro:jar:2.0.8
xalan:xalan:jar:2.7.0
xerces:xercesImpl:jar:2.8.0
xml-apis:xml-apis:jar:1.3.03
xmlenc:xmlenc:jar:0.52
```
