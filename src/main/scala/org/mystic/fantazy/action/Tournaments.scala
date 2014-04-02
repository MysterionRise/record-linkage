package org.mystic.fantazy.action

import xitrum.FutureAction
import xitrum.annotation.GET

@GET("/tournaments")
class Tournaments extends FutureAction{
  override def execute(): Unit = {
    respondText("It's not 404, but still empty page")
  }
}
