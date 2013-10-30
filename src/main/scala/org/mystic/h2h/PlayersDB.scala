package org.mystic.h2h

import org.squeryl.PrimitiveTypeMode._
import org.squeryl.KeyedEntity
import org.squeryl.PersistenceStatus
import org.squeryl.Schema


class Player(val id: Long, val name: String, val cost: Int) extends ScalatraRecord {

  def this() = this(0, "default name", 0)

  def songs = from(PlayersDB.players)(s => where(s.id === id) select (s))
}

object PlayersDB extends Schema {
  val players = table[Player]("players")

  on(players)(a => declare(
    a.id is (autoIncremented)))
}

object Player {

  def create(player: Player): Boolean = {
    inTransaction {
      val result = PlayersDB.players.insert(player)
      if (result.isPersisted) {
        true
      } else {
        false
      }
    }
  }
}


trait ScalatraRecord extends KeyedEntity[Long] with PersistenceStatus {

}