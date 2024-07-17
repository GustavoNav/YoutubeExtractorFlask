CREATE DATABASE IF NOT EXISTS youtube_extractor_db;


CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_channel_about` (
    channel_id VARCHAR(255) PRIMARY KEY,
    date_creation DATE,
    channel_location VARCHAR(255),
    extraction_date DATETIME
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_channel_metrics` (
    metric_id BIGINT NOT NULL AUTO_INCREMENT,
    channel_id VARCHAR(255),
    channel_name VARCHAR(255),
    icon VARCHAR(255),
    banner VARCHAR(255),
    subscriptions BIGINT,
    videos BIGINT,
    views BIGINT,
    extraction_date DATETIME,
    PRIMARY KEY (metric_id),
    FOREIGN KEY (channel_id) REFERENCES tb_channel_about(channel_id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_videos` (
    video_id BIGINT NOT NULL AUTO_INCREMENT,
    channel_id VARCHAR(255) NOT NULL,
    channel_link VARCHAR(255) not null,
    title VARCHAR(255),
    likes BIGINT,
    views BIGINT,
    comments BIGINT,
    duration TIME,
    video_date DATE,
    thumb VARCHAR(255),
    trending BOOLEAN,
    family_friend BOOLEAN,
    extraction_date DATETIME,
    PRIMARY KEY (video_id),
    FOREIGN KEY (channel_id) REFERENCES tb_channel_about(channel_id)
) ENGINE=INNODB;