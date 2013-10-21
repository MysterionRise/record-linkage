package org.mystic.h2h


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
    contentType = "text/html"
    ssp("/khl",
      "layout" -> "WEB-INF/templates/layouts/khl.ssp",
      "pageSize" -> 50,
      "currentPage" -> 0,
      "uri" -> "/h2h-khl/",
      "leagueName" -> "КХЛ",
      "leagueURI" -> "http://www.sports.ru/fantasy/hockey/tournament/ratings/leaders/107.html")
  }

  get("/h2h-khl/:id") {
    contentType = "text/html"
    ssp("/khl",
      "layout" -> "WEB-INF/templates/layouts/khl.ssp",
      "pageSize" -> 50,
      "currentPage" -> Integer.parseInt(params("id")),
      "uri" -> "/h2h-khl/",
      "leagueName" -> "КХЛ",
      "leagueURI" -> "http://www.sports.ru/fantasy/hockey/tournament/ratings/leaders/107.html")
  }

  get("/") {
    contentType = "text/html"
    ssp("/index")
  }

  notFound {
    <h1>Not found. Bummer.</h1>
  }

}
