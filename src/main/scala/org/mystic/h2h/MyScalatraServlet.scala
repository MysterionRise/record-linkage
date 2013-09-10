package org.mystic.h2h

import org.scalatra._
import scalate.ScalateSupport

class MyScalatraServlet extends H2hTestAppStack {

  get("/") {
    <html>
      <body>
        <h1>Hello, H2H Fantasy!</h1>
        Say <a href="hello-scalate">hello to H2H Fantasy</a>.
      </body>
    </html>
  }

}
