name := "advanced-analytics"

version := "1.0"
scalaVersion := "2.11.8"

resolvers += Resolver.mavenLocal
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

libraryDependencies += "com.hazelcast" % "hazelcast" % "3.7.4"

libraryDependencies += "org.apache.kafka" %% "kafka" % "0.10.1.1"

libraryDependencies += "org.apache.spark" %% "spark-streaming" % "2.1.0"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.1.0"

libraryDependencies += "org.apache.cassandra" % "cassandra-all" % "3.9"
