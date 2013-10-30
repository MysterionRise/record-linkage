import org.mystic.h2h.{DatabaseInit, H2HMainServlet}
import org.scalatra._
import javax.servlet.ServletContext

class ScalatraBootstrap extends LifeCycle with DatabaseInit {

  override def init(context: ServletContext) {
    configureDb()
    context mount(new H2HMainServlet, "/*")
  }

  override def destroy(context: ServletContext) {
    closeDbConnection()
  }
}
