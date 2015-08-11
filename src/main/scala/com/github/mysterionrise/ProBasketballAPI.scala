package com.github.mysterionrise

import com.github.mysterionrise.model.Player
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

  }

  def parseResponse(response: Future[Either[Throwable, String]]): JValue = {
    response() match {
      case Right(content) => {
        val res = res(content)
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

  def getAllPlayers(apiKey: String): Array[Player] = {
    val params = Map("api_key" -> apiKey)
    val req = api / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    val result = parseResponse(response)
  }

  def getPlayerStats(apiKey: String, playerId: String) = {
    val params = Map("api_key" -> apiKey, "player_id" -> playerId)
    val req = api / "stats" / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response)
  }

}
