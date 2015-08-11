package com.github.mysterionrise

import com.github.mysterionrise.model.{GameStats, Player}
import dispatch.Defaults._
import dispatch._
import org.json4s._
import org.json4s.native.JsonMethods._

import scala.io.StdIn._

object ProBasketballAPI {

  val api = url("https://probasketballapi.com")
  val headers = Map("Content-type" -> "application/json")
  // need to do like that, cause probasketball api is bad with SSL
  val http = Http.configure(_.setAcceptAnyCertificate(true))

  def main(args: Array[String]) {
    val apiKey = readLine()
    getAllPlayers(apiKey) match {
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
        } yield Player(id.intValue, team.intValue, name, date.longValue)
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
        val arr = for {
          JObject(boxscore) <- boxscores
          JField("id", JInt(id)) <- boxscore
        } yield GameStats(id.longValue)
        Some(arr)
      }
      case _ => {
        println("Error happens during parsing")
        None
      }
    }
  }

}
