organization := "org.mystic"

name := "h2h-fantazy"

version := "0.1-SNAPSHOT"

scalaVersion := "2.10.3"

seq(webSettings: _*)

libraryDependencies ++= {
  val liftVersion = "2.5.1"
  Seq(
    "net.liftweb" %% "lift-webkit" % liftVersion % "compile",
    "org.eclipse.jetty" % "jetty-webapp" % "8.1.7.v20120910" %
      "container,test",
    "org.eclipse.jetty.orbit" % "javax.servlet" % "3.0.0.v201112011016" % "container,compile" artifacts Artifact("javax.servlet", "jar", "jar"),
    "com.github.nscala-time" %% "nscala-time" % "0.6.0",
    "net.sourceforge.htmlcleaner" % "htmlcleaner" % "2.6.1",
    "org.squeryl" %% "squeryl" % "0.9.5-6",
    "c3p0" % "c3p0" % "0.9.1.2",
    "org.postgresql" % "postgresql" % "9.2-1003-jdbc4"
  )
}