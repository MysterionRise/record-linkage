package org.mystic.fantazy.action

import xitrum.annotation.GET
import xitrum.FutureAction

@GET("/about")
class About extends FutureAction {
  override def execute(): Unit = {
    respondView()
  }
}
