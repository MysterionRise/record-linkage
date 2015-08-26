package com.github.mysterionrise

import com.github.mysterionrise.model.{Team, Player, GameStats}
import dispatch._
import org.json4s._
import org.json4s.native.JsonMethods._

import scala.concurrent.ExecutionContext.Implicits.global
import scala.io.StdIn._

object ProBasketballAPI {

  implicit def bigInt2Long(b: BigInt): Long = b.longValue()

  implicit def bigInt2Int(b: BigInt): Int = b.intValue()

  val api = url("https://probasketballapi.com")
  val headers = Map("Content-type" -> "application/json")
  // need to do like that, cause probasketball api is bad with SSL
  val http = Http.configure(_.setAcceptAnyCertificate(true))

  def main(args: Array[String]) = {
    val apiKey = readLine()
    // todo it's all about Paul Pierce
    getPlayerStats(apiKey, "1718") match {
      case Some(x) => x.foreach(p => println(p))
      case _ =>
    }
  }

  def parseResponse(response: Future[Either[Throwable, String]]): JValue = {
    response() match {
      case Right(content) => {
        val res = parse(content)
        println("Content: " + pretty(render(res)))
        res
      }
      case Left(StatusCode(code)) => {
        println(s"Error code: ${code.toString}")
        JNull
      }
      case Left(e: Exception) => {
        e.printStackTrace()
        JNull
      }
      case _ => JNull
    }
  }

  def getAllPlayers(apiKey: String): Option[List[Player]] = {
    val params = Map("api_key" -> apiKey)
    val req = api / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response) match {
      case (players: JArray) => {
        val arr = for {
          JObject(player) <- players
          JField("player_id", JInt(id)) <- player
          JField("team_id", JInt(team)) <- player
          JField("player_name", JString(name)) <- player
          JField("birth_date", JInt(date)) <- player
        } yield Player(id, team, name, date)
        Some(arr)
      }
      case _ => {
        println("Error happens during parsing")
        None
      }
    }
  }

  def getPlayerStats(apiKey: String, playerId: String): Option[List[GameStats]] = {
    val params = Map("api_key" -> apiKey, "player_id" -> playerId)
    val req = api / "stats" / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response) match {
      case (boxscores: JArray) => {
        val res = for {
          JObject(boxscore) <- boxscores
          JField("id", JInt(id)) <- boxscore
          JField("game_id", JInt(gameId)) <- boxscore
          JField("team_id", JInt(teamId)) <- boxscore
          JField("opponent_id", JInt(oppId)) <- boxscore
          JField("box_fgm", JInt(fgm)) <- boxscore
          JField("box_fga", JInt(fga)) <- boxscore
          JField("box_fg3m", JInt(fg3m)) <- boxscore
          JField("box_fg3a", JInt(fg3a)) <- boxscore
          JField("box_ftm", JInt(ftm)) <- boxscore
          JField("box_fta", JInt(fta)) <- boxscore
          JField("box_oreb", JInt(oreb)) <- boxscore
          JField("box_dreb", JInt(dreb)) <- boxscore
          JField("box_ast", JInt(ast)) <- boxscore
//          JField("box_stl", JInt(stl)) <- boxscore
//          JField("box_blk", JInt(blk)) <- boxscore
//          JField("box_to", JInt(to)) <- boxscore
//          JField("box_pf", JInt(pf)) <- boxscore
//          JField("box_pts", JInt(pts)) <- boxscore
//          JField("box_plus_minus", JInt(plusMinus)) <- boxscore
        } yield GameStats(id, gameId, teamId, oppId,
            fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, ast, 0, 0, 0, 0, 0, 0)
//          yield GameStats(id, gameId, teamId, oppId,
//            fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, ast, stl, blk, to, pf, pts, plusMinus)
        Some(List())
      }
      case _ => {
        println("Error happens during parsing")
        None
      }
    }
  }

  def getAllTeams(apiKey: String): Option[List[Team]] = {
    val params = Map("api_key" -> apiKey)
    val req = api / "teams" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response) match {
      case (teams: JArray) => {
        val arr = for {
          JObject(team) <- teams
          JField("team_id", JInt(id)) <- team
          JField("team_name", JString(name)) <- team
          JField("city", JString(city)) <- team
          JField("abbreviation", JString(abb)) <- team
        } yield Team(id, name, city, abb)
        Some(arr)
      }
      case _ => {
        println("Error happens during parsing")
        None
      }
    }
  }

}
