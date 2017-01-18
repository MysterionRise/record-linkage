package org.mystic.cache

import com.hazelcast.config.Config
import com.hazelcast.core.{Hazelcast, IQueue}


object Main {

  def main(args: Array[String]): Unit = {
    // try to get hazelcast.xml from classpath
    val hz1 = Hazelcast.newHazelcastInstance();
    val hz2 = Hazelcast.newHazelcastInstance();


    /*val config = new Config()
    config.setInstanceName("test")
    val network = config.getNetworkConfig()
    val join = network.getJoin()
    join.getMulticastConfig().setEnabled(false)
    val hz = Hazelcast.newHazelcastInstance(config)*/

    val q1: IQueue[String] = hz1.getQueue("q")
    q1.put("test1")

    val q2: IQueue[String] = hz2.getQueue("q")
    println(q2.poll())

    hz1.shutdown()
    hz2.shutdown()
  }
}
