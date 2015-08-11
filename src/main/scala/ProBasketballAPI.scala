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

  def parseResponse(response: Future[Either[Throwable, String]]) = {
    response() match {
      case Right(content) => {
        println("Content: " + pretty(render(parse(content))))

      }
      case Left(StatusCode(404)) => println("Not found")
      case Left(StatusCode(code)) => println("Some other code: " + code.toString)
      case Left(e: Exception) => e.printStackTrace()
    }
  }

  def getAllPlayers(apiKey: String): JArray = {
    val params = Map("api_key" -> apiKey)
    val req = api / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response)
  }

  def getPlayerStats(apiKey: String, playerId: String) = {
    val params = Map("api_key" -> apiKey, "player_id" -> playerId)
    val req = api / "stats" / "players" <<? params <:< headers
    val response = http(req.POST OK as.String).either
    parseResponse(response)
  }

}
