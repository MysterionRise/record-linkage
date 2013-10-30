package org.mystic.h2h

import com.mchange.v2.c3p0.ComboPooledDataSource
import org.squeryl.adapters.{PostgreSqlAdapter, MySQLAdapter}
import org.squeryl.Session
import org.squeryl.SessionFactory
import org.slf4j.LoggerFactory

trait DatabaseInit {
  val logger = LoggerFactory.getLogger(getClass)

  val databaseUsername = System.getenv("LOGIN")
  val databasePassword = System.getenv("PASSWORD")
  val databaseConnection = "jdbc:postgresql://ec2-54-235-174-213.compute-1.amazonaws.com:5432/d64ect80vid8v2"

  var cpds = new ComboPooledDataSource

  def configureDb() {
    cpds.setDriverClass("org.postgresql.Driver")
    cpds.setJdbcUrl(databaseConnection)
    cpds.setUser(databaseUsername)
    cpds.setPassword(databasePassword)

    cpds.setMinPoolSize(1)
    cpds.setAcquireIncrement(1)
    cpds.setMaxPoolSize(50)

    SessionFactory.concreteFactory = Some(() => connection)

    def connection = {
      logger.info("Creating connection with c3po connection pool")
      Session.create(cpds.getConnection, new PostgreSqlAdapter)
    }
  }

  def closeDbConnection() {
    logger.info("Closing c3po connection pool")
    cpds.close()
  }
}