package org.mystic.h2h


import org.mystic.h2h.fantasy.LeagueManipulation

class H2HMainServlet extends H2hTestAppStack {

  get("/h2h-nba") {
    <html>
      <body>
        <h2>This is main page for NBA H2H on sports.ru</h2>
        Новый сезон NBA еще не начался, так что пока еще есть время для подготовки. А так же чествования чемпиона H2H NBA 2012/2013 -
        <a href="http://www.sports.ru/profile/28147397/">tan01</a>
      </body>
    </html>
  }

  get("/h2h-khl") {
    <html>
      <body>
        <h2>This is main page for KHL H2H on sports.ru</h2>
        <a href="http://www.sports.ru/fantasy/hockey/tournament/107.html">Текущее Fantasy страница</a>
      </body>
    </html>
  }

  get("/") {
    contentType="text/html"
    ssp("/index")
  }

  notFound {
    <h1>Not found. Bummer.</h1>
  }

}
