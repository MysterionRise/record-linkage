package org.mystic.sports.h2h

import com.mongodb.casbah.MongoConnection
import com.mongodb.casbah.commons.MongoDBObject
import org.joda.time.DateTime


/**
 * User: kperikov
 * Date: 20.03.13
 * Time: 13:08
 */
object DBGateway {

  private val date = "dayOfTheWeek"

  def saveH2HData(dbName: String, collName: String, data: List[(String, String)]) = {
    val mongoConn = {
      MongoConnection()(dbName)(collName)
    }
    val builder = {
      MongoDBObject.newBuilder
    }
    data foreach (f => builder += f._1 -> f._2)
    builder += date -> DateTime.now.dayOfWeek().get().toString
    mongoConn save builder.result
  }

  def deleteH2HData(dbName: String, collName: String, day: String) = {
    val mongoConn = {
      MongoConnection()(dbName)(collName)
    }
    mongoConn remove MongoDBObject(date -> day)
  }

  /**
   * def readTest = {
    val mongoConn = MongoConnection()("test")("foo")

    mongoConn.find(MongoDBObject.empty).foreach { x =>
      // do some work if you found the user...
      println("Found something! %s %s".format(x("avg"), x("date")))
    }
  }
   */
  def findH2HData(dbName: String, collName: String, day: String) = {
    val mongoConn = {
      MongoConnection()(dbName)(collName)
    }

    mongoConn findOne MongoDBObject(date -> day) foreach {
      x =>
      // do some work if you found the user...
        println(x)
    }
    //      println(it.getAs[String]("name"))
    //      println(it.getAs[String]("cost"))
    //      println(it.getAs[String]("dayOfTheWeek"))

  }
}
