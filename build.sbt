name := "advanced-stats-analytics"

version := "1.0"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "net.databinder.dispatch" % "dispatch-core_2.11" % "0.11.3",
  "org.json4s" % "json4s-native_2.11" % "3.2.11"
)

val sparkVersion = "1.4.1"

// Needed as SBT's classloader doesn't work well with Spark
fork := true

fork in console := true

javaOptions ++= Seq("-Xmx2G")

scalacOptions ++= Seq("-deprecation", "-unchecked", "-feature")
