name := "advanced-stats-analytics"

version := "1.0"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "net.databinder.dispatch" % "dispatch-core_2.11" % "0.11.3",
  "org.json4s" %% "json4s-native" % "3.2.11",
  "org.apache.spark" %% "spark-core" % "1.4.1"

)