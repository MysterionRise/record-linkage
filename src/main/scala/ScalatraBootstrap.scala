import _root_.akka.actor.ActorSystem
import org.mystic.h2h.H2HMainServlet
import org.scalatra._
import javax.servlet.ServletContext
import org.slf4j.LoggerFactory
import scala.slick.session.Database

class ScalatraBootstrap extends LifeCycle {

  val logger = LoggerFactory.getLogger(getClass)
  // Get a handle to an ActorSystem and a refere
  val system = ActorSystem()

  // In the init method, mount your servlets with references to the system
  // and/or ActorRefs, as necessary.
  override def init(context: ServletContext) {
    Class.forName("org.postgresql.Driver")
    context.mount(new H2HMainServlet, "/*")
  }

  // Make sure you shut down
  override def destroy(context: ServletContext) {
    system.shutdown()
  }
}
