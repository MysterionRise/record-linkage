name := "advanced-analytics"

version := "1.0"

scalaVersion := "2.11.6"

resolvers += Resolver.mavenLocal
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"

libraryDependencies += "org.apache.commons" % "commons-math3" % "3.6.1"

libraryDependencies += "org.jfree" % "jfreechart" % "1.0.19"
