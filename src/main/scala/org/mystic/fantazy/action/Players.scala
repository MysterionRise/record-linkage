package org.mystic.fantazy.action

import xitrum.annotation.GET
import xitrum.FutureAction

@GET("/players")
class Players extends FutureAction {
  override def execute(): Unit = {
    respondDefault404Page()
  }
}
