package org.mystic.h2h.fantasy

import collection.mutable.HashMap
import org.slf4j.LoggerFactory

/**
 * @author mysterion
 *         Crawling from sports.ru
 */
class SportsCrawler {

  var map = new HashMap[String, Int]()

  val logger = LoggerFactory.getLogger(getClass)

  def getMap(): HashMap[String, Int] = {
    logger.info(map.toString())
    map
  }

  def netParse(sUrl: String): Unit = {
    val name: String = userName(sUrl)
    //nameOfTeam(sUrl)
    val cost: String = costOfTeam(sUrl)
    val bal: String = balanceOfTeam(sUrl)
    val totalCost = Integer.parseInt(cost.substring(4, cost.length - 5)) + Integer.parseInt(bal.substring(4, bal.length - 5))
    map.put(name, totalCost)
    //log.info(name + " " + totalCost.toString)
  }

  def userName(urlstring: String): String = {
    val url = new java.net.URL(urlstring)
    val scan = new java.util.Scanner(url.openStream)
    while (scan.hasNext) {
      val s = scan.nextLine
      // @todo remove hardcoded values
      if (s.contains("<th>Пользователь</th>")) {
        val str: String = scan.nextLine.substring(48)
        return str.substring(0, str.length - 9).replace(">", "").replace("\"", "")
      }
    }
    null
  }

  def nameOfTeam(urlstring: String): Unit = {
    val url = new java.net.URL(urlstring)
    val scan = new java.util.Scanner(url.openStream)
    while (scan.hasNext) {
      val s = scan.nextLine
      if (s.contains("<title>")) {
        logger.info(s.substring(7))
      }
    }
  }

  def costOfTeam(urlstring: String): String = {
    val url = new java.net.URL(urlstring)
    val scan = new java.util.Scanner(url.openStream)
    while (scan.hasNext) {
      val s = scan.nextLine
      if (s.contains("<th>Стоимость команды</th>")) {
        return scan.nextLine
      }
    }
    null
  }

  def balanceOfTeam(urlstring: String): String = {
    val url = new java.net.URL(urlstring)
    val scan = new java.util.Scanner(url.openStream)
    while (scan.hasNext) {
      val s = scan.nextLine
      if (s.contains("<th>Баланс</th>")) {
        return scan.nextLine
      }
    }
    null
  }
}