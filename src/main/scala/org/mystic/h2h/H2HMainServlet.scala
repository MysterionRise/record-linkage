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

  get("/") {
    <html>
      <body>
        <h2>List of current H2H Fantasy Games</h2>
        <ul>
          <li>
            <a href="/h2h-nba">H2H NBA 2013/2014</a>
          </li>
        </ul>
      </body>
    </html>
  }

}
