package org.mystic.producer

import java.util.Properties

import scalaj.http._
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import twitter4j._
import twitter4j.auth.AccessToken

object Test {

  val consumerKey = "u7wWl3LBVOmm5szpaacDpBXqb"
  val consumerSecret = "97Jd8mAzz6Wj76ouYjfRdPq659TFEjqvpX9RbnO8ASxIN5uKPX"

  def loadAccessToken(): AccessToken = {
    // should be take from configs
    val token = "3019761227-GnYDDk7xcTKdcMGCgmSWjSfCVaXhIReqiJd3vCT"
    val secret = "sPYlXtUPWc6abx0fAJIeDdEytxL1cHvjBpqRE1JcVkwYu"
    return new AccessToken(token, secret)
  }

  def main(args: Array[String]): Unit = {
    val props = new Properties()
    props.put("bootstrap.servers", "localhost:9092")

    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)

    /*val TOPIC = "test"

    Http("http://stream.meetup.com/2/rsvps").execute(is => {
      scala.io.Source.fromInputStream(is).getLines().foreach(lines => {
        println(lines)
        val record = new ProducerRecord(TOPIC, "key", s"$lines")
        //producer.send(record)
      })
    })*/

    val twittterProducer = new TwitterStreamProducer("tweets", props, loadAccessToken(), consumerKey, consumerSecret)
    twittterProducer.runStream()

    val meetupStreamProducer = new MeetupStreamProducer("")

  }
}
