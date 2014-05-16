package org.mystic.fantazy.action

import xitrum.annotation.GET
import xitrum.{ActorAction, FutureAction}
import org.mystic.fantazy.parser.PlayersCrawler

@GET("/players")
class Players extends ActorAction {

  override def execute(): Unit = {
    respondView()
  }

  def renderLeague(leagueURI: String) = {
    PlayersCrawler.getAllTeams(leagueURI)
  }
}
