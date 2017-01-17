package org.mystic.producer

import java.util.Properties

import org.apache.kafka.clients.producer.ProducerRecord

import scalaj.http.Http

case class MeetupStreamProducer(topicName: String, meetupURI: String, props: Properties) extends KafkaStreamProducer {

  override def runStream() = {
    Http(meetupURI).execute(is => {
      scala.io.Source.fromInputStream(is).getLines().foreach(lines => {
        println(lines)
        val record = new ProducerRecord(topicName, "key", s"$lines")
        //producer.send(record)
      })
    })
  }

}
