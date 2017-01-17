package org.mystic.producer

import java.util.Properties

import org.apache.kafka.clients.producer.ProducerRecord

import scalaj.http.Http

case class MeetupStreamProducer(topicName: String, meetupURI: String, props: Properties) extends KafkaStreamProducer {
  //"http://stream.meetup.com/2/rsvps"

  /*val props = new Properties()
   props.put("bootstrap.servers", "localhost:9092")

   props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
   props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
   val producer = new KafkaProducer[String, String](props)*/

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
