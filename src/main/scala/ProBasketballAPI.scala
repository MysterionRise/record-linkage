import dispatch.Defaults._
import dispatch._
import org.json4s._
import org.json4s.native.JsonMethods._

import scala.io.StdIn._

object ProBasketballAPI extends App {
  val api_key = readLine()
  val api = url("https://probasketballapi.com")
  // get stats for Paul Pierce in 2013-2014 season
  val params = Map("api_key" -> api_key, "player_id" -> "1718", "season" -> "2013")
  val headers = Map("Content-type" -> "application/json")
  val req = api / "stats" / "players" <<? params <:< headers
  // need to do like that, cause probasketball api is bad with SSL
  val http = Http.configure(_.setAcceptAnyCertificate(true))
  val response = http(req.POST OK as.String).either
  println(response)
  response() match {
    case Right(content) => {
      println("Content: " + pretty(render(parse(content))))
      http.shutdown()
    }
    case Left(StatusCode(404)) => println("Not found")
    case Left(StatusCode(code)) => println("Some other code: " + code.toString)
    case Left(e: Exception) => e.printStackTrace()
  }

}
