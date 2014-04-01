package fantazy.action

import xitrum.Action
import xitrum.annotation.GET

@GET("/admin")
class Admin extends Action {

  beforeFilter {
    basicAuth("H2H Realm") {
      (username, password) =>
        username == "username" && password == "password"
    }
  }

  override def execute(): Unit = {
    respondText("Admin page, should be secured!")
  }
}
