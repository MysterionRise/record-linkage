import dispatch.Defaults._
import dispatch._

import scala.io.StdIn._

object ProBasketballAPI extends App {
  val api_key = readLine()
  val api = url("https://probasketballapi.com")
  val params = Map("api_key" -> api_key)
  val headers = Map("Content-type" -> "application/json")
  val req = api / "teams" <<? params <:< headers
  // need to do like that, cause probasketball api is bad with SSL
  val http = Http.configure(_.setAcceptAnyCertificate(true))
  val response = http(req.POST OK as.String).either
  println(response)
  response() match {
    case Right(content) => println("Content: " + content)
    case Left(StatusCode(404)) => println("Not found")
    case Left(StatusCode(code)) => println("Some other code: " + code.toString)
    case Left(e: Exception) => e.printStackTrace()
  }
  Http.shutdown()
}
