package org.mystic.bearded.scalatra

import org.scalatra._
import scalate.ScalateSupport

class MyScalatraServlet extends BeardedScalatraStack {

  get("/") {
    <html>
      <body>
        <h1>Hello, bearded world!</h1>
        Say <a href="hello-scalate">hello to Scalatra!</a>.
      </body>
    </html>
  }
  
}
