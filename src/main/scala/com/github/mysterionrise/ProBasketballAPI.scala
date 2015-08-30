package com.github.mysterionrise

import com.github.mysterionrise.model.{GameStats, Player, Team}
import dispatch._
import org.json4s._
import org.json4s.native.JsonMethods._

import scala.collection.mutable.ArrayBuffer
import scala.concurrent.ExecutionContext.Implicits.global
import scala.io.StdIn._

object ProBasketballAPI {

  implicit def bigInt2Long(b: BigInt): Long = b.longValue()

  implicit def bigInt2Int(b: BigInt): Int = b.intValue()

  implicit def jvalue2JInt(j: JValue): JInt = j.asInstanceOf[JInt]

  implicit def jInt2Long(j: JInt): Long = j.num.longValue()

  implicit def jInt2Int(j: JInt): Int = j.num.intValue()

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
        val res = new ArrayBuffer[GameStats]()
        boxscores.arr.foreach(boxscore => {
          val gameId: JInt = boxscore \ "game_id"
          val fgm: JInt = boxscore \ "box_fgm"
          val fga: JInt = boxscore \ "box_fga"
          val fg3m: JInt = boxscore \ "box_fg3m"
          val fg3a: JInt = boxscore \ "box_fg3a"
          val ftm: JInt = boxscore \ "box_ftm"
          val fta: JInt = boxscore \ "box_fta"
          val oreb: JInt = boxscore \ "box_oreb"
          val dreb: JInt = boxscore \ "box_dreb"
          val ast: JInt = boxscore \ "box_ast"
          val stl: JInt = boxscore \ "box_stl"
          val blk: JInt = boxscore \ "box_blk"
          val to: JInt = boxscore \ "box_to"
          val pf: JInt = boxscore \ "box_pf"
          val pts: JInt = boxscore \ "box_pts"
          res.append(GameStats(gameId, fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, ast, stl, blk, to, pf, pts))
        })
        Some(res.toList)
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
