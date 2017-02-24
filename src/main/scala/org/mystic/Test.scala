package org.mystic

import java.util.Properties

import org.apache.kafka.clients.producer.KafkaProducer
import org.mystic.producer.{MeetupStreamProducer, TwitterStreamProducer}
import twitter4j.auth.AccessToken

object Test {

  def loadAccessToken(): AccessToken = {
    // should be take from configs
    return new AccessToken(TOKEN, SECRET)
  }

  def main(args: Array[String]): Unit = {
    val props = new Properties()
    props.put("bootstrap.servers", "localhost:9092")

    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)

    val twittterProducer = new TwitterStreamProducer("tweets", props, loadAccessToken(), CONSUMER_KEY, CONSUMER_SECRET)
    twittterProducer.runStream()

    val meetupStreamProducer = new MeetupStreamProducer("meetups", MEETUP_URI, props)
    meetupStreamProducer.runStream()

  }
}
