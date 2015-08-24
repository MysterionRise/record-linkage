name := "advanced-stats-analytics"

version := "1.0"

scalaVersion := "2.10.5"

libraryDependencies ++= Seq(
  "net.databinder.dispatch" %% "dispatch-core" % "0.11.3",
  "org.json4s" %% "json4s-native" % "3.2.11",
  "org.apache.spark" %% "spark-core" % "1.4.1"

)

// Needed as SBT's classloader doesn't work well with Spark
fork := true

// BUG: unfortunately, it's not supported right now
fork in console := true

// Java version
javacOptions ++= Seq("-source", "1.7", "-target", "1.7")

// add a JVM option to use when forking a JVM for 'run'
javaOptions ++= Seq("-Xmx2G")

// append -deprecation to the options passed to the Scala compiler
scalacOptions ++= Seq("-deprecation", "-unchecked")