package org.mystic.h2h.fantasy

import scala.slick.driver.PostgresDriver._

object Players extends Table[(String, Int)]("PLAYERS") {
  def playerName = column[String]("PLAYER_NAME", O.PrimaryKey)

  def totalCost = column[Int]("COST")

  def * = playerName ~ totalCost
}
