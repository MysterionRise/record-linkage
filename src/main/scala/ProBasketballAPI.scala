import dispatch.Defaults._
import dispatch._

object ProBasketballAPI extends App {
   val svc = url("http://api.hostip.info/country.php")
   val country = Http(svc OK as.String)
    for (c <- country)
      println(c)

 }
