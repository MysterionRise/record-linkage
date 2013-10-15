package org.mystic.fix.server

import org.mystic.sports.h2h.{DBGateway, SportsCrawler}
import org.slf4j.LoggerFactory

/**
 * @author mysterion
 *         Main app that presents the starting point for crawling sports.ru
 */

object App  {

  // @todo add configuration layer, using typesafe config factory
  private val DB_NAME = "test"
  private val COLL_NAME = "h2h-nba"
  private val DAY = "1"

//  Logging.configure {
//    log =>
//    log.level = Level.INFO
//    log.file.enabled = true
//    log.file.filename = "scala-sport-h2h-crawler.log"
//  }


  // @todo remove hardlinkz
  def main(args: Array[String]) {
    val s = new SportsCrawler
    val players: List[String] = List(
      "http://www.sports.ru/fantasy/basketball/team/254572.html",
      "http://www.sports.ru/fantasy/basketball/team/254572.html",
      "http://www.sports.ru/fantasy/basketball/team/254575.html",
      "http://www.sports.ru/fantasy/basketball/team/254590.html",
      "http://www.sports.ru/fantasy/basketball/team/254591.html",
      "http://www.sports.ru/fantasy/basketball/team/254597.html",
      "http://www.sports.ru/fantasy/basketball/team/254684.html",
      "http://www.sports.ru/fantasy/basketball/team/254687.html",
      "http://www.sports.ru/fantasy/basketball/team/254748.html",
      "http://www.sports.ru/fantasy/basketball/team/254770.html",
      "http://www.sports.ru/fantasy/basketball/team/254786.html",
      "http://www.sports.ru/fantasy/basketball/team/254789.html",
      "http://www.sports.ru/fantasy/basketball/team/254816.html",
      "http://www.sports.ru/fantasy/basketball/team/254870.html",
      "http://www.sports.ru/fantasy/basketball/team/254906.html",
      "http://www.sports.ru/fantasy/basketball/team/254957.html",
      "http://www.sports.ru/fantasy/basketball/team/254980.html",
      "http://www.sports.ru/fantasy/basketball/team/254983.html",
      "http://www.sports.ru/fantasy/basketball/team/255079.html",
      "http://www.sports.ru/fantasy/basketball/team/255082.html",
      "http://www.sports.ru/fantasy/basketball/team/255215.html",
      "http://www.sports.ru/fantasy/basketball/team/255216.html",
      "http://www.sports.ru/fantasy/basketball/team/255239.html",
      "http://www.sports.ru/fantasy/basketball/team/255424.html",
      "http://www.sports.ru/fantasy/basketball/team/255578.html",
      "http://www.sports.ru/fantasy/basketball/team/255682.html",
      "http://www.sports.ru/fantasy/basketball/team/255738.html",
      "http://www.sports.ru/fantasy/basketball/team/255772.html",
      "http://www.sports.ru/fantasy/basketball/team/255878.html",
      "http://www.sports.ru/fantasy/basketball/team/255967.html",
      "http://www.sports.ru/fantasy/basketball/team/256066.html",
      "http://www.sports.ru/fantasy/basketball/team/256128.html",
      "http://www.sports.ru/fantasy/basketball/team/256245.html")
    
    players.foreach((url: String) => s.netParse(url))
    val logger =  LoggerFactory.getLogger(getClass)
    logger.debug("test")
    val map = s.getMap
    val it: Iterator[String] = map.keysIterator
    while (it.hasNext) {
      val name = it.next()
      println(map.get(name).get.toString)
    }
  }
}
