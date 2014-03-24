package org.mystic.h2h.snippet

import net.liftweb.http.S

class HelloWorld {

  def howdy =
    <span>Welcome to H2H Fantazy at
      {new _root_.java.util.Date}
    </span>
}
