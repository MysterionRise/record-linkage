package fantazy.action

import xitrum.FutureAction
import xitrum.annotation.GET

@GET("/leagues")
class Leagues extends FutureAction{
  override def execute(): Unit = {
    respondText("It's not 404, but still empty page")
  }
}
