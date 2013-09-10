import _root_.akka.actor.{ActorSystem, Props}
import org.mystic.h2h.H2HMainServlet
import org.scalatra._
import javax.servlet.ServletContext

class ScalatraBootstrap extends LifeCycle {

  // Get a handle to an ActorSystem and a refere

  val system = ActorSystem()
  // In the init method, mount your servlets with references to the system
  // and/or ActorRefs, as necessary.
  override def init(context: ServletContext) {
    context.mount(new H2HMainServlet, "/*")
  }

  // Make sure you shut down
  override def destroy(context: ServletContext) {
    system.shutdown()
  }
}
