package org.mystic.h2h.fantasy

import scala.slick.driver.PostgresDriver.simple._

object Players extends Table[(String, Int)]("PLAYERS") {
  def name = column[String]("PLAYER_NAME", O.PrimaryKey)

  def cost = column[Int]("COST")

  def * = name ~ cost
}

