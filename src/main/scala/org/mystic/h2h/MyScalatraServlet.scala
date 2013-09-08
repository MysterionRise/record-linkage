package org.mystic.h2h

import org.scalatra._
import scalate.ScalateSupport

class MyScalatraServlet extends H2hTestAppStack {

  get("/") {
    <html>
      <body>
        <h1>Hello, world!</h1>
        Say <a href="hello-scalate">hello to Scalate</a>.
      </body>
    </html>
  }
  
}
