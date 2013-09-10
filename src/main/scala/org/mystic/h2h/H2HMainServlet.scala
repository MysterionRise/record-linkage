package org.mystic.h2h

import org.scalatra._
import scalate.ScalateSupport

class H2HMainServlet extends H2hTestAppStack {

  get("/h2h-nba") {
    <html>
      <body>
        <h1>This is main page for NBA H2H on sports.ru</h1>
        Новый сезон NBA еще не начался, так что пока еще есть время для подготовки. А так же чествования чемпиона H2H NBA 2012/2013 - <a href="http://www.sports.ru/profile/28147397/">tan01</a>
      </body>
    </html>
  }

}
