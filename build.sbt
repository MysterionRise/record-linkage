import sbtassembly.MergeStrategy

name := "advanced-analytics"

version := "1.0"
scalaVersion := "2.11.8"

resolvers += Resolver.mavenLocal
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

libraryDependencies += "com.hazelcast" % "hazelcast" % "3.7.4"

libraryDependencies += "com.hazelcast" % "hazelcast-client" % "3.7.4"

/*libraryDependencies += "org.apache.kafka" %% "kafka" % "0.10.1.1"

libraryDependencies += "org.apache.spark" %% "spark-streaming" % "2.1.0"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.1.0"

libraryDependencies += "org.apache.cassandra" % "cassandra-all" % "3.9"

libraryDependencies += "org.scalaj" %% "scalaj-http" % "2.3.0"

libraryDependencies += "org.twitter4j" % "twitter4j-stream" % "4.0.6"

// unsure if it's really needed, tbd
libraryDependencies += "org.twitter4j" % "twitter4j-http2-support" % "4.0.6"*/

assemblyJarName in assembly := "poc.jar"

mainClass in assembly := Some("org.mystic.cache.Main")

//assemblyMergeStrategy in assembly := {
//  case PathList("META-INF", xs @ _*) =>
//    (xs map {_.toLowerCase}) match {
//      case _ => MergeStrategy.discard
//    }
//  case PathList("javax", "servlet", xs @ _*)         => MergeStrategy.first
//  case PathList(ps @ _*) if ps.last endsWith ".html" => MergeStrategy.first
//  case "application.conf"                            => MergeStrategy.concat
//  case "unwanted.txt"                                => MergeStrategy.discard
//  case _                                             => MergeStrategy.first
//}
