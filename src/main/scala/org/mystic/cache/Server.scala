package org.mystic.cache

import com.hazelcast.core.{Hazelcast, IMap, IQueue}

object Server {

  def main(args: Array[String]): Unit = {
    val hz = Hazelcast.newHazelcastInstance()
    val skus: IMap[Int, Int] = hz.getMap("skus")

  }
}
