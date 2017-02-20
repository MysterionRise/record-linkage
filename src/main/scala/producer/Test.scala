package org.mystic.producer

import java.util.Properties

import scalaj.http._
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import twitter4j._
import twitter4j.auth.AccessToken

object Test {

  def loadAccessToken(): AccessToken = {
    // should be take from configs
    val token = ""
    val secret = ""
    return new AccessToken(token, secret)
  }

  def main(args: Array[String]): Unit = {
    /*val props = new Properties()
    props.put("bootstrap.servers", "localhost:9092")

    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)*/

    val TOPIC = "test"

    Http("http://stream.meetup.com/2/rsvps").execute(is => {
      scala.io.Source.fromInputStream(is).getLines().foreach(lines => {
        println(lines)
        val record = new ProducerRecord(TOPIC, "key", s"$lines")
        //producer.send(record)
      })
    })

    val listener = new StatusListener {
      override def onStallWarning(warning: StallWarning) = ???

      override def onDeletionNotice(statusDeletionNotice: StatusDeletionNotice) = ???

      override def onScrubGeo(userId: Long, upToStatusId: Long) = ???

      override def onStatus(status: Status) = ???

      override def onTrackLimitationNotice(numberOfLimitedStatuses: Int) = ???

      override def onException(ex: Exception) = ???
    }

    val twitterStream = new TwitterStreamFactory().getInstance()
    val accessToken = loadAccessToken()
    // from configs and from twitter profile
    twitterStream.setOAuthConsumer("[consumer key]", "[consumer secret]")
    twitterStream.setOAuthAccessToken(accessToken)
    twitterStream.addListener(listener)
    // sample() method internally creates a thread which manipulates TwitterStream and calls these adequate listener methods continuously.
    twitterStream.sample()

    //producer.close()

  }
}
