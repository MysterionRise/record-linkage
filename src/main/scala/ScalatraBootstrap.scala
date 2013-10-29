import _root_.akka.actor.ActorSystem
import com.mchange.v2.c3p0.ComboPooledDataSource
import org.mystic.h2h.H2HMainServlet
import org.scalatra._
import javax.servlet.ServletContext
import org.slf4j.LoggerFactory
import scala.slick.session.Database

class ScalatraBootstrap extends LifeCycle {

  val logger = LoggerFactory.getLogger(getClass)
  val cpds = new ComboPooledDataSource
  cpds.setJdbcUrl(System.getenv("HEROKU_POSTGRESQL_AQUA_URL"))
  cpds.setDriverClass("")
  logger.info("Created c3p0 connection pool")

  // Get a handle to an ActorSystem and a refere
  val system = ActorSystem()

  // In the init method, mount your servlets with references to the system
  // and/or ActorRefs, as necessary.
  override def init(context: ServletContext) {
    val db = Database.forDataSource(cpds)  // create a Database which uses the DataSource
    context.mount(new H2HMainServlet(db), "/*")
  }

  private def closeDbConnection() {
    logger.info("Closing c3po connection pool")
    cpds.close
  }

  // Make sure you shut down
  override def destroy(context: ServletContext) {
    closeDbConnection
    system.shutdown()
  }
}
