package org.mystic.producer

import java.util.Properties

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}

import scala.util.parsing.json.JSON.parseFull
import scalaj.http.Http

case class MeetupStreamProducer(topicName: String, meetupURI: String, props: Properties) extends KafkaStreamProducer {

  val producer = new KafkaProducer[String, String](props)

  override def runStream() = {
    Http(meetupURI).execute(is => {
      scala.io.Source.fromInputStream(is).getLines().foreach(lines => {
        val map = parseFull(lines)
        val id = (map.get.asInstanceOf[Map[String, Object]]).get("rsvp_id").get.asInstanceOf[Double]
        val record = new ProducerRecord[String, String](topicName, java.lang.Long.toString(id.toLong), s"$lines")
        producer.send(record)
      })
    })
  }

}
