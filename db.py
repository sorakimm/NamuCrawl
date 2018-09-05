# -*- coding:utf-8 -*-

from mylogging import MyLogger
import dbConnect

dbLogFile = 'log/db.log'
dbLogger = MyLogger(dbLogFile)

dbi = dbConnect.DBConnect()

class DB():
    def makeNamuwikiTable(self):
        makeTableQuery = """
             CREATE TABLE IF NOT EXISTS `namuwiki_db`.`namuwiki` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `title` VARCHAR(1300) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL,
            `url` VARCHAR(1300) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NOT NULL,
            `content` LONGTEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL,
            `image` VARCHAR(1300) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL,
            `editdate` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL,
            `crawltime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `html` LONGTEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL,
            `urlhash` CHAR(32) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE INDEX `urlhash_UNIQUE` (`urlhash` ASC))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8mb4
            COLLATE = utf8mb4_unicode_ci;            
        """

        dbLogger.debug("makeNamuwikiDB")
        try:
            return dbi.query(makeTableQuery)
        except Exception as e:
            return dbLogger.error(e)

    def insertNamuwikiDB(self, dbTuple):
        insertDBQuery = """
            INSERT INTO namuwiki (title, url, content, image, editdate, crawltime, html, urlhash)\
            VALUES (%s, %s, %s, %s, %s, NOW(), %s, md5(%s))
            ON DUPLICATE KEY UPDATE 
            title=%s, url=%s, content=%s, image=%s, editdate=%s, crawltime=NOW(), html=%s
            """

        dbLogger.debug('insertNamuwikiDB')
        try:
            return dbi.insert(insertDBQuery, dbTuple + dbTuple[:-1])
        except Exception as e:
            return dbLogger.error(e)


    def selectRecentUrl(self):
        selectRecentUrl = """
        SELECT url FROM namuwiki ORDER BY id DESC
        """
        dbLogger.debug("selectRecentUrl")
        try:
            return dbi.select(selectRecentUrl)
        except Exception as e:
            return dbLogger.error(e)


    def recentCrawlCheck(self, _url):
        recentCrawlCheck = """
        SELECT id FROM namuwiki WHERE url=%s AND crawltime >  NOW() - INTERVAL 1 DAY
        """
        try:
            return dbi.select(recentCrawlCheck, (_url))

        except Exception as e:
            return dbLogger.error(e)
