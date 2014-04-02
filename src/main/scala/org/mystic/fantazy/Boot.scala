package org.mystic.fantazy

import xitrum.Server
import util.Properties

object Boot {
  def main(args: Array[String]) {
    val port = Properties.envOrElse("PORT", "8000")
    System.setProperty("xitrum.port.http", port)
    Server.start()
  }
}
