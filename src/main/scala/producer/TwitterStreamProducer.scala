package org.mystic.producer

import java.util.Properties

import twitter4j._
import twitter4j.auth.AccessToken

case class TwitterStreamProducer(topicName: String, props: Properties, accessToken: AccessToken, consumerKey: String, consumerSecret: String) extends KafkaStreamProducer {

  override def runStream() = {
    val twitterStream = new TwitterStreamFactory().getInstance()
    // from configs and from twitter profile
    twitterStream.setOAuthConsumer(consumerKey, consumerSecret)
    twitterStream.setOAuthAccessToken(accessToken)
    twitterStream.addListener(listener)
    // sample() method internally creates a thread which manipulates TwitterStream and calls these adequate listener methods continuously.
    twitterStream.sample()
  }

  val listener = new StatusListener {
    override def onStallWarning(warning: StallWarning) = ???

    override def onDeletionNotice(statusDeletionNotice: StatusDeletionNotice) = {
      // someone decided to delete tweet for some reason
      val userID = statusDeletionNotice.getUserId
      val statusID = statusDeletionNotice.getStatusId
      // send message to kafka
    }

    override def onScrubGeo(userId: Long, upToStatusId: Long) = ???

    override def onStatus(status: Status) = {
      // someone posted the tweet
      val userID = status.getUser.getId
      val statusID = status.getId
      val text = status.getText
      println(status.getText)
      //send message to kafka

    }

    override def onTrackLimitationNotice(numberOfLimitedStatuses: Int) = ???

    override def onException(ex: Exception) = ???
  }

}
