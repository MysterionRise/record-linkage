package org.mystic.h2h.fantasy

import scala.collection.mutable.{ListBuffer, HashMap}
import org.slf4j.LoggerFactory

/**
 * @author mysterion
 *         Crawling from sports.ru
 */
//@todo global todo, need to refactor this parser to use HtmlCleaner, or some SAX-style parser, not Scanner
class TeamParser {

  val logger = LoggerFactory.getLogger(getClass)

  def getItAll(urlstring: String): Array[String] = {
    val url = new java.net.URL(urlstring)
    val scan = new java.util.Scanner(url.openStream, "UTF-8")
    val result = new Array[String](6)
    while (scan.hasNext) {
      val s = scan.nextLine
      if (s.contains("<th>Пользователь</th>")) {
        val str: String = scan.nextLine.substring(48)
        result(3) = str.substring(0, str.length - 9).replace(">", "").replace("\"", "")
        // teamURI, teamName, playerURI, playerName, score, bal
      }
      if (s.contains("<title>")) {
        result(1) = s.substring(7, s.length - ": профиль - Фэнтези - Sports.ru</title>".length)
      }
      if (s.contains("<th>Стоимость команды</th>")) {
        result(4) = scan.nextLine
      }
      if (s.contains("<th>Баланс</th>")) {
        result(5) = scan.nextLine
      }
    }
    result
  }
}