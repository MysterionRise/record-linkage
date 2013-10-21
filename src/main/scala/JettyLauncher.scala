import org.eclipse.jetty.server.Server
import org.eclipse.jetty.servlet.DefaultServlet
import org.eclipse.jetty.webapp.WebAppContext
import org.slf4j.LoggerFactory

object JettyLauncher {

  val logger = LoggerFactory.getLogger(getClass)

  def main(args: Array[String]) {
    val port = if (System.getenv("PORT") != null) System.getenv("PORT").toInt else 8080
    val server = new Server(port)
    val context = new WebAppContext()
    context setContextPath "/"
    context.setResourceBase("src/main/webapp")
    context.addServlet(classOf[org.mystic.h2h.H2HMainServlet], "/*")
    context.addServlet(classOf[DefaultServlet], "/")

    server.setHandler(context)
    try {
      server.start
      server.join
    } catch {
      case e: Exception => {
        logger.error(e.getMessage, e)
      }
    }
  }
}
