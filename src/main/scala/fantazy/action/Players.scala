package fantazy.action

import xitrum.annotation.GET
import xitrum.FutureAction

@GET("/players")
class Players extends FutureAction {
  override def execute(): Unit = {
    respondText("It's not 404, but still empty page")
  }
}
